import os
import logging
import json
import asyncio
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langgraph.graph import END, StateGraph
from .models.hiring_state import HiringState
from .utils.resume_parser import extract_resume_text
from .agents.resume_screener import create_screener_agent
from .agents.interview_scheduler import schedule_interview
from .agents.rejection_sender import send_rejection

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the workflow
def create_workflow(groq_api_key: str):
    logger.info("Creating workflow with GROQ API key")
    workflow = StateGraph(HiringState)
    
    # Add nodes
    logger.info("Adding workflow nodes")
    workflow.add_node("resume_screener", create_screener_agent(groq_api_key))
    workflow.add_node("schedule_interview", schedule_interview)
    workflow.add_node("send_rejection", send_rejection)
    
    # Set entry point
    workflow.set_entry_point("resume_screener")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "resume_screener",
        lambda state: state["next_step"],
        {
            "schedule_interview": "schedule_interview",
            "send_rejection": "send_rejection"
        }
    )
    
    # Add terminal edges
    workflow.add_edge("schedule_interview", END)
    workflow.add_edge("send_rejection", END)
    
    logger.info("Workflow created successfully")
    return workflow.compile()

async def process_resume_stream(
    file: UploadFile,
    name: str,
    email: str,
    position: str,
    job_description: str,
    company_name: str,
    interviewer: str,
    interviewer_email: str,
    interview_location: str
):
    try:
        logger.info("=== Starting Resume Processing ===")
        logger.info(f"Received request for candidate: {name}")
        
        # Read file content
        file_content = await file.read()
        logger.info(f"Successfully read file: {file.filename} ({len(file_content)} bytes)")
        
        # Extract resume text
        logger.info("Starting resume text extraction")
        resume_text = extract_resume_text(file_content, file.filename)
        logger.info(f"Successfully extracted resume text ({len(resume_text)} characters)")
        
        # Prepare candidate info
        candidate_info = {
            "name": name,
            "email": email,
            "position": position,
            "company_name": company_name,
            "job_description": job_description,
            "interviewer": interviewer,
            "interviewer_email": interviewer_email,
            "interview_location": interview_location,
            "resume_text": resume_text
        }
        logger.info("Candidate info prepared")
        
        # Initialize state
        state = {
            "candidate": candidate_info,
            "screening_result": {},
            "emails_sent": [],
            "final_decision": "",
            "next_step": "resume_screener",
            "history": []
        }
        logger.info("State initialized")
        
        # Get GROQ API key from environment
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            logger.error("GROQ_API_KEY environment variable is not set")
            raise ValueError("GROQ_API_KEY environment variable is not set")
        logger.info("GROQ API key found")
        
        # Create workflow
        logger.info("Creating workflow")
        workflow = create_workflow(groq_api_key)
        
        async def generate():
            logger.info("Starting workflow processing")
            try:
                # Send initial state
                initial_state = {
                    "status": "starting",
                    "next_step": "resume_screener",
                    "message": "Starting resume screening process..."
                }
                yield f"data: {json.dumps(initial_state)}\n\n"
                await asyncio.sleep(0.1)

                for output in workflow.stream(state):
                    # Send the current state
                    logger.info(f"Sending state update: {output.get('next_step', 'unknown')}")
                    state_update = {
                        "status": "processing",
                        "next_step": output.get("next_step", "unknown"),
                        "message": f"Processing {output.get('next_step', 'unknown')}...",
                        **output
                    }
                    yield f"data: {json.dumps(state_update)}\n\n"
                    await asyncio.sleep(0.1)
                    
                # Send completion message
                completion_state = {
                    "status": "complete",
                    "message": "Processing complete"
                }
                yield f"data: {json.dumps(completion_state)}\n\n"
                yield "data: [DONE]\n\n"
                
            except Exception as e:
                logger.error(f"Error in workflow: {str(e)}", exc_info=True)
                error_state = {
                    "status": "error",
                    "error": str(e),
                    "message": f"Error: {str(e)}"
                }
                yield f"data: {json.dumps(error_state)}\n\n"
                yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
        
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}", exc_info=True)
        raise

@app.post("/process-resume")
async def process_resume(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    position: str = Form(...),
    job_description: str = Form(...),
    company_name: str = Form(...),
    interviewer: str = Form(...),
    interviewer_email: str = Form(...),
    interview_location: str = Form(...)
):
    return await process_resume_stream(
        file, name, email, position, job_description,
        company_name, interviewer, interviewer_email, interview_location
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
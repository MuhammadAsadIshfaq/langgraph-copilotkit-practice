from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
import json
import logging
from pydantic import BaseModel

from .agents.resume_screener import screen_resume
from .agents.interview_scheduler import schedule_interview
from .agents.rejection_handler import send_rejection
from .utils.file_utils import extract_resume_text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Hiring Workflow API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CandidateInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    company_name: Optional[str] = None
    interviewer: Optional[str] = None
    interviewer_email: Optional[str] = None
    interview_location: Optional[str] = None

@app.post("/process-resume")
async def process_resume(
    resume: UploadFile = File(...),
    job_description: str = None,
    candidate_info: Optional[CandidateInfo] = None,
    background_tasks: BackgroundTasks = None
):
    try:
        # Validate file type
        allowed_types = {
            'application/pdf': '.pdf',
            'application/msword': '.doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx'
        }
        
        if resume.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types.values())}"
            )

        # Validate job description
        if not job_description or len(job_description.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Job description is required and must be at least 10 characters long"
            )

        # Read file content
        try:
            file_content = await resume.read()
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            raise HTTPException(status_code=500, detail="Error reading uploaded file")

        # Extract text from resume
        try:
            resume_text = extract_resume_text(file_content, resume.filename)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing resume")

        # Prepare initial state
        initial_state = {
            "candidate": {
                "resume_text": resume_text,
                "job_description": job_description,
                **(candidate_info.dict() if candidate_info else {})
            },
            "screening_result": {},
            "emails_sent": [],
            "final_decision": "",
            "next_step": "screen_resume",
            "history": []
        }
        
        # Process through workflow
        try:
            state = screen_resume(initial_state)
            
            if state["next_step"] == "schedule_interview":
                state = schedule_interview(state)
            elif state["next_step"] == "send_rejection":
                state = send_rejection(state)
                
            return state
        except Exception as e:
            logger.error(f"Error in workflow processing: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error processing resume through workflow"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"} 
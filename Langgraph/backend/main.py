from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
import os

from agents.resume_screening import ResumeScreeningAgent
from agents.email_communication import EmailCommunicationAgent
from agents.decision_making import DecisionMakingAgent

app = FastAPI(title="LangGraph Hiring System API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
resume_screening_agent = ResumeScreeningAgent()
email_communication_agent = EmailCommunicationAgent()
decision_making_agent = DecisionMakingAgent()

@app.post("/upload-resume")
async def upload_resume(
    resume: UploadFile = File(...),
    job_description: str = "",
    threshold_score: Optional[int] = 75
):
    """
    Upload and process a resume for the hiring workflow.
    
    Args:
        resume: The uploaded resume file
        job_description: Optional job description for screening
        threshold_score: Optional threshold score for screening
    """
    try:
        # Save uploaded file
        file_location = f"uploads/{resume.filename}"
        os.makedirs("uploads", exist_ok=True)
        with open(file_location, "wb") as file:
            file.write(await resume.read())

        # Process resume
        result = await resume_screening_agent.process_resume(
            file_location,
            job_description,
            threshold_score
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-email")
async def send_email(
    to_email: str,
    subject: str,
    content: str
):
    """Send an email to a candidate."""
    try:
        result = await email_communication_agent.send_email(
            to_email,
            subject,
            content
        )
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/make-decision")
async def make_decision(
    candidate_info: dict,
    screening_result: dict,
    emails_sent: list
):
    """Make a hiring decision based on the workflow state."""
    try:
        result = await decision_making_agent.make_decision(
            candidate_info,
            screening_result,
            emails_sent
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

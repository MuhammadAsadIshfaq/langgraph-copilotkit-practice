"""
FastAPI backend for the HR Assistant.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from agent.nodes import create_workflow
from agent.state import HRState, Candidate, Interview

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the workflow
workflow = create_workflow().compile()

# Pydantic models for request/response
class Message(BaseModel):
    content: str

class CandidateCreate(BaseModel):
    name: str
    email: str
    position: str

class InterviewCreate(BaseModel):
    candidate_id: str
    date: str
    interviewer: str

# Routes
@app.post("/chat")
async def chat(message: Message):
    """
    Process a chat message.
    """
    try:
        state = HRState(
            model="mixtral-8x7b-32768",
            current_task="chat",
            candidates=[],
            interviews=[],
            current_candidate=None,
            current_interview=None,
            logs=[],
            messages=[{"role": "user", "content": message.content}]
        )
        result = workflow.invoke(state)
        return {"response": result.messages[-1].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/candidates")
async def create_candidate(candidate: CandidateCreate):
    """
    Create a new candidate.
    """
    try:
        # Implementation for candidate creation
        return {"status": "success", "candidate": candidate}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/candidates")
async def get_candidates():
    """
    Get all candidates.
    """
    try:
        # Implementation for getting candidates
        return {"candidates": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/interviews")
async def create_interview(interview: InterviewCreate):
    """
    Schedule a new interview.
    """
    try:
        # Implementation for interview scheduling
        return {"status": "success", "interview": interview}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/interviews")
async def get_interviews():
    """
    Get all interviews.
    """
    try:
        # Implementation for getting interviews
        return {"interviews": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
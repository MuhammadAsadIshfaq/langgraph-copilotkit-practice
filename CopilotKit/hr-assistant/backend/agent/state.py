"""
State management for the HR Assistant agent.
Defines the state of the agent and conversation.
"""

from typing import List, TypedDict, Optional
from langgraph.graph import MessagesState

class Candidate(TypedDict):
    """
    Represents a job candidate.
    """
    name: str
    email: str
    position: str
    status: str
    notes: str

class Interview(TypedDict):
    """
    Represents an interview.
    """
    candidate_id: str
    date: str
    interviewer: str
    feedback: str
    status: str

class HRState(MessagesState):
    """
    State of the HR Assistant agent.
    """
    model: str
    current_task: str
    candidates: List[Candidate]
    interviews: List[Interview]
    current_candidate: Optional[Candidate]
    current_interview: Optional[Interview]
    logs: List[str] 
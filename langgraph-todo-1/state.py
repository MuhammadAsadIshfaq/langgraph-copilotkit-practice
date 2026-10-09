from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str
    name: str
    email: str

class Task(BaseModel):
    id: str
    title: str
    description: str
    status: str = "pending"
    assigned_to: Optional[str] = None
    created_by: str

class TodoState(BaseModel):
    users: Dict[str, User] = Field(default_factory=dict)
    tasks: Dict[str, Task] = Field(default_factory=dict)
    current_user: Optional[str] = None
    messages: List[dict] = Field(default_factory=list)
    error: Optional[str] = None 
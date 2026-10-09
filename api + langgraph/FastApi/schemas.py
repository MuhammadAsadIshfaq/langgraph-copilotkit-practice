from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from models import TaskStatus, Priority, Role

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    email: str
    name: Optional[str] = None
    role: Role
    createdAt: datetime
    updatedAt: datetime

class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus
    assigneeId: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    priority: Priority

class UserWithTasks(UserBase):
    tasks: List[TaskBase] = []

class TaskWithAssignee(TaskBase):
    assignee: Optional[UserBase] = None
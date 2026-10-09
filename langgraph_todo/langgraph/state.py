"""
State definition for the Todo Task Management Agent.
"""
from typing import TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage


class Task(TypedDict):
    """Task data structure"""
    id: str
    title: str
    description: Optional[str]
    status: str  # "pending", "in_progress", "completed", "cancelled"
    priority: str  # "low", "medium", "high", "urgent"
    assigned_to: Optional[str]  # user_id
    created_by: str  # user_id
    created_at: str
    updated_at: str
    due_date: Optional[str]
    tags: List[str]


class User(TypedDict):
    """User data structure"""
    id: str
    name: str
    email: str
    role: str  # "admin", "user", "viewer"
    created_at: str
    active: bool


class AgentState(TypedDict):
    """State for the Todo Task Management Agent"""
    messages: List[BaseMessage]
    tasks: Dict[str, Task]  # task_id -> Task
    users: Dict[str, User]  # user_id -> User
    current_user: Optional[str]  # current user_id
    last_operation: Optional[str]  # last performed operation
    operation_result: Optional[Dict[str, Any]]  # result of last operation
    error_message: Optional[str]  # error message if any
    next_action: Optional[str]  # next action to take
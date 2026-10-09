"""
State management for the Todo agent.
"""

from typing import List, Optional
from langgraph.graph import MessagesState

class Todo:
    id: str
    title: str
    description: str
    completed: bool
    priority: str
    due_date: Optional[str]

class TodoState(MessagesState):
    """State of the Todo agent and conversation."""
    model: str
    current_task: str
    todos: List[Todo]
    current_todo: Optional[Todo]
    logs: List[str] 
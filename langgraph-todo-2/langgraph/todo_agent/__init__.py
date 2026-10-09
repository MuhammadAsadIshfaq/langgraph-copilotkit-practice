"""
LangGraph Todo Management Agent

A modular, stateful AI agent for managing tasks and users with memory capabilities.
Built with LangGraph and Groq API integration.
"""

from ..agent import TodoAgent, create_todo_agent
from ..models import User, Task, TaskStatus
from ..memory import get_memory_instance, reset_memory
from ..config import get_config, AgentConfig

__version__ = "1.0.0"

__all__ = [
    'TodoAgent',
    'create_todo_agent', 
    'User',
    'Task',
    'TaskStatus',
    'get_memory_instance',
    'reset_memory',
    'get_config',
    'AgentConfig'
]
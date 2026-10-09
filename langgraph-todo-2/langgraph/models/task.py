"""
Task model for Todo Agent
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    """Enum for task status values"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    """Task data model for the todo system"""
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[str] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        """Initialize timestamps if not provided"""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at
    
    def update_status(self, new_status: TaskStatus):
        """Update task status and timestamp"""
        self.status = new_status
        self.updated_at = datetime.now().isoformat()
    
    def assign_to_user(self, user_id: str):
        """Assign task to a user"""
        self.assigned_to = user_id
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create Task instance from dictionary"""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            status=TaskStatus(data.get('status', 'pending')),
            assigned_to=data.get('assigned_to'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
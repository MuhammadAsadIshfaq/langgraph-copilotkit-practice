"""
User model for Todo Agent
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """User data model for the todo system"""
    id: str
    name: str
    email: str
    created_at: str = None
    
    def __post_init__(self):
        """Initialize creation timestamp if not provided"""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create User instance from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            created_at=data.get('created_at')
        )
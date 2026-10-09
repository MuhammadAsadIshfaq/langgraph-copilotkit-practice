"""
Memory storage system for Todo Agent
"""

from typing import Dict, Optional
from ..models import User, Task


class TodoMemory:
    """In-memory storage system for tasks and users"""
    
    def __init__(self):
        """Initialize empty storage"""
        self.users: Dict[str, User] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_counter = 0
        self.user_counter = 0
    
    def generate_task_id(self) -> str:
        """Generate unique task ID"""
        self.task_counter += 1
        return f"task_{self.task_counter}"
    
    def generate_user_id(self) -> str:
        """Generate unique user ID"""
        self.user_counter += 1
        return f"user_{self.user_counter}"
    
    # User operations
    def add_user(self, user: User) -> None:
        """Add user to memory"""
        self.users[user.id] = user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    def get_all_users(self) -> Dict[str, User]:
        """Get all users"""
        return self.users.copy()
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user by ID"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    # Task operations
    def add_task(self, task: Task) -> None:
        """Add task to memory"""
        self.tasks[task.id] = task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> Dict[str, Task]:
        """Get all tasks"""
        return self.tasks.copy()
    
    def get_tasks_by_user(self, user_id: str) -> Dict[str, Task]:
        """Get all tasks assigned to a specific user"""
        return {
            task_id: task for task_id, task in self.tasks.items()
            if task.assigned_to == user_id
        }
    
    def delete_task(self, task_id: str) -> bool:
        """Delete task by ID"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def clear_all(self) -> None:
        """Clear all data"""
        self.users.clear()
        self.tasks.clear()
        self.task_counter = 0
        self.user_counter = 0
    
    def get_stats(self) -> dict:
        """Get memory statistics"""
        return {
            'total_users': len(self.users),
            'total_tasks': len(self.tasks),
            'pending_tasks': len([t for t in self.tasks.values() if t.status.value == 'pending']),
            'in_progress_tasks': len([t for t in self.tasks.values() if t.status.value == 'in_progress']),
            'completed_tasks': len([t for t in self.tasks.values() if t.status.value == 'completed']),
            'unassigned_tasks': len([t for t in self.tasks.values() if t.assigned_to is None])
        }


# Global memory instance
_memory_instance = None


def get_memory_instance() -> TodoMemory:
    """Get or create the global memory instance (Singleton pattern)"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = TodoMemory()
    return _memory_instance


def reset_memory() -> None:
    """Reset the global memory instance"""
    global _memory_instance
    if _memory_instance:
        _memory_instance.clear_all()
    else:
        _memory_instance = TodoMemory()
"""
User management tools for Todo Agent
"""

from langchain_core.tools import tool
from ..models import User
from ..memory import get_memory_instance


@tool
def create_user(name: str, email: str) -> str:
    """Create a new user in the system
    
    Args:
        name: User's full name
        email: User's email address
    
    Returns:
        Success message with user ID or error message
    """
    try:
        memory = get_memory_instance()
        
        # Validate input
        if not name or not name.strip():
            return "Error: Name is required and cannot be empty"
        
        if not email or not email.strip():
            return "Error: Email is required and cannot be empty"
        
        # Basic email validation
        if '@' not in email or '.' not in email.split('@')[-1]:
            return "Error: Please provide a valid email address"
        
        # Check if user with email already exists
        existing_user = memory.get_user_by_email(email.strip())
        if existing_user:
            return f"Error: User with email {email} already exists (ID: {existing_user.id})"
        
        # Create new user
        user_id = memory.generate_user_id()
        user = User(id=user_id, name=name.strip(), email=email.strip())
        memory.add_user(user)
        
        return f"✅ User created successfully! ID: {user_id}, Name: {name.strip()}, Email: {email.strip()}"
    
    except Exception as e:
        return f"Error creating user: {str(e)}"


@tool
def list_users() -> str:
    """List all users in the system
    
    Returns:
        Formatted list of all users or message if no users exist
    """
    try:
        memory = get_memory_instance()
        users = memory.get_all_users()
        
        if not users:
            return "📋 No users found in the system"
        
        user_list = ["📋 Current Users:"]
        for user in users.values():
            user_info = f"  • ID: {user.id} | Name: {user.name} | Email: {user.email}"
            user_list.append(user_info)
        
        return "\n".join(user_list)
    
    except Exception as e:
        return f"Error listing users: {str(e)}"


@tool
def get_user_info(user_id: str) -> str:
    """Get detailed information about a specific user
    
    Args:
        user_id: ID of the user to get information about
    
    Returns:
        User information or error message
    """
    try:
        memory = get_memory_instance()
        user = memory.get_user(user_id)
        
        if not user:
            return f"Error: User with ID {user_id} not found"
        
        # Get user's tasks
        user_tasks = memory.get_tasks_by_user(user_id)
        task_count = len(user_tasks)
        
        info = [
            f"👤 User Information:",
            f"  • ID: {user.id}",
            f"  • Name: {user.name}",
            f"  • Email: {user.email}",
            f"  • Created: {user.created_at}",
            f"  • Assigned Tasks: {task_count}"
        ]
        
        if user_tasks:
            info.append("  • Task Details:")
            for task in user_tasks.values():
                info.append(f"    - {task.title} ({task.status.value})")
        
        return "\n".join(info)
    
    except Exception as e:
        return f"Error getting user info: {str(e)}"


@tool
def delete_user(user_id: str) -> str:
    """Delete a user from the system
    
    Args:
        user_id: ID of the user to delete
    
    Returns:
        Success or error message
    """
    try:
        memory = get_memory_instance()
        user = memory.get_user(user_id)
        
        if not user:
            return f"Error: User with ID {user_id} not found"
        
        # Check if user has assigned tasks
        user_tasks = memory.get_tasks_by_user(user_id)
        if user_tasks:
            task_titles = [task.title for task in user_tasks.values()]
            return f"Error: Cannot delete user {user.name}. They have {len(user_tasks)} assigned tasks: {', '.join(task_titles)}"
        
        # Delete user
        memory.delete_user(user_id)
        return f"✅ User '{user.name}' deleted successfully!"
    
    except Exception as e:
        return f"Error deleting user: {str(e)}"


def get_user_tools():
    """Get all user management tools"""
    return [create_user, list_users, get_user_info, delete_user]
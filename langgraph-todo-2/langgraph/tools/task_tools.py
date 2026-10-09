"""
Task management tools for Todo Agent
"""

from langchain_core.tools import tool
from ..models import Task, TaskStatus
from ..memory import get_memory_instance


@tool
def create_task(title: str, description: str) -> str:
    """Create a new task
    
    Args:
        title: Task title
        description: Task description
    
    Returns:
        Success message with task ID or error message
    """
    try:
        memory = get_memory_instance()
        
        # Validate input
        if not title or not title.strip():
            return "Error: Task title is required and cannot be empty"
        
        if not description or not description.strip():
            return "Error: Task description is required and cannot be empty"
        
        # Create new task
        task_id = memory.generate_task_id()
        task = Task(
            id=task_id, 
            title=title.strip(), 
            description=description.strip()
        )
        memory.add_task(task)
        
        return f"✅ Task created successfully! ID: {task_id}, Title: '{title.strip()}'"
    
    except Exception as e:
        return f"Error creating task: {str(e)}"


@tool
def assign_task(task_id: str, user_id: str) -> str:
    """Assign a task to a user
    
    Args:
        task_id: ID of the task to assign
        user_id: ID of the user to assign the task to
    
    Returns:
        Success or error message
    """
    try:
        memory = get_memory_instance()
        
        # Validate task exists
        task = memory.get_task(task_id)
        if not task:
            return f"Error: Task with ID {task_id} not found"
        
        # Validate user exists
        user = memory.get_user(user_id)
        if not user:
            return f"Error: User with ID {user_id} not found"
        
        # Check if task is already assigned
        if task.assigned_to:
            current_user = memory.get_user(task.assigned_to)
            current_user_name = current_user.name if current_user else "Unknown"
            return f"⚠️  Task '{task.title}' is already assigned to {current_user_name}. Use update to reassign."
        
        # Assign task
        task.assign_to_user(user_id)
        
        return f"✅ Task '{task.title}' assigned to {user.name} successfully!"
    
    except Exception as e:
        return f"Error assigning task: {str(e)}"


@tool
def update_task_status(task_id: str, status: str) -> str:
    """Update the status of a task
    
    Args:
        task_id: ID of the task to update
        status: New status (pending, in_progress, completed)
    
    Returns:
        Success or error message
    """
    try:
        memory = get_memory_instance()
        
        # Validate task exists
        task = memory.get_task(task_id)
        if not task:
            return f"Error: Task with ID {task_id} not found"
        
        # Validate status
        status = status.lower().strip()
        try:
            new_status = TaskStatus(status)
        except ValueError:
            valid_statuses = [s.value for s in TaskStatus]
            return f"Error: Invalid status '{status}'. Valid options: {', '.join(valid_statuses)}"
        
        # Check if status is already the same
        if task.status == new_status:
            return f"ℹ️  Task '{task.title}' is already in '{status}' status"
        
        # Update task status
        old_status = task.status.value
        task.update_status(new_status)
        
        return f"✅ Task '{task.title}' status updated from '{old_status}' to '{status}' successfully!"
    
    except Exception as e:
        return f"Error updating task status: {str(e)}"


@tool
def delete_task(task_id: str) -> str:
    """Delete a task from the system
    
    Args:
        task_id: ID of the task to delete
    
    Returns:
        Success or error message
    """
    try:
        memory = get_memory_instance()
        
        # Validate task exists
        task = memory.get_task(task_id)
        if not task:
            return f"Error: Task with ID {task_id} not found"
        
        # Store task info before deletion
        task_title = task.title
        
        # Delete task
        memory.delete_task(task_id)
        return f"✅ Task '{task_title}' deleted successfully!"
    
    except Exception as e:
        return f"Error deleting task: {str(e)}"


@tool
def list_tasks() -> str:
    """List all tasks in the system
    
    Returns:
        Formatted list of all tasks or message if no tasks exist
    """
    try:
        memory = get_memory_instance()
        tasks = memory.get_all_tasks()
        
        if not tasks:
            return "📋 No tasks found in the system"
        
        task_list = ["📋 Current Tasks:"]
        
        # Group tasks by status
        status_groups = {
            TaskStatus.PENDING: [],
            TaskStatus.IN_PROGRESS: [],
            TaskStatus.COMPLETED: []
        }
        
        for task in tasks.values():
            status_groups[task.status].append(task)
        
        # Display tasks grouped by status
        for status, status_tasks in status_groups.items():
            if status_tasks:
                task_list.append(f"\n  📌 {status.value.upper().replace('_', ' ')} ({len(status_tasks)}):")
                for task in status_tasks:
                    assigned_name = "Unassigned"
                    if task.assigned_to:
                        user = memory.get_user(task.assigned_to)
                        assigned_name = user.name if user else "Unknown User"
                    
                    task_info = f"    • {task.id}: {task.title} → {assigned_name}"
                    task_list.append(task_info)
        
        return "\n".join(task_list)
    
    except Exception as e:
        return f"Error listing tasks: {str(e)}"


@tool
def get_task_info(task_id: str) -> str:
    """Get detailed information about a specific task
    
    Args:
        task_id: ID of the task to get information about
    
    Returns:
        Task information or error message
    """
    try:
        memory = get_memory_instance()
        task = memory.get_task(task_id)
        
        if not task:
            return f"Error: Task with ID {task_id} not found"
        
        # Get assigned user info
        assigned_info = "Unassigned"
        if task.assigned_to:
            user = memory.get_user(task.assigned_to)
            assigned_info = f"{user.name} ({user.email})" if user else "Unknown User"
        
        info = [
            f"📋 Task Information:",
            f"  • ID: {task.id}",
            f"  • Title: {task.title}",
            f"  • Description: {task.description}",
            f"  • Status: {task.status.value}",
            f"  • Assigned to: {assigned_info}",
            f"  • Created: {task.created_at}",
            f"  • Updated: {task.updated_at}"
        ]
        
        return "\n".join(info)
    
    except Exception as e:
        return f"Error getting task info: {str(e)}"


@tool
def reassign_task(task_id: str, new_user_id: str) -> str:
    """Reassign a task to a different user
    
    Args:
        task_id: ID of the task to reassign
        new_user_id: ID of the new user to assign the task to
    
    Returns:
        Success or error message
    """
    try:
        memory = get_memory_instance()
        
        # Validate task exists
        task = memory.get_task(task_id)
        if not task:
            return f"Error: Task with ID {task_id} not found"
        
        # Validate new user exists
        new_user = memory.get_user(new_user_id)
        if not new_user:
            return f"Error: User with ID {new_user_id} not found"
        
        # Get old user info
        old_user_name = "Unassigned"
        if task.assigned_to:
            old_user = memory.get_user(task.assigned_to)
            old_user_name = old_user.name if old_user else "Unknown User"
        
        # Reassign task
        task.assign_to_user(new_user_id)
        
        return f"✅ Task '{task.title}' reassigned from {old_user_name} to {new_user.name} successfully!"
    
    except Exception as e:
        return f"Error reassigning task: {str(e)}"


def get_task_tools():
    """Get all task management tools"""
    return [
        create_task, 
        assign_task, 
        update_task_status, 
        delete_task, 
        list_tasks,
        get_task_info,
        reassign_task
    ]
import os
"""
Task Management Node and Tools
"""
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from state import AgentState, Task, User


@tool
def create_task(
    title: str,
    description: str = "",
    priority: str = "medium",
    assigned_to: Optional[str] = None,
    created_by: str = "system",
    due_date: Optional[str] = None,
    tags: List[str] = None
) -> Dict[str, Any]:
    """
    Create a new task.
    
    Args:
        title: Task title
        description: Task description
        priority: Task priority (low, medium, high, urgent)
        assigned_to: User ID to assign the task to
        created_by: User ID who created the task
        due_date: Due date in ISO format
        tags: List of tags for the task
    
    Returns:
        Dictionary with task creation result
    """
    if tags is None:
        tags = []
        
    task_id = str(uuid.uuid4())
    task: Task = {
        "id": task_id,
        "title": title,
        "description": description,
        "status": "pending",
        "priority": priority,
        "assigned_to": assigned_to,
        "created_by": created_by,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "due_date": due_date,
        "tags": tags
    }
    
    return {
        "success": True,
        "task": task,
        "message": f"Task '{title}' created successfully with ID: {task_id}"
    }


@tool
def get_task(task_id: str, tasks: Dict[str, Task]) -> Dict[str, Any]:
    """
    Get task by ID.
    
    Args:
        task_id: The task ID to retrieve
        tasks: Dictionary of tasks
    
    Returns:
        Dictionary with task data or error
    """
    if task_id in tasks:
        return {
            "success": True,
            "task": tasks[task_id],
            "message": f"Task found: {tasks[task_id]['title']}"
        }
    else:
        return {
            "success": False,
            "task": None,
            "message": f"Task with ID '{task_id}' not found"
        }


@tool
def list_tasks(
    tasks: Dict[str, Task],
    status: Optional[str] = None,
    assigned_to: Optional[str] = None,
    priority: Optional[str] = None,
    created_by: Optional[str] = None
) -> Dict[str, Any]:
    """
    List tasks with optional filters.
    
    Args:
        tasks: Dictionary of tasks
        status: Filter by status
        assigned_to: Filter by assigned user
        priority: Filter by priority
        created_by: Filter by creator
    
    Returns:
        Dictionary with list of tasks
    """
    task_list = []
    
    for task in tasks.values():
        # Apply filters
        if status and task["status"] != status:
            continue
        if assigned_to and task["assigned_to"] != assigned_to:
            continue
        if priority and task["priority"] != priority:
            continue
        if created_by and task["created_by"] != created_by:
            continue
            
        task_list.append(task)
    
    # Sort by priority and created date
    priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
    task_list.sort(key=lambda x: (priority_order.get(x["priority"], 4), x["created_at"]))
    
    return {
        "success": True,
        "tasks": task_list,
        "count": len(task_list),
        "message": f"Found {len(task_list)} tasks"
    }


@tool
def update_task(task_id: str, tasks: Dict[str, Task], **kwargs) -> Dict[str, Any]:
    """
    Update task information.
    
    Args:
        task_id: The task ID to update
        tasks: Dictionary of tasks
        **kwargs: Fields to update
    
    Returns:
        Dictionary with update result
    """
    if task_id not in tasks:
        return {
            "success": False,
            "message": f"Task with ID '{task_id}' not found"
        }
    
    task = tasks[task_id]
    updated_fields = []
    
    valid_fields = ["title", "description", "status", "priority", "assigned_to", "due_date", "tags"]
    
    for field, value in kwargs.items():
        if field in valid_fields and value is not None:
            task[field] = value
            updated_fields.append(field)
    
    # Update the updated_at timestamp
    task["updated_at"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "task": task,
        "updated_fields": updated_fields,
        "message": f"Task '{task['title']}' updated successfully"
    }


@tool
def assign_task(task_id: str, user_id: str, tasks: Dict[str, Task], users: Dict[str, User]) -> Dict[str, Any]:
    """
    Assign a task to a user.
    
    Args:
        task_id: The task ID to assign
        user_id: The user ID to assign to
        tasks: Dictionary of tasks
        users: Dictionary of users
    
    Returns:
        Dictionary with assignment result
    """
    if task_id not in tasks:
        return {
            "success": False,
            "message": f"Task with ID '{task_id}' not found"
        }
    
    if user_id not in users:
        return {
            "success": False,
            "message": f"User with ID '{user_id}' not found"
        }
    
    if not users[user_id].get("active", True):
        return {
            "success": False,
            "message": f"Cannot assign task to inactive user '{users[user_id]['name']}'"
        }
    
    tasks[task_id]["assigned_to"] = user_id
    tasks[task_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "task": tasks[task_id],
        "user": users[user_id],
        "message": f"Task '{tasks[task_id]['title']}' assigned to '{users[user_id]['name']}'"
    }


@tool
def delete_task(task_id: str, tasks: Dict[str, Task]) -> Dict[str, Any]:
    """
    Delete a task.
    
    Args:
        task_id: The task ID to delete
        tasks: Dictionary of tasks
    
    Returns:
        Dictionary with deletion result
    """
    if task_id not in tasks:
        return {
            "success": False,
            "message": f"Task with ID '{task_id}' not found"
        }
    
    task_title = tasks[task_id]["title"]
    del tasks[task_id]
    
    return {
        "success": True,
        "message": f"Task '{task_title}' deleted successfully"
    }


@tool
def complete_task(task_id: str, tasks: Dict[str, Task]) -> Dict[str, Any]:
    """
    Mark a task as completed.
    
    Args:
        task_id: The task ID to complete
        tasks: Dictionary of tasks
    
    Returns:
        Dictionary with completion result
    """
    if task_id not in tasks:
        return {
            "success": False,
            "message": f"Task with ID '{task_id}' not found"
        }
    
    tasks[task_id]["status"] = "completed"
    tasks[task_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "task": tasks[task_id],
        "message": f"Task '{tasks[task_id]['title']}' marked as completed"
    }


# Task management tools list
task_tools = [
    create_task,
    get_task,
    list_tasks,
    update_task,
    assign_task,
    delete_task,
    complete_task
]


def task_management_node(state: AgentState) -> AgentState:
    """
    Node for handling task management operations.
    """
    llm = ChatGroq(model="deepseek-r1-distill-llama-70b", temperature=0,api_key=os.environ.get("GROQ_API_KEY"))
    llm_with_tools = llm.bind_tools(task_tools)
    
    # Get the last human message for processing
    last_human_message = None
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            last_human_message = msg
            break
    
    if not last_human_message:
        return state
    
    # Process the message with the LLM
    response = llm_with_tools.invoke([last_human_message])
    
    # Handle tool calls
    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            # Execute the tool
            if tool_name == "create_task":
                result = create_task.invoke(tool_args)
                if result["success"]:
                    # Add task to state
                    task = result["task"]
                    state["tasks"][task["id"]] = task
                    
            elif tool_name == "get_task":
                tool_args["tasks"] = state["tasks"]
                result = get_task.invoke(tool_args)
                
            elif tool_name == "list_tasks":
                tool_args["tasks"] = state["tasks"]
                result = list_tasks.invoke(tool_args)
                
            elif tool_name == "update_task":
                tool_args["tasks"] = state["tasks"]
                result = update_task.invoke(tool_args)
                
            elif tool_name == "assign_task":
                tool_args["tasks"] = state["tasks"]
                tool_args["users"] = state["users"]
                result = assign_task.invoke(tool_args)
                
            elif tool_name == "delete_task":
                tool_args["tasks"] = state["tasks"]
                result = delete_task.invoke(tool_args)
                
            elif tool_name == "complete_task":
                tool_args["tasks"] = state["tasks"]
                result = complete_task.invoke(tool_args)
            
            # Store operation result
            state["last_operation"] = tool_name
            state["operation_result"] = result
    else:
        # No tool calls, just a regular response
        state["operation_result"] = {
            "success": False,
            "message": "I understand you want to work with tasks, but I need more specific information. Try: 'Create a task called Setup Project with high priority'"
        }
        state["last_operation"] = "task_chat"
    
    return state
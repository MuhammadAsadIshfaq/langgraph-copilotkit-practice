from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langchain.tools import tool
from state import TodoState, Task
import uuid

class TaskNodeInput(TypedDict):
    messages: list[BaseMessage]
    state: TodoState

def create_task_tool(state: TodoState) -> None:
    """Create a new task in the system."""
    @tool
    def create_task(title: str, description: str, created_by: str) -> str:
        """Create a new task with the given title and description."""
        if created_by not in state.users:
            return "Error: User not found"
        
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            title=title,
            description=description,
            created_by=created_by
        )
        state.tasks[task_id] = task
        return f"Task created successfully with ID: {task_id}"
    
    return create_task

def update_task_tool(state: TodoState) -> None:
    """Update an existing task."""
    @tool
    def update_task(task_id: str, title: str = None, description: str = None, status: str = None) -> str:
        """Update a task's details."""
        if task_id not in state.tasks:
            return "Error: Task not found"
        
        task = state.tasks[task_id]
        if title:
            task.title = title
        if description:
            task.description = description
        if status:
            task.status = status
        
        return f"Task {task_id} updated successfully"
    
    return update_task

def assign_task_tool(state: TodoState) -> None:
    """Assign a task to a user."""
    @tool
    def assign_task(task_id: str, user_id: str) -> str:
        """Assign a task to a user."""
        if task_id not in state.tasks:
            return "Error: Task not found"
        if user_id not in state.users:
            return "Error: User not found"
        
        state.tasks[task_id].assigned_to = user_id
        return f"Task {task_id} assigned to user {user_id}"
    
    return assign_task

def delete_task_tool(state: TodoState) -> None:
    """Delete a task."""
    @tool
    def delete_task(task_id: str) -> str:
        """Delete a task."""
        if task_id not in state.tasks:
            return "Error: Task not found"
        
        del state.tasks[task_id]
        return f"Task {task_id} deleted successfully"
    
    return delete_task

def task_node(state: TodoState, messages: list[BaseMessage]) -> dict:
    """Node for handling task-related operations."""
    llm = ChatGroq(temperature=0)
    
    # Create tools
    tools = [
        create_task_tool(state),
        update_task_tool(state),
        assign_task_tool(state),
        delete_task_tool(state)
    ]
    
    # Process the message with the LLM
    response = llm.invoke(messages, tools=tools)
    
    # Update state with the response
    state.messages.append({"role": "assistant", "content": response.content})
    
    return {"state": state} 
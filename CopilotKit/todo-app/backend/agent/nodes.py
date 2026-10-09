"""
Node functions for the Todo agent workflow.
"""

from typing import Annotated, Sequence, TypedDict
from langgraph.graph import Graph, StateGraph
from .state import TodoState, Todo
from .model import get_model, get_prompt_template
import uuid

def process_input(state: TodoState) -> TodoState:
    """Process user input and determine the action."""
    model = get_model()
    prompt = get_prompt_template()
    
    # Process the input and determine the action
    response = model.invoke(prompt.format(input=state.messages[-1].content))
    state.messages.append(response)
    
    # Update current task based on the response
    if "create" in response.content.lower():
        state.current_task = "create"
    elif "list" in response.content.lower():
        state.current_task = "list"
    elif "complete" in response.content.lower():
        state.current_task = "complete"
    elif "update" in response.content.lower():
        state.current_task = "update"
    elif "delete" in response.content.lower():
        state.current_task = "delete"
    else:
        state.current_task = "chat"
    
    return state

def create_todo(state: TodoState) -> TodoState:
    """Create a new todo."""
    if state.current_task == "create":
        # Extract todo details from the message
        message = state.messages[-1].content
        todo = Todo(
            id=str(uuid.uuid4()),
            title="New Todo",  # Extract from message
            description="",    # Extract from message
            completed=False,
            priority="medium", # Extract from message
            due_date=None     # Extract from message
        )
        state.todos.append(todo)
        state.current_todo = todo
        state.logs.append(f"Created new todo: {todo.title}")
    return state

def update_todo(state: TodoState) -> TodoState:
    """Update an existing todo."""
    if state.current_task == "update" and state.current_todo:
        # Update todo details based on the message
        message = state.messages[-1].content
        # Update logic here
        state.logs.append(f"Updated todo: {state.current_todo.title}")
    return state

def complete_todo(state: TodoState) -> TodoState:
    """Mark a todo as complete."""
    if state.current_task == "complete" and state.current_todo:
        state.current_todo.completed = True
        state.logs.append(f"Marked todo as complete: {state.current_todo.title}")
    return state

def delete_todo(state: TodoState) -> TodoState:
    """Delete a todo."""
    if state.current_task == "delete" and state.current_todo:
        state.todos = [t for t in state.todos if t.id != state.current_todo.id]
        state.current_todo = None
        state.logs.append("Deleted todo")
    return state

def generate_summary(state: TodoState) -> TodoState:
    """Generate a summary of todos."""
    if state.current_task == "list":
        summary = f"Total todos: {len(state.todos)}\n"
        summary += f"Completed: {len([t for t in state.todos if t.completed])}\n"
        summary += f"Pending: {len([t for t in state.todos if not t.completed])}\n"
        state.messages.append({"role": "assistant", "content": summary})
    return state

def create_workflow() -> Graph:
    """Create the workflow graph."""
    workflow = StateGraph(TodoState)
    
    # Add nodes
    workflow.add_node("process_input", process_input)
    workflow.add_node("create_todo", create_todo)
    workflow.add_node("update_todo", update_todo)
    workflow.add_node("complete_todo", complete_todo)
    workflow.add_node("delete_todo", delete_todo)
    workflow.add_node("generate_summary", generate_summary)
    
    # Set entry point
    workflow.set_entry_point("process_input")
    
    # Add edges
    workflow.add_edge("process_input", "create_todo")
    workflow.add_edge("process_input", "update_todo")
    workflow.add_edge("process_input", "complete_todo")
    workflow.add_edge("process_input", "delete_todo")
    workflow.add_edge("process_input", "generate_summary")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "process_input",
        lambda x: x.current_task,
        {
            "create": "create_todo",
            "update": "update_todo",
            "complete": "complete_todo",
            "delete": "delete_todo",
            "list": "generate_summary",
            "chat": "generate_summary"
        }
    )
    
    return workflow 
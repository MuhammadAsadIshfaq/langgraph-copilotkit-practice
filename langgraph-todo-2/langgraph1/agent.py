"""
LangGraph Todo Task Management Agent with Groq API
A stateful AI agent that manages tasks and users with memory capabilities
"""

import os
from typing import Dict, List, Optional, TypedDict, Annotated
from datetime import datetime
import json
from dataclasses import dataclass, asdict
from enum import Enum

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver





# Data Models
class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class User:
    """User data model"""
    id: str
    name: str
    email: str
    created_at: str = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class Task:
    """Task data model"""
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[str] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at


# Agent State
class AgentState(TypedDict):
    """State that persists across agent interactions"""
    messages: Annotated[list, add_messages]
    users: Dict[str, User]
    tasks: Dict[str, Task]
    last_action: str
    context: str


# In-memory storage (simulates persistent memory)
class TodoMemory:
    """Simple in-memory storage for tasks and users"""
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_counter = 0
        self.user_counter = 0
    
    def generate_task_id(self) -> str:
        self.task_counter += 1
        return f"task_{self.task_counter}"
    
    def generate_user_id(self) -> str:
        self.user_counter += 1
        return f"user_{self.user_counter}"


# Global memory instance
memory_store = TodoMemory()


# Tools for Task Management
@tool
def create_user(name: str, email: str) -> str:
    """Create a new user in the system
    
    Args:
        name: User's full name
        email: User's email address
    
    Returns:
        Success message with user ID
    """
    try:
        # Validate input
        if not name or not email:
            return "Error: Name and email are required"
        
        # Check if user with email already exists
        for user in memory_store.users.values():
            if user.email == email:
                return f"Error: User with email {email} already exists"
        
        # Create new user
        user_id = memory_store.generate_user_id()
        user = User(id=user_id, name=name, email=email)
        memory_store.users[user_id] = user
        
        return f"User created successfully! ID: {user_id}, Name: {name}, Email: {email}"
    
    except Exception as e:
        return f"Error creating user: {str(e)}"


@tool
def create_task(title: str, description: str) -> str:
    """Create a new task
    
    Args:
        title: Task title
        description: Task description
    
    Returns:
        Success message with task ID
    """
    try:
        # Validate input
        if not title or not description:
            return "Error: Title and description are required"
        
        # Create new task
        task_id = memory_store.generate_task_id()
        task = Task(id=task_id, title=title, description=description)
        memory_store.tasks[task_id] = task
        
        return f"Task created successfully! ID: {task_id}, Title: {title}"
    
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
        # Validate task exists
        if task_id not in memory_store.tasks:
            return f"Error: Task with ID {task_id} not found"
        
        # Validate user exists
        if user_id not in memory_store.users:
            return f"Error: User with ID {user_id} not found"
        
        # Assign task
        task = memory_store.tasks[task_id]
        user = memory_store.users[user_id]
        task.assigned_to = user_id
        task.updated_at = datetime.now().isoformat()
        
        return f"Task '{task.title}' assigned to {user.name} successfully!"
    
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
        # Validate task exists
        if task_id not in memory_store.tasks:
            return f"Error: Task with ID {task_id} not found"
        
        # Validate status
        try:
            new_status = TaskStatus(status.lower())
        except ValueError:
            return f"Error: Invalid status. Use 'pending', 'in_progress', or 'completed'"
        
        # Update task
        task = memory_store.tasks[task_id]
        task.status = new_status
        task.updated_at = datetime.now().isoformat()
        
        return f"Task '{task.title}' status updated to '{status}' successfully!"
    
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
        # Validate task exists
        if task_id not in memory_store.tasks:
            return f"Error: Task with ID {task_id} not found"
        
        # Delete task
        task = memory_store.tasks.pop(task_id)
        return f"Task '{task.title}' deleted successfully!"
    
    except Exception as e:
        return f"Error deleting task: {str(e)}"


@tool
def list_tasks() -> str:
    """List all tasks in the system
    
    Returns:
        Formatted list of all tasks
    """
    try:
        if not memory_store.tasks:
            return "No tasks found in the system"
        
        task_list = []
        for task in memory_store.tasks.values():
            assigned_name = "Unassigned"
            if task.assigned_to and task.assigned_to in memory_store.users:
                assigned_name = memory_store.users[task.assigned_to].name
            
            task_info = f"ID: {task.id} | Title: {task.title} | Status: {task.status.value} | Assigned to: {assigned_name}"
            task_list.append(task_info)
        
        return "Current Tasks:\n" + "\n".join(task_list)
    
    except Exception as e:
        return f"Error listing tasks: {str(e)}"


@tool
def list_users() -> str:
    """List all users in the system
    
    Returns:
        Formatted list of all users
    """
    try:
        if not memory_store.users:
            return "No users found in the system"
        
        user_list = []
        for user in memory_store.users.values():
            user_info = f"ID: {user.id} | Name: {user.name} | Email: {user.email}"
            user_list.append(user_info)
        
        return "Current Users:\n" + "\n".join(user_list)
    
    except Exception as e:
        return f"Error listing users: {str(e)}"


# Agent Nodes
def task_management_node(state: AgentState):
    """Node for handling task-related operations"""
    # Tools available in this node
    tools = [create_task, update_task_status, delete_task, assign_task, list_tasks]
    
    # Create tool node
    tool_node = ToolNode(tools)
    
    # Initialize LLM with Groq
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",  # You can change this to other Groq models
        temperature=0.1,
        api_key=os.environ.get("GROQ_API_KEY")
    )
    
    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(tools)
    
    # Get the latest message
    messages = state["messages"]
    
    # Add system message for task management context
    system_msg = SystemMessage(content="""
    You are a task management assistant. You help users create, update, delete, and assign tasks.
    
    Available operations:
    - Create tasks with title and description
    - Update task status (pending, in_progress, completed)
    - Delete tasks
    - Assign tasks to users (make sure user exists first)
    - List all tasks
    
    Always be helpful and provide clear feedback about the operations performed.
    If you need to assign a task, make sure the user exists first by listing users.
    """)
    
    # Invoke LLM with tools
    response = llm_with_tools.invoke([system_msg] + messages)
    
    # return {"messages": [response], "last_action": "task_management"}
    state["messages"].append(response)
    state["last_action"] = "task_management"

    return state


def user_management_node(state: AgentState):
    """Node for handling user-related operations"""
    # Tools available in this node
    tools = [create_user, list_users]
    
    # Create tool node
    tool_node = ToolNode(tools)
    
    # Initialize LLM with Groq
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        api_key=os.environ.get("GROQ_API_KEY")
    )
    
    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(tools)
    
    # Get the latest message
    messages = state["messages"]
    
    # Add system message for user management context
    system_msg = SystemMessage(content="""
    You are a user management assistant. You help create and manage users in the todo system.
    
    Available operations:
    - Create new users with name and email
    - List all existing users
    
    Always validate that required information (name and email) is provided before creating users.
    Provide clear feedback about the operations performed.
    """)
    
    # Invoke LLM with tools
    response = llm_with_tools.invoke([system_msg] + messages)
    
    # return {"messages": [response], "last_action": "user_management"}
    state["messages"].append(response)
    state["last_action"] = "user_management"

    return state

def router_node(state: AgentState):
    """Router node to determine which specialized node to use"""
    # Initialize LLM for routing decisions
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        api_key=os.environ.get("GROQ_API_KEY")
    )
    
    # Get the latest user message
    messages = state["messages"]
    latest_message = messages[-1].content if messages else ""
    
    # System message for routing logic
    system_msg = SystemMessage(content="""
    You are a router that determines which type of operation the user wants to perform.
    
    Analyze the user's message and respond with ONLY one of these options:
    - "TASK_MANAGEMENT" - if the user wants to create, update, delete, assign tasks, or list tasks
    - "USER_MANAGEMENT" - if the user wants to create users or list users
    - "GENERAL" - for general questions or greetings
    
    Examples:
    - "Create a task" -> TASK_MANAGEMENT
    - "Add a new user" -> USER_MANAGEMENT  
    - "Hello" -> GENERAL
    - "Assign task to user" -> TASK_MANAGEMENT
    - "List all tasks" -> TASK_MANAGEMENT
    - "Show me users" -> USER_MANAGEMENT
    """)
    
    routing_message = HumanMessage(content=f"Route this message: {latest_message}")
    response = llm.invoke([system_msg, routing_message])
    
    # Extract routing decision
    decision = response.content.strip().upper()
    
    return {"context": decision, "last_action": "routing"}


def general_node(state: AgentState):
    """Node for handling general queries and greetings"""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        api_key=os.environ.get("GROQ_API_KEY")
    )
    
    messages = state["messages"]
    
    system_msg = SystemMessage(content="""
    You are a friendly todo management assistant. You help users manage their tasks and users.
    
    You can help with:
    - Creating, updating, deleting, and assigning tasks
    - Creating and managing users
    - Listing tasks and users
    
    Be friendly and guide users on what they can do with this system.
    """)
    
    response = llm.invoke([system_msg] + messages)
    
    # return {"messages": [response], "last_action": "general"}
    state["messages"].append(response)
    state["last_action"] = "general"

    return state


# Conditional edge function for routing
def route_decision(state: AgentState):
    """Determine which node to route to based on context"""
    context = state.get("context", "")
    
    if "TASK_MANAGEMENT" in context:
        return "task_management"
    elif "USER_MANAGEMENT" in context:
        return "user_management"
    else:
        return "general"


# Build the LangGraph workflow
def create_todo_agent():
    """Create the LangGraph todo management agent"""
    
    # Initialize the graph with state
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("router", router_node)
    workflow.add_node("task_management", task_management_node)
    workflow.add_node("user_management", user_management_node)
    workflow.add_node("general", general_node)
    
    # Add tool nodes for each management type
    task_tools = [create_task, update_task_status, delete_task, assign_task, list_tasks]
    user_tools = [create_user, list_users]
    
    workflow.add_node("task_tools", ToolNode(task_tools))
    workflow.add_node("user_tools", ToolNode(user_tools))
    
    # Define the workflow edges
    workflow.add_edge(START, "router")
    workflow.add_conditional_edges(
        "router",
        route_decision,
        {
            "task_management": "task_management",
            "user_management": "user_management", 
            "general": "general"
        }
    )
    
    # Add edges from management nodes to tool nodes
    workflow.add_edge("task_management", "task_tools")
    workflow.add_edge("user_management", "user_tools")
    
    # Add edges to END
    workflow.add_edge("task_tools", END)
    workflow.add_edge("user_tools", END)
    workflow.add_edge("general", END)
    
    # Add memory for persistence
    memory = MemorySaver()
    
    # Compile the graph
    app = workflow.compile(checkpointer=memory)
    
    return app


# Usage example and testing
def main():
    
    # Create the agent
    agent = create_todo_agent()
    
    # Configuration for the conversation
    config = {"configurable": {"thread_id": "todo_session_1"}}
    
    print("Todo Management Agent is ready!")
    print("You can:")
    print("- Create users: 'Create a user named John with email john@example.com'")
    print("- Create tasks: 'Create a task called Setup Project with description Set up the new project'")
    print("- Assign tasks: 'Assign task_1 to user_1'")
    print("- Update task status: 'Update task_1 status to in_progress'")
    print("- List tasks/users: 'List all tasks' or 'Show me all users'")
    print("- Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Create initial state
            initial_state = {
                "messages": [HumanMessage(content=user_input)],
                "users": memory_store.users,
                "tasks": memory_store.tasks,
                "last_action": "",
                "context": ""
            }
            
            # Run the agent
            result = agent.invoke(initial_state, config)
            
            # Get the last AI message
            if result["messages"]:
                last_message = result["messages"][-1]
                if hasattr(last_message, 'content'):
                    print(f"Assistant: {last_message.content}")
                else:
                    print(f"Assistant: {last_message}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()




"""
Router node for Todo Agent
"""

from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from ..config import get_config


class AgentState(TypedDict):
    """State that persists across agent interactions"""
    messages: Annotated[list, add_messages]
    last_action: str
    context: str


def router_node(state: AgentState) -> dict:
    """Router node to determine which specialized node to use"""
    
    config = get_config()
    
    # Initialize LLM for routing decisions
    llm = ChatGroq(
        model=config.groq_model,
        temperature=config.temperature,
        groq_api_key=config.groq_api_key
    )
    
    # Get the latest user message
    messages = state["messages"]
    latest_message = messages[-1].content if messages else ""
    
    # System message for routing logic
    system_msg = SystemMessage(content="""
    You are a router that determines which type of operation the user wants to perform.
    
    Analyze the user's message and respond with ONLY one of these options:
    - "TASK_MANAGEMENT" - if the user wants to create, update, delete, assign, reassign tasks, or list tasks
    - "USER_MANAGEMENT" - if the user wants to create users, delete users, or list users
    - "GENERAL" - for general questions, greetings, or help requests
    
    Examples:
    - "Create a task" -> TASK_MANAGEMENT
    - "Add a new user" -> USER_MANAGEMENT  
    - "Hello" -> GENERAL
    - "Assign task to user" -> TASK_MANAGEMENT
    - "List all tasks" -> TASK_MANAGEMENT
    - "Show me users" -> USER_MANAGEMENT
    - "Update task status" -> TASK_MANAGEMENT
    - "Delete user" -> USER_MANAGEMENT
    - "Help me" -> GENERAL
    - "What can you do?" -> GENERAL
    
    Be precise and only return one of the three options.
    """)
    
    routing_message = HumanMessage(content=f"Route this message: {latest_message}")
    response = llm.invoke([system_msg, routing_message])
    
    # Extract routing decision
    decision = response.content.strip().upper()
    
    # Ensure valid decision
    if decision not in ["TASK_MANAGEMENT", "USER_MANAGEMENT", "GENERAL"]:
        decision = "GENERAL"
    
    return {
        "context": decision, 
        "last_action": "routing"
    }


def route_decision(state: AgentState) -> str:
    """Determine which node to route to based on context"""
    context = state.get("context", "")
    
    if "TASK_MANAGEMENT" in context:
        return "task_management"
    elif "USER_MANAGEMENT" in context:
        return "user_management"
    else:
        return "general"
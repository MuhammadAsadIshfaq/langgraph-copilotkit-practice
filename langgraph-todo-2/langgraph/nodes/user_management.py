"""
User management node for Todo Agent
"""

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from ..tools.user_tools import get_user_tools
from ..config import get_config
from .router import AgentState


def user_management_node(state: AgentState) -> dict:
    """Node for handling user-related operations"""
    
    config = get_config()
    
    # Get user management tools
    tools = get_user_tools()
    
    # Initialize LLM with Groq
    llm = ChatGroq(
        model=config.groq_model,
        temperature=config.temperature,
        groq_api_key=config.groq_api_key
    )
    
    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(tools)
    
    # Get the latest messages
    messages = state["messages"]
    
    # Add system message for user management context
    system_msg = SystemMessage(content="""
    You are a user management assistant. You help create and manage users in the todo system efficiently.
    
    Available operations:
    - Create new users with name and email (both required)
    - List all existing users with their details
    - Get detailed information about specific users
    - Delete users (only if they have no assigned tasks)
    
    Guidelines:
    - Always validate that required information (name and email) is provided
    - Check for duplicate email addresses before creating users
    - Provide clear feedback about operations performed
    - Use emojis to make responses more engaging (✅ for success, ❌ for errors, ℹ️ for info)
    - When listing users, show their ID, name, and email clearly
    - If someone tries to delete a user with assigned tasks, explain why it's not allowed
    - Be helpful and suggest alternatives when operations can't be completed
    
    Email validation:
    - Must contain @ symbol
    - Must have a domain part after @
    - Basic format validation only
    
    Remember:
    - User IDs are generated automatically (user_1, user_2, etc.)
    - Email addresses must be unique in the system
    - Users with assigned tasks cannot be deleted
    - Always use the exact IDs provided by the system
    """)
    
    # Invoke LLM with tools
    response = llm_with_tools.invoke([system_msg] + messages)
    
    return {
        "messages": [response], 
        "last_action": "user_management"
    }
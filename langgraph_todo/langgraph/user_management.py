import os
"""
User Management Node and Tools
"""
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from state import AgentState, User


@tool
def create_user(name: str, email: str, role: str = "user") -> Dict[str, Any]:
    """
    Create a new user.
    
    Args:
        name: User's full name
        email: User's email address
        role: User's role (admin, user, viewer)
    
    Returns:
        Dictionary with user creation result
    """
    user_id = str(uuid.uuid4())
    user: User = {
        "id": user_id,
        "name": name,
        "email": email,
        "role": role,
        "created_at": datetime.now().isoformat(),
        "active": True
    }
    
    return {
        "success": True,
        "user": user,
        "message": f"User '{name}' created successfully with ID: {user_id}"
    }


@tool
def get_user(user_id: str, users: Dict[str, User]) -> Dict[str, Any]:
    """
    Get user by ID.
    
    Args:
        user_id: The user ID to retrieve
        users: Dictionary of users
    
    Returns:
        Dictionary with user data or error
    """
    if user_id in users:
        return {
            "success": True,
            "user": users[user_id],
            "message": f"User found: {users[user_id]['name']}"
        }
    else:
        return {
            "success": False,
            "user": None,
            "message": f"User with ID '{user_id}' not found"
        }


@tool
def list_users(users: Dict[str, User], active_only: bool = True) -> Dict[str, Any]:
    """
    List all users.
    
    Args:
        users: Dictionary of users
        active_only: If True, only return active users
    
    Returns:
        Dictionary with list of users
    """
    user_list = []
    for user in users.values():
        if not active_only or user.get("active", True):
            user_list.append(user)
    
    return {
        "success": True,
        "users": user_list,
        "count": len(user_list),
        "message": f"Found {len(user_list)} users"
    }


@tool
def update_user(user_id: str, users: Dict[str, User], **kwargs) -> Dict[str, Any]:
    """
    Update user information.
    
    Args:
        user_id: The user ID to update
        users: Dictionary of users
        **kwargs: Fields to update (name, email, role, active)
    
    Returns:
        Dictionary with update result
    """
    if user_id not in users:
        return {
            "success": False,
            "message": f"User with ID '{user_id}' not found"
        }
    
    user = users[user_id]
    updated_fields = []
    
    for field, value in kwargs.items():
        if field in ["name", "email", "role", "active"] and value is not None:
            user[field] = value
            updated_fields.append(field)
    
    return {
        "success": True,
        "user": user,
        "updated_fields": updated_fields,
        "message": f"User '{user['name']}' updated successfully"
    }


@tool
def deactivate_user(user_id: str, users: Dict[str, User]) -> Dict[str, Any]:
    """
    Deactivate a user.
    
    Args:
        user_id: The user ID to deactivate
        users: Dictionary of users
    
    Returns:
        Dictionary with deactivation result
    """
    if user_id not in users:
        return {
            "success": False,
            "message": f"User with ID '{user_id}' not found"
        }
    
    users[user_id]["active"] = False
    return {
        "success": True,
        "user": users[user_id],
        "message": f"User '{users[user_id]['name']}' deactivated successfully"
    }


# User management tools list
user_tools = [
    create_user,
    get_user,
    list_users,
    update_user,
    deactivate_user
]


def user_management_node(state: AgentState) -> AgentState:
    """
    Node for handling user management operations.
    """
    llm = ChatGroq(model="deepseek-r1-distill-llama-70b", temperature=0.7,api_key=os.environ.get("GROQ_API_KEY"))
    llm_with_tools = llm.bind_tools(user_tools)
    
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
            if tool_name == "create_user":
                result = create_user.invoke(tool_args)
                if result["success"]:
                    # Add user to state
                    user = result["user"]
                    state["users"][user["id"]] = user
                    
            elif tool_name == "get_user":
                tool_args["users"] = state["users"]
                result = get_user.invoke(tool_args)
                
            elif tool_name == "list_users":
                tool_args["users"] = state["users"]
                result = list_users.invoke(tool_args)
                
            elif tool_name == "update_user":
                tool_args["users"] = state["users"]
                result = update_user.invoke(tool_args)
                
            elif tool_name == "deactivate_user":
                tool_args["users"] = state["users"]
                result = deactivate_user.invoke(tool_args)
            
            # Store operation result
            state["last_operation"] = tool_name
            state["operation_result"] = result
    else:
        # No tool calls, just a regular response
        state["operation_result"] = {
            "success": False,
            "message": "I understand you want to work with users, but I need more specific information. Try: 'Create a user named John with email john@example.com'"
        }
        state["last_operation"] = "user_chat"
    
    return state
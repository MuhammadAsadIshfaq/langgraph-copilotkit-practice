from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langchain.tools import tool
from state import TodoState, User
import uuid

class UserNodeInput(TypedDict):
    messages: list[BaseMessage]
    state: TodoState

def create_user_tool(state: TodoState) -> None:
    """Create a new user in the system."""
    @tool
    def create_user(name: str, email: str) -> str:
        """Create a new user with the given name and email."""
        user_id = str(uuid.uuid4())
        user = User(id=user_id, name=name, email=email)
        state.users[user_id] = user
        return f"User created successfully with ID: {user_id}"
    
    return create_user

def user_node(state: TodoState, messages: list[BaseMessage]) -> dict:
    """Node for handling user-related operations."""
    llm = ChatGroq(temperature=0)
    
    # Create tools
    tools = [create_user_tool(state)]
    
    # Process the message with the LLM
    response = llm.invoke(messages, tools=tools)
    
    # Update state with the response
    state.messages.append({"role": "assistant", "content": response.content})
    
    return {"state": state} 
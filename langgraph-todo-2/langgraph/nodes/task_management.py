"""
Task management node for Todo Agent
"""

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from ..tools.task_tools import get_task_tools
from ..config import get_config
from .router import AgentState


def task_management_node(state: AgentState) -> dict:
    """Node for handling task-related operations"""
    
    config = get_config()
    
    # Get task management tools
    tools = get_task_tools()
    
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
    
    # Add system message for task management context
    system_msg = SystemMessage(content="""
    You are a task management assistant. You help users create, update, delete, and assign tasks efficiently.
    
    Available operations:
    - Create tasks with title and description
    - Update task status (pending, in_progress, completed)
    - Delete tasks from the system
    - Assign tasks to users (verify user exists first)
    - Reassign tasks to different users
    - List all tasks with status and assignment info
    - Get detailed information about specific tasks
    
    Guidelines:
    - Always validate that users exist before assigning tasks
    - Provide clear feedback about operations performed
    - Use emojis to make responses more engaging (✅ for success, ❌ for errors, ℹ️ for info)
    - When listing tasks, group them by status for better readability
    - If a user tries to assign a task but no users exist, suggest creating a user first
    - Be helpful and proactive in suggesting next steps
    
    Remember:
    - Task IDs are generated automatically (task_1, task_2, etc.)
    - User IDs are generated automatically (user_1, user_2, etc.)
    - Always use the exact IDs provided by the system
    """)
    
    # Invoke LLM with tools
    response = llm_with_tools.invoke([system_msg] + messages)
    
    return {
        "messages": [response], 
        "last_action": "task_management"
    }
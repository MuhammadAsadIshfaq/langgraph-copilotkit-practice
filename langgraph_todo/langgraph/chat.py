import os
"""
Chat Node for general conversation and routing
"""
from typing import Dict, Any
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from state import AgentState


def determine_intent(message: str) -> str:
    """
    Determine the intent of the user message.
    
    Args:
        message: User's message
    
    Returns:
        Intent category
    """
    message_lower = message.lower()
    
    # Task-related keywords
    task_keywords = [
        "task", "todo", "create task", "new task", "add task", "update task",
        "delete task", "complete task", "finish task", "assign task", "task list",
        "show tasks", "my tasks", "pending tasks", "completed tasks"
    ]
    
    # User-related keywords
    user_keywords = [
        "user", "create user", "new user", "add user", "user list", "show users",
        "update user", "delete user", "deactivate user", "assign to"
    ]
    
    # Check for task-related intent
    for keyword in task_keywords:
        if keyword in message_lower:
            return "task_management"
    
    # Check for user-related intent
    for keyword in user_keywords:
        if keyword in message_lower:
            return "user_management"
    
    # Default to general chat
    return "chat"


def chat_node(state: AgentState) -> AgentState:
    """
    Node for handling general chat and routing to appropriate nodes.
    """
    # Initialize LLM
    llm = ChatGroq(model="deepseek-r1-distill-llama-70b", temperature=0.7,api_key=os.environ.get("GROQ_API_KEY"))
    
    # Get the last message
    last_message = state["messages"][-1] if state["messages"] else None
    
    # Check if this is a fresh user message that needs routing
    if isinstance(last_message, HumanMessage) and not state.get("next_action"):
        # Determine intent
        intent = determine_intent(last_message.content)
        
        if intent in ["task_management", "user_management"]:
            # Set next action for routing
            state["next_action"] = intent
            return state
    
    # Handle chat responses and status updates
    # Create context-aware prompt
    system_prompt = """You are a helpful Todo Task Management Assistant. You can help users with:

1. Task Management:
   - Create, update, delete tasks
   - Assign tasks to users
   - Mark tasks as complete
   - List and filter tasks

2. User Management:
   - Create and manage users
   - Assign tasks to users
   - List users

3. General Chat:
   - Answer questions about the system
   - Provide help and guidance

Current State:
- Total Tasks: {task_count}
- Total Users: {user_count}
- Current User: {current_user}

Be helpful, concise, and ask clarifying questions when needed."""

    # Fill in current state information
    task_count = len(state["tasks"])
    user_count = len(state["users"])
    current_user = state.get("current_user", "Not set")
    
    formatted_prompt = system_prompt.format(
        task_count=task_count,
        user_count=user_count,
        current_user=current_user
    )
    
    # Create chat prompt template
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", formatted_prompt),
        ("human", "{input}")
    ])
    
    # Generate appropriate response
    if state.get("operation_result"):
        # We have an operation result to report
        result = state["operation_result"]
        response_content = result.get("message", "Operation completed.")
        
        # Add additional context if successful operation
        if result.get("success"):
            if state.get("last_operation") == "create_user" and "user" in result:
                user = result["user"]
                response_content += f"\n\nUser Details:\n- Name: {user['name']}\n- Email: {user['email']}\n- Role: {user['role']}\n- ID: {user['id']}"
            elif state.get("last_operation") == "create_task" and "task" in result:
                task = result["task"]
                response_content += f"\n\nTask Details:\n- Title: {task['title']}\n- Priority: {task['priority']}\n- Status: {task['status']}\n- ID: {task['id']}"
            elif state.get("last_operation") == "list_users" and "users" in result:
                users = result["users"]
                if users:
                    response_content += f"\n\nUsers ({len(users)}):"
                    for user in users[:5]:  # Show first 5
                        response_content += f"\n- {user['name']} ({user['email']}) - {user['role']}"
                    if len(users) > 5:
                        response_content += f"\n... and {len(users) - 5} more"
            elif state.get("last_operation") == "list_tasks" and "tasks" in result:
                tasks = result["tasks"]
                if tasks:
                    response_content += f"\n\nTasks ({len(tasks)}):"
                    for task in tasks[:5]:  # Show first 5
                        assigned = f" (assigned to: {task['assigned_to']})" if task.get('assigned_to') else ""
                        response_content += f"\n- {task['title']} - {task['status']} - {task['priority']}{assigned}"
                    if len(tasks) > 5:
                        response_content += f"\n... and {len(tasks) - 5} more"
        
        response = AIMessage(content=response_content)
        state["messages"].append(response)
        
        # Clear operation result
        state["operation_result"] = None
        state["last_operation"] = None
        
    elif isinstance(last_message, HumanMessage):
        # Generate response for general chat
        chain = chat_prompt | llm
        response = chain.invoke({"input": last_message.content})
        state["messages"].append(response)
    
    # Check if conversation should end
    if last_message and hasattr(last_message, 'content'):
        content = last_message.content.lower()
        stop_phrases = [
            "goodbye", "bye", "exit", "quit", "stop", "end",
            "thank you, that's all", "that's everything", "done"
        ]
        
        if any(phrase in content for phrase in stop_phrases):
            state["next_action"] = "end"
    
    return state


def format_task_summary(tasks: Dict[str, Any]) -> str:
    """Format a summary of tasks."""
    if not tasks:
        return "No tasks found."
    
    total = len(tasks)
    by_status = {}
    by_priority = {}
    
    for task in tasks.values():
        status = task.get("status", "unknown")
        priority = task.get("priority", "unknown")
        
        by_status[status] = by_status.get(status, 0) + 1
        by_priority[priority] = by_priority.get(priority, 0) + 1
    
    summary = f"Total Tasks: {total}\n"
    summary += "By Status: " + ", ".join([f"{k}: {v}" for k, v in by_status.items()]) + "\n"
    summary += "By Priority: " + ", ".join([f"{k}: {v}" for k, v in by_priority.items()])
    
    return summary


def format_user_summary(users: Dict[str, Any]) -> str:
    """Format a summary of users."""
    if not users:
        return "No users found."
    
    total = len(users)
    active = sum(1 for user in users.values() if user.get("active", True))
    by_role = {}
    
    for user in users.values():
        role = user.get("role", "unknown")
        by_role[role] = by_role.get(role, 0) + 1
    
    summary = f"Total Users: {total} (Active: {active})\n"
    summary += "By Role: " + ", ".join([f"{k}: {v}" for k, v in by_role.items()])
    
    return summary
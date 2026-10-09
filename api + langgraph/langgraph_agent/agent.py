import os
from typing import Dict, List, Optional, TypedDict, Annotated, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
import requests
import json
import re
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"  # Your FastAPI server URL

# State definition
class TodoState(TypedDict):
    messages: Annotated[list, add_messages]
    user_input: str
    api_response: Optional[Dict]
    formatted_response: str
    selected_tools: List[str]
    error: Optional[str]
    is_greeting: bool  # New field to track if it's a greeting

# Initialize LLM
def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=0,
        api_key=os.environ.get("GROQ_API_KEY")
    )

# Tool definitions for your API endpoints
@tool
def get_all_users() -> str:
    """Get all users from the todo system"""
    try:
        response = requests.get(f"{API_BASE_URL}/users")
        response.raise_for_status()
        users = response.json()
        return json.dumps(users, indent=2)
    except Exception as e:
        return f"Error fetching users: {str(e)}"

@tool
def get_user_by_id(user_id: str) -> str:
    """Get a specific user by their ID"""
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        response.raise_for_status()
        user = response.json()
        return json.dumps(user, indent=2)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"User with ID {user_id} not found"
        return f"Error fetching user: {str(e)}"
    except Exception as e:
        return f"Error fetching user: {str(e)}"

@tool
def get_user_tasks(user_id: str) -> str:
    """Get all tasks assigned to a specific user"""
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}/tasks")
        response.raise_for_status()
        tasks = response.json()
        return json.dumps(tasks, indent=2)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"User with ID {user_id} not found"
        return f"Error fetching user tasks: {str(e)}"
    except Exception as e:
        return f"Error fetching user tasks: {str(e)}"

@tool
def get_users_with_tasks() -> str:
    """Get all users with their assigned tasks"""
    try:
        response = requests.get(f"{API_BASE_URL}/users-with-tasks")
        response.raise_for_status()
        users_with_tasks = response.json()
        return json.dumps(users_with_tasks, indent=2)
    except Exception as e:
        return f"Error fetching users with tasks: {str(e)}"

@tool
def get_all_tasks(status: str = None, priority: str = None) -> str:
    """Get all tasks with optional filtering by status and priority"""
    try:
        params = {}
        if status:
            params['status'] = status
        if priority:
            params['priority'] = priority
            
        response = requests.get(f"{API_BASE_URL}/tasks", params=params)
        response.raise_for_status()
        tasks = response.json()
        return json.dumps(tasks, indent=2)
    except Exception as e:
        return f"Error fetching tasks: {str(e)}"

@tool
def get_task_by_id(task_id: str) -> str:
    """Get a specific task by its ID"""
    try:
        response = requests.get(f"{API_BASE_URL}/tasks/{task_id}")
        response.raise_for_status()
        task = response.json()
        return json.dumps(task, indent=2)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Task with ID {task_id} not found"
        return f"Error fetching task: {str(e)}"
    except Exception as e:
        return f"Error fetching task: {str(e)}"

@tool
def get_tasks_with_assignees() -> str:
    """Get all tasks with their assigned users"""
    try:
        response = requests.get(f"{API_BASE_URL}/tasks-with-assignees")
        response.raise_for_status()
        tasks_with_assignees = response.json()
        return json.dumps(tasks_with_assignees, indent=2)
    except Exception as e:
        return f"Error fetching tasks with assignees: {str(e)}"

@tool
def get_tasks_by_status(status: str) -> str:
    """Get tasks by status (TODO, IN_PROGRESS, DONE)"""
    try:
        response = requests.get(f"{API_BASE_URL}/tasks/status/{status}")
        response.raise_for_status()
        tasks = response.json()
        return json.dumps(tasks, indent=2)
    except Exception as e:
        return f"Error fetching tasks by status: {str(e)}"

@tool
def get_tasks_by_priority(priority: str) -> str:
    """Get tasks by priority (LOW, MEDIUM, HIGH)"""
    try:
        response = requests.get(f"{API_BASE_URL}/tasks/priority/{priority}")
        response.raise_for_status()
        tasks = response.json()
        return json.dumps(tasks, indent=2)
    except Exception as e:
        return f"Error fetching tasks by priority: {str(e)}"

# Available tools
AVAILABLE_TOOLS = {
    "get_all_users": get_all_users,
    "get_user_by_id": get_user_by_id,
    "get_user_tasks": get_user_tasks,
    "get_users_with_tasks": get_users_with_tasks,
    "get_all_tasks": get_all_tasks,
    "get_task_by_id": get_task_by_id,
    "get_tasks_with_assignees": get_tasks_with_assignees,
    "get_tasks_by_status": get_tasks_by_status,
    "get_tasks_by_priority": get_tasks_by_priority,
}

def initialize_state() -> TodoState:
    return TodoState(
        messages=[],
        user_input="",
        api_response=None,
        formatted_response="",
        selected_tools=[],
        error=None,
        is_greeting=False
    )

# Helper function to detect greetings and casual conversation
def is_greeting_or_casual(user_input: str) -> bool:
    """Check if user input is a greeting or casual conversation"""
    casual_patterns = [
        r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
        r'\b(how are you|what\'s up|wassup)\b',
        r'\b(thanks|thank you|bye|goodbye|see you)\b',
        r'^\s*hi\s*$',
        r'^\s*hello\s*$',
        r'^\s*hey\s*$',
    ]
    
    user_input_lower = user_input.lower().strip()
    
    # Check if it matches any casual pattern
    for pattern in casual_patterns:
        if re.search(pattern, user_input_lower, re.IGNORECASE):
            return True
    
    # Check if it's a very short input (likely casual)
    if len(user_input_lower.split()) <= 2 and not any(keyword in user_input_lower for keyword in 
        ['user', 'task', 'todo', 'show', 'get', 'find', 'list', 'status', 'priority']):
        return True
    
    return False

# Node: Analyze user request and select appropriate tools
def analyze_request_node(state: TodoState) -> TodoState:
    """Use LLM to analyze user request and determine which API tools to call"""
    
    user_input = state["user_input"].strip()
    print("USer input is: ",user_input)
    
    # Check if it's a greeting or casual conversation
    if is_greeting_or_casual(user_input):
        state["is_greeting"] = True
        state["selected_tools"] = []
        state["error"] = None
        print(f"DEBUG: Detected greeting: {user_input}")  # Debug print
        print("Analyze request node state is:",state)
        return state
    
    # Reset greeting flag for non-greetings
    state["is_greeting"] = False
    
    llm = get_llm()
    
    tools_description = """
    Available API tools:
    1. get_all_users() - Get list of all users
    2. get_user_by_id(user_id) - Get specific user details
    3. get_user_tasks(user_id) - Get tasks assigned to a user
    4. get_users_with_tasks() - Get all users with their tasks
    5. get_all_tasks(status=None, priority=None) - Get tasks with optional filters
    6. get_task_by_id(task_id) - Get specific task details
    7. get_tasks_with_assignees() - Get all tasks with assignee info
    8. get_tasks_by_status(status) - Get tasks by status (TODO, IN_PROGRESS, DONE)
    9. get_tasks_by_priority(priority) - Get tasks by priority (LOW, MEDIUM, HIGH)
    """
    
    system_prompt = f"""
    You are an API assistant for a todo management system. Based on the user's request, determine which API tools to call and what parameters to use.
    
    {tools_description}
    
    Respond with a JSON object containing:
    {{
        "tools_to_call": [
            {{
                "tool_name": "function_name",
                "parameters": {{"param1": "value1", "param2": "value2"}}
            }}
        ],
        "explanation": "Brief explanation of what you're going to do"
    }}
    
    Examples:
    - "Show me all users" -> {{"tools_to_call": [{{"tool_name": "get_all_users", "parameters": {{}}}}], "explanation": "Fetching all users"}}
    - "Get high priority tasks" -> {{"tools_to_call": [{{"tool_name": "get_tasks_by_priority", "parameters": {{"priority": "HIGH"}}}}], "explanation": "Fetching high priority tasks"}}
    - "Show user 123's tasks" -> {{"tools_to_call": [{{"tool_name": "get_user_tasks", "parameters": {{"user_id": "123"}}}}], "explanation": "Getting tasks for user 123"}}
    
    Return ONLY the JSON, no other text.
    """
    
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = llm.invoke(messages)
        print("reponse of analyze request node",response)
        analysis = json.loads(response.content.strip())
        
        state["selected_tools"] = analysis.get("tools_to_call", [])
        state["error"] = None
        
    except Exception as e:
        state["error"] = f"Failed to analyze request: {str(e)}"
        state["selected_tools"] = []
    print("Analyze requeest node end state is",state)
    return state

# Node: Handle greetings and casual conversation
def handle_greeting_node(state: TodoState) -> TodoState:
    """Handle greetings and casual conversation with LLM"""
    
    llm = get_llm()
    
    system_prompt = """
    You are a friendly assistant for a todo management system. The user has sent a greeting or casual message.
    Respond warmly and offer help with the todo system. 
    
    You can help users with:
    - Viewing all users
    - Getting user details and their tasks
    - Viewing all tasks with filtering options
    - Checking task status and priority
    - Getting specific task details
    
    Keep your response friendly, brief, and helpful.
    """
    
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=state["user_input"])
        ]
        
        response = llm.invoke(messages)
        state["formatted_response"] = f"🤖 {response.content}\n\n💡 **Try asking me:**\n• 'Show me all users'\n• 'Get all tasks'\n• 'Show high priority tasks'\n• 'Get tasks with status TODO'"
        
    except Exception as e:
        # Fallback greeting response
        state["formatted_response"] = """🤖 Hello! I'm your Todo API assistant. 

I can help you manage your tasks and users. Here are some things you can ask me:

💡 **Available Commands:**
• "Show me all users"
• "Get all tasks" 
• "Show high priority tasks"
• "Get tasks with status TODO"
• "Show user 123's tasks"
• "Get task details for task 456"
• "Show all users with their tasks"

What would you like to do? 😊"""
    
    return state

# Node: Execute API calls
def execute_api_calls_node(state: TodoState) -> TodoState:
    """Execute the selected API calls"""
    
    if state.get("error") or not state["selected_tools"]:
        return state
    
    results = []
    
    for tool_call in state["selected_tools"]:
        tool_name = tool_call.get("tool_name")
        parameters = tool_call.get("parameters", {})
        
        if tool_name in AVAILABLE_TOOLS:
            try:
                tool_func = AVAILABLE_TOOLS[tool_name]
                
                # Call the tool with parameters
                if parameters:
                    result = tool_func.invoke(parameters)
                else:
                    result = tool_func.invoke({})
                
                results.append({
                    "tool": tool_name,
                    "parameters": parameters,
                    "result": result
                })
                
            except Exception as e:
                results.append({
                    "tool": tool_name,
                    "parameters": parameters,
                    "error": str(e)
                })
        else:
            results.append({
                "tool": tool_name,
                "error": f"Tool {tool_name} not found"
            })
    
    state["api_response"] = {"results": results}
    return state

# Node: Format response using LLM
def format_response_node(state: TodoState) -> TodoState:
    """Use LLM to format the API response into a user-friendly format"""
    
    if state.get("error"):
        state["formatted_response"] = f"❌ Error: {state['error']}"
        return state
    
    if not state.get("api_response"):
        state["formatted_response"] = "❌ No data received from API"
        return state
    
    llm = get_llm()
    
    system_prompt = """
    You are formatting API responses for a todo management system. 
    Take the raw API data and format it into a clean, user-friendly response with:
    - Clear headings and sections
    - Emojis for visual appeal
    - Proper formatting for lists and data
    - Summary statistics when relevant
    - Highlight important information
    
    Make it conversational and helpful.
    """
    
    api_data = json.dumps(state["api_response"], indent=2)
    user_request = state["user_input"]
    
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User asked: '{user_request}'\n\nAPI Response:\n{api_data}")
        ]
        
        response = llm.invoke(messages)
        state["formatted_response"] = response.content
        
    except Exception as e:
        # Fallback formatting
        results = state["api_response"]["results"]
        formatted = f"📋 **Results for:** {user_request}\n\n"
        
        for i, result in enumerate(results, 1):
            formatted += f"**{i}. {result['tool']}**\n"
            if "error" in result:
                formatted += f"❌ Error: {result['error']}\n"
            else:
                # Try to parse and format JSON
                try:
                    data = json.loads(result['result'])
                    if isinstance(data, list):
                        formatted += f"📊 Found {len(data)} items\n"
                        for item in data[:3]:  # Show first 3 items
                            if isinstance(item, dict):
                                name = item.get('name', item.get('title', 'Item'))
                                formatted += f"  • {name}\n"
                    else:
                        formatted += f"✅ Data retrieved successfully\n"
                except:
                    formatted += f"✅ {result['result'][:100]}...\n"
            formatted += "\n"
        
        state["formatted_response"] = formatted
    print("state of formated response is:",state)
    
    return state

# Node: Handle errors
def handle_error_node(state: TodoState) -> TodoState:
    """Handle errors and provide helpful suggestions"""
    error_msg = state.get("error", "Unknown error occurred")
    
    suggestions = """
    💡 **Try these commands:**
    • "Show me all users"
    • "Get all tasks"
    • "Show high priority tasks"
    • "Get tasks with status TODO"
    • "Show user 123's tasks"
    • "Get task details for task 456"
    • "Show all users with their tasks"
    """
    
    state["formatted_response"] = f"❌ **Error:** {error_msg}\n\n{suggestions}"
    return state

# Router function
def route_execution(state: TodoState) -> str:
    """Route to appropriate execution path"""
    # Check for greeting first (highest priority)
    if state.get("is_greeting"):
        return "handle_greeting"
    
    # Check for errors
    if state.get("error"):
        return "handle_error"
    
    # Check if we have tools to execute
    if not state.get("selected_tools") or len(state.get("selected_tools", [])) == 0:
        return "handle_error"
    
    return "execute_api"
from langgraph.checkpoint.memory import MemorySaver

# Create the graph
def create_todo_api_graph():
    graph = StateGraph(TodoState)
    
    # Add nodes
    graph.add_node("analyze_request", analyze_request_node)
    graph.add_node("handle_greeting", handle_greeting_node)
    graph.add_node("execute_api", execute_api_calls_node)
    graph.add_node("format_response", format_response_node)
    graph.add_node("handle_error", handle_error_node)
    
    # Set entry point
    graph.add_edge("__start__", "analyze_request")
    
    # Add conditional routing
    graph.add_conditional_edges(
        "analyze_request",
        route_execution,
        {
            "handle_greeting": "handle_greeting",
            "execute_api": "execute_api",
            "handle_error": "handle_error"
        }
    )
    
    # Connect execution flow
    graph.add_edge("execute_api", "format_response")
    
    # End nodes
    graph.add_edge("format_response", END)
    graph.add_edge("handle_greeting", END)
    graph.add_edge("handle_error", END)
    memory = MemorySaver()
    graph2 = graph.compile(checkpointer=memory)    
    return graph2

# Main application class
class TodoApiAgent:
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        global API_BASE_URL
        API_BASE_URL = api_base_url
        self.graph = create_todo_api_graph()
        self.state = initialize_state()
    
    def query(self, user_input: str) -> str:
        """Process a user query using the API"""
        self.state["user_input"] = user_input
        
        # Run the graph
        result = self.graph.invoke(self.state)
        
        # Update state
        self.state = result
        
        return result["formatted_response"]
    
    def health_check(self) -> bool:
        """Check if the API is accessible"""
        try:
            response = requests.get(f"{API_BASE_URL}/")
            return response.status_code == 200
        except:
            return False

# Demo usage
if __name__ == "__main__":
    print("🚀 LangGraph Todo API Agent")
    print("=" * 50)
    
    # Create agent
    agent = TodoApiAgent()
    
    # Check API health
    if not agent.health_check():
        print("⚠️  Warning: Cannot connect to API at http://localhost:8000")
        print("Make sure your FastAPI server is running!")
        print("\nTo run your FastAPI server:")
        print("uvicorn main:app --reload")
        print("\n" + "="*50)
    
    # Interactive mode
    print("\n" + "="*50)
    print("💡 Interactive Mode - Type 'quit' to exit")
    print("Example queries:")
    print("  • 'Hi' or 'Hello' (casual greetings)")
    print("  • 'Show me all users'")
    print("  • 'Get high priority tasks'")
    print("  • 'Show tasks with status TODO'")
    print("  • 'Get user 123 tasks'")
    print("="*50)
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if user_input:
                result = agent.query(user_input)
                print(f"🤖 Agent: {result}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
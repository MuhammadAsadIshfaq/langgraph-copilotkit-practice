"""
Main entry point for the Todo Task Management AI Agent.
It defines the workflow graph and the entry point for the agent.
"""
import os
from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Import all the components
from state import AgentState
from user_management import user_management_node
from task_management import task_management_node
from chat import chat_node
from router import route_to_next_node


def initialize_agent_state() -> AgentState:
    """
    Initialize the agent state with default values.
    
    Returns:
        Initialized AgentState
    """
    return AgentState(
        messages=[],
        tasks={},
        users={},
        current_user=None,
        last_operation=None,
        operation_result=None,
        error_message=None,
        next_action=None
    )


def create_todo_agent() -> StateGraph:
    """
    Create and configure the Todo Task Management Agent graph.
    
    Returns:
        Compiled StateGraph for the agent
    """
    # Define the workflow graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("chat", chat_node)
    workflow.add_node("task_management", task_management_node)
    workflow.add_node("user_management", user_management_node)
    
    # Set entry point
    workflow.set_entry_point("chat")
    
    # Add edges with proper conditional routing
    workflow.add_conditional_edges(
        "chat",
        route_to_next_node,
        {
            "task_management": "task_management",
            "user_management": "user_management", 
            "chat": "chat",
            "end": END
        }
    )
    
    # Add edges back to chat after operations
    workflow.add_edge("task_management", "chat")
    workflow.add_edge("user_management", "chat")
    
    # Compile the graph
    compile_kwargs = {}
    
    # Check if we're running in LangGraph API mode
    if os.environ.get("LANGGRAPH_API", "false").lower() == "true":
        # When running in LangGraph API, don't use a custom checkpointer
        graph = workflow.compile(**compile_kwargs)
    else:
        # For other contexts, use MemorySaver
        memory = MemorySaver()
        compile_kwargs["checkpointer"] = memory
        graph = workflow.compile(checkpointer=memory)
    
    return graph


def run_agent_conversation(graph: StateGraph, user_input: str, state: AgentState = None) -> AgentState:
    """
    Run a single conversation turn with the agent.
    
    Args:
        graph: The compiled agent graph
        user_input: User's input message
        state: Current agent state (optional)
    
    Returns:
        Updated agent state
    """
    if state is None:
        state = initialize_agent_state()
    
    # Add user message to state
    user_message = HumanMessage(content=user_input)
    state["messages"].append(user_message)
    
    # Run the graph
    config = {"configurable": {"thread_id": "todo_agent_thread"},"recursion_limit": 50}
    
    try:
        result = graph.invoke(state, config)
        return result
    except Exception as e:
        # Handle errors gracefully
        error_message = f"An error occurred: {str(e)}"
        state["error_message"] = error_message
        state["messages"].append(AIMessage(content=error_message))
        return state


# def demo_conversation():
#     """
#     Demonstration of the Todo Agent with sample conversations.
#     """
#     print("🤖 Todo Task Management Agent Demo")
#     print("=" * 50)
    
#     # Create the agent
#     graph = create_todo_agent()
#     state = initialize_agent_state()
    
#     # Demo conversations
#     demo_inputs = [
#         "Hello! I'd like to create a new user.",
#         "Create a user named John Doe with email john@example.com and role admin",
#         "Create another user named Jane Smith with email jane@example.com",
#         "Show me all users",
#         "Create a task called 'Setup project repository' with high priority",
#         "Create a task 'Write documentation' and assign it to Jane Smith",
#         "Show me all tasks",
#         "Complete the first task",
#         "List all completed tasks",
#         "Thank you, that's all!"
#     ]
    
#     for i, user_input in enumerate(demo_inputs, 1):
#         print(f"\n💬 User ({i}): {user_input}")
        
#         # Run conversation
#         state = run_agent_conversation(graph, user_input, state)
        
#         # Get the last AI message
#         if state["messages"]:
#             last_message = state["messages"][-1]
#             if isinstance(last_message, AIMessage):
#                 print(f"🤖 Agent: {last_message.content}")
        
#         # Show current stats
#         print(f"📊 Stats: {len(state['tasks'])} tasks, {len(state['users'])} users")
        
#         # Check for errors
#         if state.get("error_message"):
#             print(f"❌ Error: {state['error_message']}")
#             break


# Main execution
if __name__ == "__main__":
    # You can run the demo or create your own agent instance
    
    # Option 1: Run demo
    # demo_conversation()
    
    # Option 2: Create agent for interactive use
    graph = create_todo_agent()
    state = initialize_agent_state()
    
    print("Todo Agent is ready! Start chatting...")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
        
        state = run_agent_conversation(graph, user_input, state)
        
        if state["messages"]:
            last_message = state["messages"][-1]
            if isinstance(last_message, AIMessage):
                print(f"Agent: {last_message.content}")


# Export the main components for external use
__all__ = [
    "create_todo_agent",
    "initialize_agent_state", 
    "run_agent_conversation",
    "AgentState"
]
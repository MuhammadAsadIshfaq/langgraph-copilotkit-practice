"""
Router Node for determining next actions
"""
from typing import Literal
from state import AgentState


def route_to_next_node(state: AgentState) -> Literal["task_management", "user_management", "chat", "end"]:
    """
    Determine the next action based on state.
    
    Args:
        state: Current agent state
    
    Returns:
        Next node to execute
    """
    # Check if there's a specific next action set
    next_action = state.get("next_action")
    
    if next_action == "task_management":
        # Clear the next action
        state["next_action"] = None
        return "task_management"
    
    elif next_action == "user_management":
        # Clear the next action
        state["next_action"] = None
        return "user_management"
    
    elif next_action == "end":
        return "end"
    
    # Default to chat for general conversation
    return "chat"


def should_continue(state: AgentState) -> Literal["router", "end"]:
    """
    Determine if the agent should continue processing or end.
    
    Args:
        state: Current agent state
    
    Returns:
        Next step - either continue routing or end
    """
    # Check if there's an error that should stop processing
    if state.get("error_message"):
        return "end"
    
    # Check if the last message indicates completion
    last_message = state["messages"][-1] if state["messages"] else None
    
    if last_message and hasattr(last_message, 'content'):
        content = last_message.content.lower()
        
        # Stop words/phrases
        stop_phrases = [
            "goodbye", "bye", "exit", "quit", "stop", "end",
            "thank you, that's all", "that's everything", "done"
        ]
        
        if any(phrase in content for phrase in stop_phrases):
            return "end"
    
    # Continue by default
    return "router"
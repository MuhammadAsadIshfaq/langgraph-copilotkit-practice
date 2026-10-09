"""
Main Todo Agent implementation using LangGraph
"""

from typing import Dict, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from ..nodes import (
    router_node, 
    route_decision,
    task_management_node,
    user_management_node,
    general_node,
    AgentState
)
from ..tools import get_task_tools, get_user_tools
from ..config import get_config
from ..memory import get_memory_instance


class TodoAgent:
    """Main Todo Agent class that encapsulates the LangGraph workflow"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Todo Agent
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = get_config()
        self.memory = get_memory_instance()
        self.app = self._build_workflow()
        
    def _build_workflow(self):
        """Build the LangGraph workflow"""
        
        # Initialize the graph with state
        workflow = StateGraph(AgentState)
        
        # Add nodes to the graph
        workflow.add_node("router", router_node)
        workflow.add_node("task_management", task_management_node)
        workflow.add_node("user_management", user_management_node)
        workflow.add_node("general", general_node)
        
        # Add tool nodes for each management type
        task_tools = get_task_tools()
        user_tools = get_user_tools()
        
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
        memory_saver = MemorySaver()
        
        # Compile the graph
        return workflow.compile(checkpointer=memory_saver)
    
    def chat(self, message: str, thread_id: Optional[str] = None) -> str:
        """Chat with the agent
        
        Args:
            message: User message
            thread_id: Optional thread ID for conversation memory
            
        Returns:
            Agent response
        """
        if not thread_id:
            thread_id = self.config.memory_thread_id
            
        # Configuration for the conversation
        config = {"configurable": {"thread_id": thread_id}}
        
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "last_action": "",
            "context": ""
        }
        
        try:
            # Run the agent
            result = self.app.invoke(initial_state, config)
            
            # Extract the response
            if result["messages"]:
                last_message = result["messages"][-1]
                if hasattr(last_message, 'content'):
                    return last_message.content
                else:
                    return str(last_message)
            else:
                return "I'm sorry, I couldn't process your request."
                
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def get_conversation_history(self, thread_id: Optional[str] = None) -> list:
        """Get conversation history for a thread
        
        Args:
            thread_id: Optional thread ID
            
        Returns:
            List of messages in the conversation
        """
        if not thread_id:
            thread_id = self.config.memory_thread_id
            
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            # Get the current state
            state = self.app.get_state(config)
            return state.values.get("messages", [])
        except Exception:
            return []
    
    def reset_conversation(self, thread_id: Optional[str] = None) -> None:
        """Reset conversation history
        
        Args:
            thread_id: Optional thread ID to reset
        """
        if not thread_id:
            thread_id = self.config.memory_thread_id
            
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            # Clear the conversation state
            self.app.update_state(config, {"messages": []})
        except Exception:
            pass
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get current system statistics
        
        Returns:
            Dictionary with system stats
        """
        return self.memory.get_stats()
    
    def export_data(self) -> Dict[str, Any]:
        """Export all data from the system
        
        Returns:
            Dictionary containing all users and tasks
        """
        return {
            "users": {uid: user.to_dict() for uid, user in self.memory.get_all_users().items()},
            "tasks": {tid: task.to_dict() for tid, task in self.memory.get_all_tasks().items()},
            "stats": self.get_system_stats()
        }
    
    def clear_all_data(self) -> None:
        """Clear all data from the system"""
        self.memory.clear_all()


def create_todo_agent(config: Optional[Dict[str, Any]] = None) -> TodoAgent:
    """Factory function to create a Todo Agent
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured TodoAgent instance
    """
    return TodoAgent(config)
import os
import uuid
from typing import cast
from langgraph.graph import StateGraph, END
from state import TodoState
from nodes.user_node import user_node
from nodes.task_node import task_node

# Define the workflow graph
workflow = StateGraph(TodoState)

# Add nodes
workflow.add_node("user_operations", user_node)
workflow.add_node("task_operations", task_node)

# Set entry point
workflow.set_entry_point("user_operations")

# Add edges
workflow.add_edge("user_operations", "task_operations")
workflow.add_edge("task_operations", END)

# Compile the graph
compile_kwargs = {}

# Check if we're running in LangGraph API mode
if os.environ.get("LANGGRAPH_API", "false").lower() == "true":
    graph = workflow.compile(**compile_kwargs)
else:
    from langgraph.checkpoint.memory import MemorySaver
    memory = MemorySaver()
    compile_kwargs["checkpointer"] = memory
    graph = workflow.compile(**compile_kwargs)

def run_agent(message: str, state: TodoState = None, thread_id: str = None) -> dict:
    """Run the agent with a given message and optional state."""
    if state is None:
        state = TodoState()
    if thread_id is None:
        thread_id = str(uuid.uuid4())
    # Add the user message to the state
    state.messages.append({"role": "user", "content": message})
    # Run the graph with thread_id, checkpoint_id, and checkpoint_ns for checkpointer
    result = graph.invoke({
        "state": state,
        "thread_id": thread_id,
        "checkpoint_id": thread_id,
        "checkpoint_ns": thread_id
    })
    return result["state"] 
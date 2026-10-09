from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage

def echo_agent(state, config):
    messages = state.get("messages", [])
    user_input = messages[-1].content
    reply = AIMessage(content=f"Agent says: {user_input}")
    messages.append(reply)
    return {"messages": messages}

graph = StateGraph()
graph.add_node("echo", echo_agent)
graph.set_entry_point("echo")
graph.set_finish_point("echo")
compiled_graph = graph.compile()

def run_agent(user_message):
    initial_state = {"messages": [HumanMessage(content=user_message)]}
    result = compiled_graph.invoke(initial_state)
    return result["messages"][-1].content

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

@tool
def add_todo(text: str) -> str:
    """Add a new todo item."""
    return f"Added todo: {text}"

@tool
def list_todos() -> str:
    """List all todos."""
    return "Here are your todos"

def create_todo_agent():
    tools = [add_todo, list_todos]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful todo assistant. You can add and list todos."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    llm = ChatOpenAI(temperature=0)
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

# Example usage
if __name__ == "__main__":
    agent = create_todo_agent()
    response = agent.invoke({"input": "Add a todo to buy groceries"})
    print(response) 
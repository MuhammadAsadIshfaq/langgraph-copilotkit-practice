"""
Model configuration for the Todo agent using Groq.
"""

import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

def get_model():
    """Initialize the Groq model."""
    api_key = os.getenv("GROQ_API_KEY")
    model = ChatGroq(
        api_key=api_key,
        model_name="mixtral-8x7b-32768"
    )
    return model

def get_prompt_template():
    """Return the base prompt template for the Todo agent."""
    system_prompt = """You are an AI Todo Assistant that helps users manage their tasks efficiently.
    You can:
    1. Create new todos with titles, descriptions, priorities, and due dates
    2. List all todos with their status
    3. Mark todos as complete or incomplete
    4. Update todo details
    5. Delete todos
    6. Provide suggestions for task organization
    7. Generate summaries of pending tasks
    
    Always be helpful, concise, and maintain a professional tone."""
    
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ]) 
"""
Model configuration for the HR Assistant using Groq.
"""

import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Initialize Groq model
def get_model():
    """
    Get the Groq model instance.
    """
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="mixtral-8x7b-32768"
    )

# HR Assistant system prompt
HR_SYSTEM_PROMPT = """You are an HR Assistant AI. Your role is to help with:
1. Candidate management
2. Interview scheduling and feedback
3. Job posting and requirements
4. Employee onboarding
5. HR policy questions

Always maintain professionalism and confidentiality.
"""

# Create the base prompt template
def get_prompt_template():
    """
    Get the base prompt template for the HR Assistant.
    """
    return ChatPromptTemplate.from_messages([
        ("system", HR_SYSTEM_PROMPT),
        ("human", "{input}")
    ]) 
"""
Configuration settings for Todo Agent
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class AgentConfig:
    """Configuration class for the Todo Agent"""
    
    # Groq API settings
    groq_api_key: str
    groq_model: str = "mixtral-8x7b-32768"
    temperature: float = 0.1
    
    # Agent settings
    max_iterations: int = 10
    verbose: bool = False
    
    # Memory settings
    enable_persistence: bool = True
    memory_thread_id: str = "todo_session"
    
    # Validation settings
    validate_email: bool = True
    allow_duplicate_emails: bool = False
    
    @classmethod
    def from_env(cls) -> 'AgentConfig':
        """Create configuration from environment variables"""
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        return cls(
            groq_api_key=groq_api_key,
            groq_model=os.getenv("GROQ_MODEL", "mixtral-8x7b-32768"),
            temperature=float(os.getenv("GROQ_TEMPERATURE", "0.1")),
            max_iterations=int(os.getenv("MAX_ITERATIONS", "10")),
            verbose=os.getenv("VERBOSE", "false").lower() == "true",
            enable_persistence=os.getenv("ENABLE_PERSISTENCE", "true").lower() == "true",
            memory_thread_id=os.getenv("MEMORY_THREAD_ID", "todo_session"),
            validate_email=os.getenv("VALIDATE_EMAIL", "true").lower() == "true",
            allow_duplicate_emails=os.getenv("ALLOW_DUPLICATE_EMAILS", "false").lower() == "true"
        )
    
    def validate(self) -> None:
        """Validate configuration settings"""
        if not self.groq_api_key:
            raise ValueError("Groq API key is required")
        
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("Temperature must be between 0 and 2")
        
        if self.max_iterations < 1:
            raise ValueError("Max iterations must be at least 1")


def get_config() -> AgentConfig:
    """Get the default configuration"""
    config = AgentConfig.from_env()
    config.validate()
    return config
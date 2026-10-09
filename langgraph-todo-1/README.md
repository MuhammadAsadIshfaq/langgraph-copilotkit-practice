# LangGraph Todo Agent

A powerful todo management agent built with LangGraph and Groq that can handle user management and task operations.

## Features

- User Management
  - Create new users
  - User authentication
- Task Management
  - Create tasks
  - Update tasks
  - Delete tasks
  - Assign tasks to users
  - Track task status

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Groq API key:
```bash
export GROQ_API_KEY=your_api_key_here
```

## Usage

```python
from agent import run_agent
from state import TodoState

# Initialize the agent
state = TodoState()

# Create a user
result = run_agent("Create a new user named John Doe with email john@example.com", state)
state = result

# Create a task
result = run_agent("Create a task 'Complete project documentation' for user {user_id}", state)
state = result

# Assign a task
result = run_agent("Assign task {task_id} to user {user_id}", state)
state = result

# Update a task
result = run_agent("Update task {task_id} status to 'completed'", state)
state = result

# Delete a task
result = run_agent("Delete task {task_id}", state)
state = result
```

## Project Structure

- `agent.py`: Main agent file with the workflow graph
- `state.py`: State management and data models
- `nodes/`: Directory containing different operation nodes
  - `user_node.py`: User management operations
  - `task_node.py`: Task management operations
- `requirements.txt`: Project dependencies

## Notes

- The agent uses Groq as the LLM provider
- State is maintained in memory by default
- The agent can be run in both LangGraph API mode and standalone mode 
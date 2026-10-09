from agent import run_agent
from state import TodoState
import uuid

def main():
    # Initialize the state
    state = TodoState()
    thread_id = str(uuid.uuid4())
    
    # Test creating a user
    print("\n1. Creating a user...")
    result = run_agent("Create a new user named John Doe with email john@example.com", state, thread_id)
    state = result
    print("User creation response:", state.messages[-1]["content"])
    
    # Get the user ID from the response
    user_id = list(state.users.keys())[0]
    
    # Test creating a task
    print("\n2. Creating a task...")
    result = run_agent(f"Create a task 'Complete project documentation' for user {user_id}", state, thread_id)
    state = result
    print("Task creation response:", state.messages[-1]["content"])
    
    # Get the task ID from the response
    task_id = list(state.tasks.keys())[0]
    
    # Test assigning the task
    print("\n3. Assigning the task...")
    result = run_agent(f"Assign task {task_id} to user {user_id}", state, thread_id)
    state = result
    print("Task assignment response:", state.messages[-1]["content"])
    
    # Test updating the task
    print("\n4. Updating the task...")
    result = run_agent(f"Update task {task_id} status to 'in_progress'", state, thread_id)
    state = result
    print("Task update response:", state.messages[-1]["content"])
    
    # Print final state
    print("\nFinal State:")
    print("Users:", {k: v.dict() for k, v in state.users.items()})
    print("Tasks:", {k: v.dict() for k, v in state.tasks.items()})

if __name__ == "__main__":
    main() 
"""
FastAPI backend for the Todo app.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from agent.nodes import create_workflow
from agent.state import TodoState, Todo

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the workflow
workflow = create_workflow().compile()

# Pydantic models for request/response
class Message(BaseModel):
    content: str

class TodoCreate(BaseModel):
    title: str
    description: str
    priority: str
    due_date: Optional[str]

class TodoUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[str]
    due_date: Optional[str]
    completed: Optional[bool]

# Routes
@app.post("/chat")
async def chat(message: Message):
    """
    Process a chat message.
    """
    try:
        state = TodoState(
            model="mixtral-8x7b-32768",
            current_task="chat",
            todos=[],
            current_todo=None,
            logs=[],
            messages=[{"role": "user", "content": message.content}]
        )
        result = workflow.invoke(state)
        return {"response": result.messages[-1].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/todos")
async def create_todo(todo: TodoCreate):
    """
    Create a new todo.
    """
    try:
        # Implementation for todo creation
        return {"status": "success", "todo": todo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/todos")
async def get_todos():
    """
    Get all todos.
    """
    try:
        # Implementation for getting todos
        return {"todos": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, todo: TodoUpdate):
    """
    Update a todo.
    """
    try:
        # Implementation for updating todo
        return {"status": "success", "todo": todo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    """
    Delete a todo.
    """
    try:
        # Implementation for deleting todo
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
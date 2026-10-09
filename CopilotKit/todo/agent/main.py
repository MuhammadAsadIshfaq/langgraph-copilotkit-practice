from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
from todo_workflow import TodoWorkflow

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize TodoWorkflow
todo_workflow = TodoWorkflow()

# Todo models
class Todo(BaseModel):
    id: int
    text: str
    completed: bool
    priority: Optional[str] = None
    estimated_time: Optional[str] = None
    subtasks: Optional[str] = None

class TodoCreate(BaseModel):
    text: str

class TodoResponse(BaseModel):
    id: int
    text: str
    completed: bool
    priority: str
    estimated_time: str
    subtasks: str

# In-memory storage
todos: List[Todo] = []
current_id = 1

# API endpoints
@app.get("/todos", response_model=List[TodoResponse])
async def get_todos():
    return todos

@app.post("/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreate):
    global current_id
    
    # Process todo through the workflow
    result = todo_workflow.process_todo(todo.text)
    
    new_todo = Todo(
        id=current_id,
        text=result["enhanced_todo"],
        completed=False,
        priority=result["priority"],
        estimated_time=result["estimated_time"],
        subtasks=result["subtasks"]
    )
    todos.append(new_todo)
    current_id += 1
    return new_todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, completed: bool):
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    global todos
    todos = [todo for todo in todos if todo.id != todo_id]
    return {"message": "Todo deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Todo(BaseModel):
    id: int
    text: str
    completed: bool = False

todos: List[Todo] = []
current_id = 1

@app.get("/todos")
async def get_todos():
    return todos

@app.post("/todos")
async def create_todo(todo: Todo):
    global current_id
    todo.id = current_id
    current_id += 1
    todos.append(todo)
    return todo

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, updated_todo: Todo):
    for todo in todos:
        if todo.id == todo_id:
            todo.text = updated_todo.text
            todo.completed = updated_todo.completed
            return todo
    return {"error": "Todo not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
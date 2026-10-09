from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User, Task
from schemas import UserBase, TaskBase, UserWithTasks, TaskWithAssignee

app = FastAPI(title="Todo API", description="Read-only API for Tasks and Users")

@app.get("/")
async def root():
    return {"message": "Hello World - Todo API"}

# User endpoints
@app.get("/users", response_model=List[UserBase])
async def get_all_users(db: Session = Depends(get_db)):
    """Get all users"""
    users = db.query(User).all()
    return users

@app.get("/users/{user_id}", response_model=UserBase)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/{user_id}/tasks", response_model=List[TaskBase])
async def get_user_tasks(user_id: str, db: Session = Depends(get_db)):
    """Get all tasks assigned to a specific user"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    tasks = db.query(Task).filter(Task.assigneeId == user_id).all()
    return tasks

@app.get("/users-with-tasks", response_model=List[UserWithTasks])
async def get_users_with_tasks(db: Session = Depends(get_db)):
    """Get all users with their assigned tasks"""
    users = db.query(User).all()
    return users

# Task endpoints
@app.get("/tasks", response_model=List[TaskBase])
async def get_all_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all tasks with optional filtering by status and priority"""
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    
    tasks = query.all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskBase)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    """Get a specific task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/tasks-with-assignees", response_model=List[TaskWithAssignee])
async def get_tasks_with_assignees(db: Session = Depends(get_db)):
    """Get all tasks with their assigned users"""
    tasks = db.query(Task).all()
    return tasks

@app.get("/tasks/status/{status}", response_model=List[TaskBase])
async def get_tasks_by_status(status: str, db: Session = Depends(get_db)):
    """Get tasks by status (TODO, IN_PROGRESS, DONE)"""
    tasks = db.query(Task).filter(Task.status == status).all()
    return tasks

@app.get("/tasks/priority/{priority}", response_model=List[TaskBase])
async def get_tasks_by_priority(priority: str, db: Session = Depends(get_db)):
    """Get tasks by priority (LOW, MEDIUM, HIGH)"""
    tasks = db.query(Task).filter(Task.priority == priority).all()
    return tasks

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
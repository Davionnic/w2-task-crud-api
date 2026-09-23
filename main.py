from fastapi import FastAPI, HTTPException
import uvicorn
from typing import Optional
from pydantic import BaseModel
from database import init_database, TaskRepository

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks with PostgreSQL",
    version="1.0"
)

# Track if database has been initialized
_db_initialized = False

def ensure_db_initialized():
    """Ensure database is initialized, call on first API request"""
    global _db_initialized
    if not _db_initialized:
        init_database()
        _db_initialized = True

# Pydantic models
class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/")
def root():
    """Root endpoint returning API information"""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    try:
        ensure_db_initialized()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": f"failed: {str(e)}"}

@app.get("/tasks")
def get_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    """Get all tasks with optional filtering by done status and title search"""
    ensure_db_initialized()
    return TaskRepository.get_all_tasks(done=done, search=search)

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get a single task by ID"""
    task = TaskRepository.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    """Create a new task"""
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")
    
    return TaskRepository.create_task(task_data.title.strip())

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    # Validate title if provided
    title = None
    if task_update.title is not None:
        if not task_update.title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        title = task_update.title.strip()
    
    task = TaskRepository.update_task(task_id, title=title, done=task_update.done)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task"""
    if not TaskRepository.delete_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.get("/stats")
def get_stats():
    """Get task statistics"""
    return TaskRepository.get_task_stats()

@app.post("/reset")
def reset_tasks():
    """Reset tasks to the original 3 seed tasks"""
    tasks = TaskRepository.reset_tasks()
    return {"message": "Tasks reset to seed data", "tasks": tasks}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
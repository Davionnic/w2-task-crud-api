from fastapi import FastAPI, HTTPException
import uvicorn
from typing import Optional
from pydantic import BaseModel
from database import task_repo, init_database

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks with SQLite persistence",
    version="1.0"
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database schema and seed data on application startup."""
    print("Initializing database...")
    init_database()
    print("Database initialized successfully.")

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
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    """Get all tasks with optional filtering by done status and title search"""
    return task_repo.get_all_tasks(done=done, search=search)

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get a single task by ID"""
    task = task_repo.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    """Create a new task"""
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")
    
    return task_repo.create_task(task_data.title)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    # Validate title if provided
    if task_update.title is not None and not task_update.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    updated_task = task_repo.update_task(
        task_id, 
        title=task_update.title, 
        done=task_update.done
    )
    
    if not updated_task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task"""
    deleted = task_repo.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.get("/stats")
def get_stats():
    """Get task statistics"""
    return task_repo.get_task_stats()

@app.post("/reset")
def reset_tasks():
    """Reset tasks to the original 3 seed tasks"""
    tasks = task_repo.reset_to_seed_data()
    return {"message": "Tasks reset to seed data", "tasks": tasks}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, HTTPException
import uvicorn
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks",
    version="1.0"
)

# In-memory storage for tasks
tasks: List[Dict[str, Any]] = []
next_id = 1

def init_seed_tasks():
    """Initialize with 3 seed tasks"""
    global next_id, tasks
    tasks = [
        {"id": 1, "title": "Learn FastAPI", "done": False},
        {"id": 2, "title": "Build CRUD API", "done": False},
        {"id": 3, "title": "Write documentation", "done": True}
    ]
    next_id = 4

# Initialize seed data
init_seed_tasks()

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
def get_tasks():
    """Get all tasks"""
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get a single task by ID"""
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    """Create a new task"""
    global next_id
    
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")
    
    new_task = {
        "id": next_id,
        "title": task_data.title.strip(),
        "done": False
    }
    tasks.append(new_task)
    next_id += 1
    
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    # Validate title if provided
    if task_update.title is not None:
        if not task_update.title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        task["title"] = task_update.title.strip()
    
    # Update done status if provided
    if task_update.done is not None:
        task["done"] = task_update.done
    
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task"""
    global tasks
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    tasks = [task for task in tasks if task["id"] != task_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
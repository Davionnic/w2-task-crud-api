from fastapi import FastAPI, HTTPException
import uvicorn
import sqlite3
import os
from typing import Optional
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks",
    version="1.0"
)

# Database configuration
DATABASE_PATH = "tasks.db"

def init_database():
    """Create SQLite database and tasks table if they don't exist, seed with 3 tasks if table is empty"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create tasks table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    
    # Check if table is empty and seed with 3 tasks if so
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    if count == 0:
        seed_tasks = [
            ("Learn FastAPI", 0),
            ("Build CRUD API", 0),
            ("Write documentation", 1)
        ]
        cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", seed_tasks)
        conn.commit()
    
    conn.close()

# In-memory storage for tasks (still used in this stage)
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Write documentation", "done": True}
]
next_id = 4

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_database()

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
    """Get all tasks from database using SELECT *"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    
    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        })
    
    conn.close()
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get a single task by ID using parameterized query"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    
    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }

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

@app.get("/stats")
def get_stats():
    """Get task statistics"""
    total = len(tasks)
    done = len([task for task in tasks if task["done"]])
    open_tasks = total - done
    
    return {
        "total": total,
        "done": done,
        "open": open_tasks
    }

@app.post("/reset")
def reset_tasks():
    """Reset tasks to the original 3 seed tasks"""
    init_seed_tasks()
    return {"message": "Tasks reset to seed data", "tasks": tasks}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
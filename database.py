"""
Database module for Task CRUD API using SQLAlchemy with SQLite.
Provides task persistence and database initialization.
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional, Dict, Any

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TaskModel(Base):
    """SQLAlchemy model for tasks table."""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False, nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert SQLAlchemy model to dictionary for API responses."""
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done
        }


class TaskRepository:
    """Repository class handling all task database operations."""
    
    def __init__(self):
        self.session_local = SessionLocal
    
    def get_session(self) -> Session:
        """Get a database session."""
        return self.session_local()
    
    def create_task(self, title: str) -> Dict[str, Any]:
        """Create a new task in the database."""
        db = self.get_session()
        try:
            task = TaskModel(title=title.strip(), done=False)
            db.add(task)
            db.commit()
            db.refresh(task)
            return task.to_dict()
        finally:
            db.close()
    
    def get_all_tasks(self, done: Optional[bool] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all tasks with optional filtering."""
        db = self.get_session()
        try:
            query = db.query(TaskModel)
            
            # Filter by done status
            if done is not None:
                query = query.filter(TaskModel.done == done)
            
            # Filter by search term in title
            if search:
                query = query.filter(TaskModel.title.ilike(f"%{search}%"))
            
            tasks = query.all()
            return [task.to_dict() for task in tasks]
        finally:
            db.close()
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a single task by ID."""
        db = self.get_session()
        try:
            task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
            return task.to_dict() if task else None
        finally:
            db.close()
    
    def update_task(self, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[Dict[str, Any]]:
        """Update an existing task."""
        db = self.get_session()
        try:
            task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
            if not task:
                return None
            
            if title is not None:
                task.title = title.strip()
            if done is not None:
                task.done = done
            
            db.commit()
            db.refresh(task)
            return task.to_dict()
        finally:
            db.close()
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted, False if not found."""
        db = self.get_session()
        try:
            task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
            if not task:
                return False
            
            db.delete(task)
            db.commit()
            return True
        finally:
            db.close()
    
    def get_task_stats(self) -> Dict[str, int]:
        """Get task statistics."""
        db = self.get_session()
        try:
            total = db.query(TaskModel).count()
            done = db.query(TaskModel).filter(TaskModel.done == True).count()
            open_tasks = total - done
            
            return {
                "total": total,
                "done": done,
                "open": open_tasks
            }
        finally:
            db.close()
    
    def reset_to_seed_data(self) -> List[Dict[str, Any]]:
        """Reset database to original seed tasks."""
        db = self.get_session()
        try:
            # Clear all existing tasks
            db.query(TaskModel).delete()
            
            # Add seed tasks
            seed_tasks = [
                TaskModel(title="Learn FastAPI", done=False),
                TaskModel(title="Build CRUD API", done=False),
                TaskModel(title="Write documentation", done=True)
            ]
            
            for task in seed_tasks:
                db.add(task)
            
            db.commit()
            
            # Refresh and return the created tasks
            for task in seed_tasks:
                db.refresh(task)
            
            return [task.to_dict() for task in seed_tasks]
        finally:
            db.close()


def init_database():
    """Initialize the database schema. Creates tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    
    # Check if we need to add seed data (if database is empty)
    repo = TaskRepository()
    db = repo.get_session()
    try:
        task_count = db.query(TaskModel).count()
        if task_count == 0:
            print("Database is empty. Adding seed data...")
            repo.reset_to_seed_data()
            print("Seed data added successfully.")
    finally:
        db.close()


# Global repository instance
task_repo = TaskRepository()
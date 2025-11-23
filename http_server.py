#!/usr/bin/env python3
"""
HTTP API Server for managing employee onboarding checklist.
FastAPI version for HTTP requests.
"""

import json
import os
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

# Constants
DATA_FILE = "data.json"
CONFIG_FILE = "config.json"

# Onboarding checklist definition
CHECKLIST = {
    1: {"day": 1, "task": "Meet your manager"},
    2: {"day": 1, "task": "Meet your buddy / mentor"},
    3: {"day": 1, "task": "Read the company handbook"},
    4: {"day": 1, "task": "Complete basic security training"},
    5: {"day": 2, "task": "Set up your development environment"},
    6: {"day": 2, "task": "Join the team stand-up meeting"},
    7: {"day": 2, "task": "Read the documentation for the main product"},
    8: {"day": 3, "task": "Shadow a team member during a real task"},
    9: {"day": 3, "task": "Pick your first small task from the backlog"},
}


# Pydantic models for request/response validation
class UserProgress(BaseModel):
    email: str
    completed_tasks: List[int]
    created_at: str
    last_updated: str
    progress_percentage: float
    total_tasks: int


class TaskCompleteRequest(BaseModel):
    email: EmailStr
    task_id: int


class MentorRequest(BaseModel):
    mentor_email: EmailStr


class AllUsersProgress(BaseModel):
    users: dict
    total_users: int


class TaskInfo(BaseModel):
    id: int
    day: int
    task: str
    completed: bool


class DetailedProgress(BaseModel):
    email: str
    completed_tasks: List[int]
    created_at: str
    last_updated: str
    progress_percentage: float
    total_tasks: int
    tasks_by_day: dict


# Data handling functions (from original server.py)
def load_json_file(filepath: str) -> dict:
    """Loads data from JSON file."""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_json_file(filepath: str, data: dict) -> None:
    """Saves data to JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_user_data() -> dict:
    """Loads user data."""
    return load_json_file(DATA_FILE)


def save_user_data(data: dict) -> None:
    """Saves user data."""
    save_json_file(DATA_FILE, data)


def load_config() -> dict:
    """Loads configuration."""
    return load_json_file(CONFIG_FILE)


def create_new_user(email: str) -> dict:
    """Creates a new user with empty progress."""
    now = datetime.now().isoformat()
    return {
        "completed_tasks": [],
        "created_at": now,
        "last_updated": now
    }


def get_user(email: str, data: dict) -> dict:
    """Gets user data or creates a new one."""
    if email not in data:
        data[email] = create_new_user(email)
        save_user_data(data)
    return data[email]


# Create FastAPI application
app = FastAPI(
    title="Onboarding Checklist API",
    description="API for managing employee onboarding checklist",
    version="1.0.0"
)

# Add CORS for browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Onboarding Checklist API",
        "version": "1.0.0",
        "endpoints": {
            "get_user_progress": "GET /api/users/{email}/progress",
            "mark_task_complete": "POST /api/users/tasks/complete",
            "get_all_users": "POST /api/admin/users",
            "get_checklist": "GET /api/checklist"
        }
    }


@app.get("/api/checklist")
async def get_checklist():
    """Get full onboarding checklist."""
    checklist_by_day = {}
    for task_id, info in CHECKLIST.items():
        day = info["day"]
        if day not in checklist_by_day:
            checklist_by_day[day] = []
        checklist_by_day[day].append({
            "id": task_id,
            "task": info["task"]
        })
    
    return {
        "checklist": checklist_by_day,
        "total_tasks": len(CHECKLIST),
        "total_days": 3
    }


@app.get("/api/users/{email}/progress", response_model=DetailedProgress)
async def get_user_progress(email: str):
    """
    Get user progress for checklist.
    If user doesn't exist - created automatically with zero progress.
    """
    data = load_user_data()
    user_data = get_user(email, data)
    
    completed = set(user_data["completed_tasks"])
    total_tasks = len(CHECKLIST)
    progress_percentage = (len(completed) / total_tasks * 100) if total_tasks > 0 else 0
    
    # Group tasks by day
    tasks_by_day = {}
    for day in [1, 2, 3]:
        tasks_by_day[f"day_{day}"] = []
        day_tasks = [tid for tid, info in CHECKLIST.items() if info["day"] == day]
        for task_id in day_tasks:
            tasks_by_day[f"day_{day}"].append({
                "id": task_id,
                "task": CHECKLIST[task_id]["task"],
                "completed": task_id in completed
            })
    
    return {
        "email": email,
        "completed_tasks": sorted(list(completed)),
        "created_at": user_data["created_at"],
        "last_updated": user_data["last_updated"],
        "progress_percentage": round(progress_percentage, 1),
        "total_tasks": total_tasks,
        "tasks_by_day": tasks_by_day
    }


@app.post("/api/users/tasks/complete")
async def mark_task_complete(request: TaskCompleteRequest):
    """
    Mark task as completed for user.
    """
    email = request.email
    task_id = request.task_id
    
    # Validate task_id
    if task_id not in CHECKLIST:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid task_id. Must be between 1 and 9. Got: {task_id}"
        )
    
    # Load data
    data = load_user_data()
    user_data = get_user(email, data)
    
    # Add task if not already completed
    was_completed = task_id in user_data["completed_tasks"]
    if not was_completed:
        user_data["completed_tasks"].append(task_id)
        user_data["completed_tasks"].sort()
        user_data["last_updated"] = datetime.now().isoformat()
        save_user_data(data)
    
    completed = set(user_data["completed_tasks"])
    progress_percentage = (len(completed) / len(CHECKLIST) * 100)
    
    return {
        "success": True,
        "message": f"Task {task_id} marked as completed" if not was_completed else f"Task {task_id} was already completed",
        "task": CHECKLIST[task_id]["task"],
        "email": email,
        "completed_tasks": sorted(list(completed)),
        "progress_percentage": round(progress_percentage, 1),
        "was_already_completed": was_completed
    }


@app.post("/api/admin/users", response_model=AllUsersProgress)
async def get_all_users_progress(request: MentorRequest):
    """
    Get progress for all users.
    Only available to mentors from config.json.
    """
    mentor_email = request.mentor_email
    
    # Check if email is a mentor
    config = load_config()
    mentors = config.get("mentors", [])
    
    if mentor_email not in mentors:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. {mentor_email} is not authorized as a mentor."
        )
    
    # Load all users data
    data = load_user_data()
    
    users_info = {}
    for email, user_data in data.items():
        completed = len(user_data["completed_tasks"])
        total = len(CHECKLIST)
        percentage = (completed / total * 100) if total > 0 else 0
        
        users_info[email] = {
            "completed_tasks": user_data["completed_tasks"],
            "progress_percentage": round(percentage, 1),
            "completed_count": completed,
            "total_tasks": total,
            "created_at": user_data["created_at"],
            "last_updated": user_data["last_updated"]
        }
    
    return {
        "users": users_info,
        "total_users": len(users_info)
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


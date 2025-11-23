#!/usr/bin/env python3
"""
HTTP API Server для управления чек-листом онбординга сотрудников.
FastAPI версия для работы через HTTP запросы.
"""

import json
import os
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

# Константы
DATA_FILE = "data.json"
CONFIG_FILE = "config.json"

# Определение чек-листа онбординга
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


# Pydantic модели для валидации запросов/ответов
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


# Функции работы с данными (из оригинального server.py)
def load_json_file(filepath: str) -> dict:
    """Загружает данные из JSON файла."""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_json_file(filepath: str, data: dict) -> None:
    """Сохраняет данные в JSON файл."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_user_data() -> dict:
    """Загружает данные пользователей."""
    return load_json_file(DATA_FILE)


def save_user_data(data: dict) -> None:
    """Сохраняет данные пользователей."""
    save_json_file(DATA_FILE, data)


def load_config() -> dict:
    """Загружает конфигурацию."""
    return load_json_file(CONFIG_FILE)


def create_new_user(email: str) -> dict:
    """Создает нового пользователя с пустым прогрессом."""
    now = datetime.now().isoformat()
    return {
        "completed_tasks": [],
        "created_at": now,
        "last_updated": now
    }


def get_user(email: str, data: dict) -> dict:
    """Получает данные пользователя или создает нового."""
    if email not in data:
        data[email] = create_new_user(email)
        save_user_data(data)
    return data[email]


# Создаем FastAPI приложение
app = FastAPI(
    title="Onboarding Checklist API",
    description="API для управления чек-листом онбординга сотрудников",
    version="1.0.0"
)

# Добавляем CORS для возможности запросов из браузера
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Корневой endpoint с информацией об API."""
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
    """Получить полный чек-лист онбординга."""
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
    Получить прогресс пользователя по чек-листу.
    Если пользователя нет - создается автоматически с нулевым прогрессом.
    """
    data = load_user_data()
    user_data = get_user(email, data)
    
    completed = set(user_data["completed_tasks"])
    total_tasks = len(CHECKLIST)
    progress_percentage = (len(completed) / total_tasks * 100) if total_tasks > 0 else 0
    
    # Группируем задачи по дням
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
    Отметить задачу как выполненную для пользователя.
    """
    email = request.email
    task_id = request.task_id
    
    # Валидация task_id
    if task_id not in CHECKLIST:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid task_id. Must be between 1 and 9. Got: {task_id}"
        )
    
    # Загружаем данные
    data = load_user_data()
    user_data = get_user(email, data)
    
    # Добавляем задачу если ее еще нет
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
    Получить прогресс всех пользователей.
    Доступно только менторам из config.json.
    """
    mentor_email = request.mentor_email
    
    # Проверяем, является ли email ментором
    config = load_config()
    mentors = config.get("mentors", [])
    
    if mentor_email not in mentors:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. {mentor_email} is not authorized as a mentor."
        )
    
    # Загружаем данные всех пользователей
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
    """Health check endpoint для мониторинга."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


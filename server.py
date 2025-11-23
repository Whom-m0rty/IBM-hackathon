#!/usr/bin/env python3
"""
MCP Server for managing employee onboarding checklist.
"""

import json
import os
from datetime import datetime
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

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


def format_progress(email: str, user_data: dict) -> str:
    """Formats user progress in readable format."""
    completed = set(user_data["completed_tasks"])
    
    result = [f"Onboarding Progress for: {email}"]
    result.append(f"Started: {user_data['created_at']}")
    result.append(f"Last Updated: {user_data['last_updated']}")
    result.append("")
    
    for day in [1, 2, 3]:
        result.append(f"Day {day}:")
        day_tasks = [tid for tid, info in CHECKLIST.items() if info["day"] == day]
        for task_id in day_tasks:
            status = "✓" if task_id in completed else "☐"
            result.append(f"  {status} {task_id}. {CHECKLIST[task_id]['task']}")
        result.append("")
    
    total_completed = len(completed)
    total_tasks = len(CHECKLIST)
    result.append(f"Progress: {total_completed}/{total_tasks} tasks completed")
    
    return "\n".join(result)


def format_all_users_progress(data: dict) -> str:
    """Formats progress for all users."""
    if not data:
        return "No users found in the system."
    
    result = ["All Users Onboarding Progress", "=" * 50, ""]
    
    for email, user_data in data.items():
        completed = len(user_data["completed_tasks"])
        total = len(CHECKLIST)
        percentage = (completed / total * 100) if total > 0 else 0
        
        result.append(f"User: {email}")
        result.append(f"  Progress: {completed}/{total} tasks ({percentage:.1f}%)")
        result.append(f"  Started: {user_data['created_at']}")
        result.append(f"  Last Updated: {user_data['last_updated']}")
        result.append(f"  Completed Tasks: {sorted(user_data['completed_tasks'])}")
        result.append("")
    
    return "\n".join(result)


# Create MCP server
app = Server("onboarding-checklist")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List of available tools."""
    return [
        Tool(
            name="get_user_progress",
            description="Get the onboarding checklist progress for a specific user by email. Creates a new user if email doesn't exist.",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "User's email address"
                    }
                },
                "required": ["email"]
            }
        ),
        Tool(
            name="mark_task_complete",
            description="Mark a specific task as completed for a user. Task IDs are 1-9. Creates a new user if email doesn't exist.",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "User's email address"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to mark as complete (1-9)",
                        "minimum": 1,
                        "maximum": 9
                    }
                },
                "required": ["email", "task_id"]
            }
        ),
        Tool(
            name="get_all_users_progress",
            description="Get onboarding progress for all users. Only accessible by mentor emails configured in config.json.",
            inputSchema={
                "type": "object",
                "properties": {
                    "mentor_email": {
                        "type": "string",
                        "description": "Mentor's email address"
                    }
                },
                "required": ["mentor_email"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "get_user_progress":
        email = arguments.get("email")
        if not email:
            return [TextContent(type="text", text="Error: email is required")]
        
        data = load_user_data()
        user_data = get_user(email, data)
        progress = format_progress(email, user_data)
        
        return [TextContent(type="text", text=progress)]
    
    elif name == "mark_task_complete":
        email = arguments.get("email")
        task_id = arguments.get("task_id")
        
        if not email:
            return [TextContent(type="text", text="Error: email is required")]
        if task_id is None:
            return [TextContent(type="text", text="Error: task_id is required")]
        
        # Validate task_id
        if task_id not in CHECKLIST:
            return [TextContent(
                type="text",
                text=f"Error: Invalid task_id. Must be between 1 and 9."
            )]
        
        # Load data
        data = load_user_data()
        user_data = get_user(email, data)
        
        # Add task if not already completed
        if task_id not in user_data["completed_tasks"]:
            user_data["completed_tasks"].append(task_id)
            user_data["completed_tasks"].sort()
            user_data["last_updated"] = datetime.now().isoformat()
            save_user_data(data)
            message = f"Task {task_id} marked as completed for {email}"
        else:
            message = f"Task {task_id} was already completed for {email}"
        
        # Return updated progress
        progress = format_progress(email, user_data)
        return [TextContent(type="text", text=f"{message}\n\n{progress}")]
    
    elif name == "get_all_users_progress":
        mentor_email = arguments.get("mentor_email")
        if not mentor_email:
            return [TextContent(type="text", text="Error: mentor_email is required")]
        
        # Check if email is a mentor
        config = load_config()
        mentors = config.get("mentors", [])
        
        if mentor_email not in mentors:
            return [TextContent(
                type="text",
                text=f"Error: Access denied. {mentor_email} is not authorized as a mentor."
            )]
        
        # Load and format all users data
        data = load_user_data()
        all_progress = format_all_users_progress(data)
        
        return [TextContent(type="text", text=all_progress)]
    
    else:
        return [TextContent(type="text", text=f"Error: Unknown tool {name}")]


async def main():
    """Start MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


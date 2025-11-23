# MCP Onboarding Checklist Server

A server for managing employee onboarding checklist. Allows tracking progress of new employees through a standard onboarding checklist for the "Junior Software Engineer" position.

## 🚀 Quick Deploy

**Need to deploy fast?** See [QUICKSTART.md](QUICKSTART.md) or [DEPLOY.md](DEPLOY.md)

**Your app is already working!** Just need to publish it:
1. Push to GitHub (1 min)
2. Use your ngrok URL as Application URL
3. Done! ✅

**Live Demo:** API running at ngrok URL with Swagger docs at `/docs`

## 🚀 Two Server Versions

The project contains **two versions** of the server with identical functionality:

### 1. MCP Server (`server.py`)
- Works via MCP protocol (stdio)
- For use with Claude Desktop and MCP clients
- **Documentation:** see below in this file

### 2. HTTP API Server (`http_server.py`)
- Works via HTTP REST API (FastAPI)
- Can be used with nginx, curl, browser
- Port: 8000 (default)
- **Detailed documentation:** [HTTP_API.md](HTTP_API.md)
- **Swagger UI:** http://localhost:8000/docs

**Both versions use the same data files (`data.json`, `config.json`)!**

## Features

- ✅ Get user progress by email
- ✅ Mark completed tasks
- ✅ Automatic creation of new users
- ✅ Mentor access to all users' progress
- ✅ Data storage in JSON
- ✅ Checklist of 9 tasks over 3 days

## Quick Start

### 🎯 Version Selection

**Simple version (recommended):**
- Use `agent_prompt_simple.txt` for watsonx
- Better compliance with agents
- Clean formatting
- See [SIMPLE_SETUP.md](SIMPLE_SETUP.md) and [CHEATSHEET.md](CHEATSHEET.md)

**Extended version (optional):**
- Use `FORMATTING_EXAMPLES.md` for beautiful formatting
- More emojis and visual elements
- May not always work with agents

### HTTP API version (recommended for web integration)

```bash
# Installation
pip install -r requirements.txt

# Run
python http_server.py

# Server available at http://localhost:8000
# Documentation: http://localhost:8000/docs
```

See [HTTP_API.md](HTTP_API.md) for examples with curl, nginx, etc.

### MCP version (for Claude Desktop)

```bash
# Installation
pip install -r requirements.txt

# Run
python server.py
```

See instructions below for setup with Claude Desktop.

## Checklist Structure

### Day 1
1. Meet your manager
2. Meet your buddy / mentor
3. Read the company handbook
4. Complete basic security training

### Day 2
5. Set up your development environment
6. Join the team stand-up meeting
7. Read the documentation for the main product

### Day 3
8. Shadow a team member during a real task
9. Pick your first small task from the backlog

---

# MCP Server (stdio version)

Below describes the setup of the **MCP version** for working with Claude Desktop. For HTTP API see [HTTP_API.md](HTTP_API.md).

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure mentor list

Edit the `config.json` file and add mentor email addresses:

```json
{
  "mentors": [
    "mentor@company.com",
    "admin@company.com"
  ]
}
```

## Running MCP Server

### Directly via Python

```bash
python server.py
```

### Connecting to Claude Desktop (MCP)

Add the following configuration to the Claude Desktop configuration file:

**MacOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "onboarding-checklist": {
      "command": "python",
      "args": ["/Users/whom/Documents/watsonxMCP/server.py"]
    }
  }
}
```

Replace the path `/Users/whom/Documents/watsonxMCP/server.py` with the full path to your server.py file.

After adding the configuration, restart Claude Desktop.

## Available Tools (MCP Tools)

### 1. get_user_progress

Gets user progress on the checklist.

**Parameters:**
- `email` (string) - User's email address

**Behavior:**
- If user is not in database, automatically creates new one with zero progress
- Returns formatted progress for all tasks

**Example usage in prompt:**
```
Show my onboarding progress for user@company.com
```

### 2. mark_task_complete

Marks a task as completed for a specific user.

**Parameters:**
- `email` (string) - User's email address
- `task_id` (integer, 1-9) - Task ID to mark

**Behavior:**
- Validates task_id (must be from 1 to 9)
- If user doesn't exist, creates new one
- If task is already completed, returns appropriate message
- Updates last modified timestamp

**Example usage in prompt:**
```
Mark task 1 as completed for user@company.com
```

### 3. get_all_users_progress

Gets progress for all users. Only available to mentors.

**Parameters:**
- `mentor_email` (string) - Mentor's email address

**Behavior:**
- Checks that email is in the mentor list from `config.json`
- If email is not a mentor, returns access error
- Returns summary for all users with completion percentage

**Example usage in prompt:**
```
Show progress for all employees (mentor@company.com)
```

## Using with Agent

Use the prompt from the `agent_prompt.txt` file to configure your AI agent. This prompt:

- Instructs the agent to always request user's email
- Explains how to use available MCP tools
- Contains examples of interactions with users
- Defines logic for working with checklist

## Data Structure

### data.json

Stores progress for all users:

```json
{
  "user@company.com": {
    "completed_tasks": [1, 2, 4],
    "created_at": "2025-11-23T10:00:00",
    "last_updated": "2025-11-23T15:30:00"
  },
  "another@company.com": {
    "completed_tasks": [1, 2, 3, 4, 5],
    "created_at": "2025-11-22T09:00:00",
    "last_updated": "2025-11-23T11:00:00"
  }
}
```

### config.json

List of mentor email addresses with access to all users' data:

```json
{
  "mentors": [
    "mentor@company.com",
    "admin@company.com"
  ]
}
```

## Usage Scenarios

### Scenario 1: New employee starts onboarding

1. Employee writes: "Show me my onboarding checklist"
2. Agent requests email
3. Employee provides: john.doe@company.com
4. Agent calls `get_user_progress` → new user is created
5. Agent shows full checklist with indication that nothing is completed

### Scenario 2: Employee completes tasks

1. Employee: "I met with the manager! (john.doe@company.com)"
2. Agent calls `mark_task_complete` with task_id=1
3. Agent confirms and shows updated progress

### Scenario 3: Mentor checks everyone

1. Mentor: "Show progress for all employees (mentor@company.com)"
2. Agent calls `get_all_users_progress`
3. Agent shows summary table for all users

### Scenario 4: Unauthorized access

1. Regular user tries: "Show all users (user@company.com)"
2. Agent calls `get_all_users_progress`
3. Server returns error: "Access denied"
4. Agent politely explains that access is only for mentors

## Development and Debugging

### Testing tools

You can test MCP tools directly through MCP inspector or through Claude Desktop.

### Logs

Server works via stdio, all interactions happen through standard input/output streams.

### Backup

Recommended to regularly back up the `data.json` file:

```bash
cp data.json data.json.backup
```

## Requirements

- Python 3.8+
- mcp >= 0.9.0

## License

MIT

## Support

If problems occur:

1. Check that all dependencies are installed
2. Make sure files `data.json` and `config.json` exist
3. Check file permissions
4. Make sure the path to server.py in MCP configuration is correct

## Extending Functionality

### Adding new mentors

Simply add email to `config.json`:

```json
{
  "mentors": [
    "mentor@company.com",
    "admin@company.com",
    "new-mentor@company.com"
  ]
}
```

### Modifying checklist

Checklist is hardcoded in `server.py` in the `CHECKLIST` variable. To modify, edit this variable and restart the server.

**Note:** When changing the number of tasks, make sure to update task_id validation in the `mark_task_complete` function.

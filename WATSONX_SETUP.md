# watsonx Orchestrate Setup Guide

Complete guide for integrating the Onboarding Checklist API with watsonx Orchestrate.

## 🚀 Quick Start

### Step 1: Start Your Servers

**Terminal 1 - HTTP API Server:**
```bash
cd /Users/whom/Documents/watsonxMCP
python3 http_server.py
```

**Terminal 2 - Ngrok Tunnel:**
```bash
ngrok http 8000
```

Copy your ngrok URL (e.g., `https://xxxx.ngrok-free.app`)

### Step 2: Update OpenAPI File

Edit `openapi.json` and update the server URL (line 10) with your ngrok URL:

```json
"servers": [
  {
    "url": "https://YOUR_NGROK_URL",
    "description": "Ngrok tunnel to local development server"
  }
],
```

### Step 3: Import to watsonx Orchestrate

1. Log in to watsonx Orchestrate
2. Navigate to **Import tool** or **Add Skills**
3. Choose **OpenAPI** import option
4. Upload the file: `openapi.json`

### Step 4: Select Operations

When prompted, select these operations:

- ✅ **get_user_progress** - Get User Progress
- ✅ **mark_task_complete** - Mark Task Complete  
- ✅ **get_all_users_progress** - Get All Users Progress

### Step 5: Create Your Agent

1. Click **Create new agent**
2. Fill in:
   - **Name:** `HR Onboarding Assistant`
   - **Description:** `Agent that manages a structured onboarding checklist for a new hire (for example, a junior software engineer) and returns the tasks grouped by day or category.`

### Step 6: Add Tools to Agent

1. Go to **Toolset** section
2. Click **Add tool**
3. Select **Add from local instance**
4. Choose all 3 operations imported earlier
5. Click **Add to agent**

### Step 7: Configure Agent Behavior

Copy the content from `agent_prompt_openapi.txt` and paste it into the **Behavior** section of your agent.

This prompt includes:
- Checklist structure (9 tasks, 3 days)
- Instructions to always ask for email
- How to use each API operation
- Response format examples
- Error handling guidelines

### Step 8: Test Your Agent

In the **Preview** panel or main chat, try these queries:

```
Show me my onboarding progress
```

```
I completed task 1 (john.doe@company.com)
```

```
What should I do today? (my email is jane@company.com)
```

```
Show all employees' progress (mentor@company.com)
```

## 📊 API Operations Summary

### 1. Get User Progress
- **Method:** GET
- **Endpoint:** `/api/users/{email}/progress`
- **Purpose:** Retrieve user's checklist progress
- **Auto-creates:** Yes, new users with zero progress

### 2. Mark Task Complete
- **Method:** POST
- **Endpoint:** `/api/users/tasks/complete`
- **Body:** `{"email": "user@example.com", "task_id": 1}`
- **Purpose:** Mark a task (1-9) as completed

### 3. Get All Users Progress (Mentors Only)
- **Method:** POST
- **Endpoint:** `/api/admin/users`
- **Body:** `{"mentor_email": "mentor@example.com"}`
- **Purpose:** View all users' progress (requires mentor access)

## 🔧 Configuration

### Mentor Access

Edit `config.json` to add mentor emails:

```json
{
  "mentors": [
    "mentor@company.com",
    "admin@company.com",
    "your-email@company.com"
  ]
}
```

Only emails in this list can use the "Get All Users Progress" operation.

## 🔍 Troubleshooting

### ngrok URL Changed
If you restart ngrok, you'll get a new URL. Update:
1. `openapi.json` (line 10)
2. Re-import to watsonx Orchestrate

### API Not Responding
Check:
1. Is `http_server.py` running? (Terminal 1)
2. Is ngrok running? (Terminal 2)
3. Does ngrok URL match in `openapi.json`?

### 403 Forbidden (Mentor Access)
The email used is not in the mentors list. Add it to `config.json`.

### Invalid Task ID
Task IDs must be 1-9. Other numbers will return a 400 error.

## 📝 Sample Conversations

### New Employee First Day

```
User: Hi, I'm starting today!
Agent: Welcome! I'd be happy to help with your onboarding. Could you please provide your email address?
User: john.doe@company.com
Agent: Great! Here's your onboarding checklist...
[Shows full checklist with Day 1 tasks]
```

### Completing Tasks

```
User: I just met with my manager (john.doe@company.com)
Agent: [Calls mark_task_complete with task_id=1]
Excellent! I've marked "Meet your manager" as completed...
```

### Mentor Checking Team

```
User: Show everyone's progress (mentor@company.com)
Agent: [Calls get_all_users_progress]
Here's the onboarding progress overview for all employees...
```

## 🎯 Best Practices

1. **Keep Servers Running:** Both `http_server.py` and `ngrok` must run continuously
2. **Stable ngrok URL:** Consider ngrok paid plan for static URLs
3. **Mentor List:** Keep `config.json` updated with current mentors
4. **Regular Backups:** Backup `data.json` regularly (contains all user progress)
5. **Monitor Logs:** Check terminal output for errors

## 📚 Files Reference

- `openapi.json` - API specification for watsonx import
- `agent_prompt_openapi.txt` - Agent behavior prompt
- `http_server.py` - HTTP API server (FastAPI)
- `server.py` - MCP server (stdio, for MCP clients)
- `data.json` - User progress database
- `config.json` - Mentor configuration
- `HTTP_API.md` - Detailed API documentation

## 🔄 Updating Checklist

To modify the checklist, edit `http_server.py`:

```python
CHECKLIST = {
    1: {"day": 1, "task": "Your new task"},
    # ... add more tasks
}
```

Then restart the server.

## ✅ Verification Checklist

Before going live:

- [ ] `http_server.py` is running on port 8000
- [ ] `ngrok` is running and URL is noted
- [ ] `openapi.json` has correct ngrok URL
- [ ] OpenAPI imported successfully to watsonx
- [ ] Agent created with all 3 operations
- [ ] Agent behavior configured with prompt
- [ ] `config.json` has correct mentor emails
- [ ] Test queries work correctly
- [ ] Mentor access verified

You're all set! 🎉


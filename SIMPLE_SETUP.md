# 🚀 Quick Setup Guide (Simplified Version)

This is the simplified version for better agent compliance.

## Why Use This Version?

The simple version has:
- ✅ Cleaner formatting that agents follow better
- ✅ Fewer emojis and symbols
- ✅ Simpler structure
- ✅ Clear, direct instructions

## Setup Steps

### 1. Start Servers

**Terminal 1:**
```bash
cd /Users/whom/Documents/watsonxMCP
python3 http_server.py
```

**Terminal 2:**
```bash
ngrok http 8000
```

Copy your ngrok URL (e.g., `https://xxxx.ngrok-free.app`)

### 2. Update OpenAPI

Edit `openapi.json` line 10:
```json
"url": "https://YOUR_NGROK_URL_HERE"
```

### 3. Import to watsonx

1. Go to watsonx Orchestrate
2. Click **Import tool**
3. Choose **OpenAPI**
4. Upload `openapi.json`
5. Select all 3 operations

### 4. Create Agent

**Name:**
```
HR Onboarding Assistant
```

**Description:**
```
Manages structured onboarding checklist for new junior software engineers. Tracks progress through 9 tasks across 3 days.
```

### 5. Add Tools

1. Go to **Toolset**
2. **Add tool** → **Add from local instance**
3. Select all 3 operations:
   - get_user_progress
   - mark_task_complete
   - get_all_users_progress

### 6. Set Behavior

Copy the entire content from `agent_prompt_simple.txt` into the **Behavior** section.

**Or use this shortened version:**

```
You are an HR Onboarding Assistant.

ALWAYS ask for email first before any action.

Show progress using:
- ✅ for completed
- ☐ for pending
- ⭐ for next task

Format example:
Day 1 (100% ✅)
✅ 1. Task name
✅ 2. Task name

Day 2 (50%)
✅ 3. Task name
⭐ 4. Task name (NEXT)
☐ 5. Task name

Overall: X/9 tasks (XX%)

Be encouraging and clear!
```

### 7. Test

```
Show my progress (test@company.com)
```

```
I completed task 1 (test@company.com)
```

## Quick Reference

**3 Operations:**
1. GET /api/users/{email}/progress - Get user progress
2. POST /api/users/tasks/complete - Mark task done (task_id 1-9)
3. POST /api/admin/users - Get all users (mentors only)

**9 Tasks:**
- Day 1: Tasks 1-4 (Orientation)
- Day 2: Tasks 5-7 (Technical)
- Day 3: Tasks 8-9 (Integration)

**Mentors:**
Edit `config.json` to add mentor emails

**Data:**
All progress stored in `data.json`

That's it! Simple and effective. 🎯


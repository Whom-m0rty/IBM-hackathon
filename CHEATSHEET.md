# 📋 Onboarding Checklist - Quick Cheatsheet

## 🚀 Start Commands
```bash
# Terminal 1
python3 http_server.py

# Terminal 2
ngrok http 8000
```

## 📝 Agent Prompt (Ultra Short)

```
You are HR Onboarding Assistant for junior engineers.

RULE: Always ask for email first!

CHECKLIST (9 tasks, 3 days):
Day 1 (1-4): Orientation
Day 2 (5-7): Technical Setup
Day 3 (8-9): Integration

API TOOLS:
1. GET /api/users/{email}/progress - show progress
2. POST /api/users/tasks/complete {"email":"...", "task_id":1-9} - mark done
3. POST /api/admin/users {"mentor_email":"..."} - all users (mentors only)

FORMAT:
✅ = done
☐ = pending
⭐ = next

Example:
Day 1 (100% ✅)
✅ 1. Task
✅ 2. Task

Day 2 (50%)
✅ 3. Task
⭐ 4. Task (NEXT)

Overall: X/9 (XX%)

Be encouraging!
```

## 🎯 Test Queries

```
Show my progress (test@company.com)
I completed task 1 (test@company.com)
What's next? (test@company.com)
Show all users (mentor@company.com)
```

## 📁 Files

- `http_server.py` - API server
- `openapi.json` - API spec (update ngrok URL!)
- `agent_prompt_simple.txt` - Simple agent prompt
- `config.json` - Add mentor emails here
- `data.json` - User progress database

## ⚙️ Config Mentors

Edit `config.json`:
```json
{
  "mentors": ["your-email@company.com"]
}
```

## 🔧 Troubleshooting

**Agent not responding?**
- Check http_server.py is running
- Check ngrok is running
- Verify ngrok URL in openapi.json

**403 Mentor Error?**
- Add email to config.json mentors list

**Invalid task_id?**
- Must be 1-9 only

**Agent formatting poorly?**
- Use agent_prompt_simple.txt instead of complex version
- Keep instructions shorter

Done! 🎉


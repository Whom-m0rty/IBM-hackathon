# ⚡ QUICKSTART - Deploy in 2 Minutes

## Your app is already working! Just publish it.

### Step 1: Test Locally (30 seconds)

```bash
# Terminal 1: Start API
python3 http_server.py

# Terminal 2: Start ngrok
ngrok http 8000

# Terminal 3: Test Streamlit UI (optional)
streamlit run streamlit_app.py
```

Your API is live at: `https://c16f287ee8a0.ngrok-free.app`

### Step 2: Push to GitHub (1 minute)

```bash
cd /Users/whom/Documents/watsonxMCP

# Run the deploy script
./quick_deploy.sh

# Follow the instructions to create GitHub repo
```

**Or manually:**

```bash
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/watsonx-onboarding-mcp.git
git branch -M main
git push -u origin main
```

### Step 3: Submit (30 seconds)

**Public GitHub Repository:**
```
https://github.com/YOUR_USERNAME/watsonx-onboarding-mcp
```

**Application URL (choose one):**

**Option A - Current ngrok (already working):**
```
https://c16f287ee8a0.ngrok-free.app
```
API Docs: Add `/docs` to URL

**Option B - Streamlit Cloud (beautiful UI, 5 more minutes):**
1. Go to https://share.streamlit.io/
2. Connect GitHub repo
3. Deploy `streamlit_app.py`
4. Get URL like: `https://yourapp.streamlit.app`

**Option C - Vercel (permanent URL, 5 more minutes):**
```bash
npm install -g vercel
vercel --prod
```

### ✅ You're done!

**What you have:**
- ✅ Public GitHub Repository
- ✅ Working API with Swagger docs
- ✅ 3 API endpoints (get progress, mark complete, view all)
- ✅ MCP Server compatibility
- ✅ OpenAPI specification
- ✅ Streamlit UI (optional)

**Features:**
- Track onboarding progress by email
- 9 tasks across 3 days
- Automatic user creation
- Mentor dashboard
- Beautiful formatting
- JSON data storage

**Test it:**
```bash
# Get progress
curl https://c16f287ee8a0.ngrok-free.app/api/users/test@company.com/progress

# Mark task complete
curl -X POST https://c16f287ee8a0.ngrok-free.app/api/users/tasks/complete \
  -H "Content-Type: application/json" \
  -d '{"email":"test@company.com","task_id":1}'
```

**Access Swagger UI:**
```
https://c16f287ee8a0.ngrok-free.app/docs
```

That's it! 🎉


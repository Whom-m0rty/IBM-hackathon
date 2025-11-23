# 🚀 Quick Deploy (5-10 minutes)

## ⚡ Option 1: GitHub + Ngrok (RIGHT NOW - 2 minutes)

Your API is already working! Just need to upload to GitHub.

### Steps:

```bash
cd /Users/whom/Documents/watsonxMCP

# 1. Create .gitignore
cat > .gitignore << 'EOF'
*.pyc
__pycache__/
.venv/
venv/
*.log
.DS_Store
.streamlit/secrets.toml
EOF

# 2. Initialize git
git init
git add .
git commit -m "Initial commit: HR Onboarding Checklist"

# 3. Create repository on GitHub.com
# Go to https://github.com/new
# Name: watsonx-onboarding-mcp
# Public ✅
# Don't add README (we already have one)

# 4. Push code
git remote add origin https://github.com/YOUR_USERNAME/watsonx-onboarding-mcp.git
git branch -M main
git push -u origin main
```

### Your Links:

- **GitHub Repository:** `https://github.com/YOUR_USERNAME/watsonx-onboarding-mcp`
- **Application URL:** `https://c16f287ee8a0.ngrok-free.app`
- **API Docs:** `https://c16f287ee8a0.ngrok-free.app/docs`

✅ **Done in 2 minutes!**

---

## 🎨 Option 2: Streamlit Cloud (10 minutes, beautiful UI)

Create web interface on Streamlit Cloud (free).

### Steps:

**1. Push to GitHub (if not already done):**
```bash
# See Option 1 above
```

**2. Run locally for testing:**
```bash
cd /Users/whom/Documents/watsonxMCP

# Make sure http_server.py is running
python3 http_server.py  # Terminal 1

# In another terminal:
streamlit run streamlit_app.py
```

Open `http://localhost:8501` - verify everything works!

**3. Deploy to Streamlit Cloud:**

1. Go to https://share.streamlit.io/
2. Login via GitHub
3. Click **"New app"**
4. Select:
   - Repository: `YOUR_USERNAME/watsonx-onboarding-mcp`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
5. **Advanced settings** → **Secrets** → add:
   ```toml
   API_URL = "https://c16f287ee8a0.ngrok-free.app"
   ```
6. Click **Deploy**

**4. Wait 2-3 minutes**

Your app will be available at:
```
https://YOUR_USERNAME-watsonx-onboarding-mcp-streamlit-app-xyz123.streamlit.app
```

✅ **You now have:**
- Public GitHub Repository ✅
- Beautiful Web UI ✅
- Live Application URL ✅

---

## 🔥 Option 3: Vercel (for production)

Deploy FastAPI to Vercel (free, permanent URL).

**1. Create `vercel.json`:**
```bash
cd /Users/whom/Documents/watsonxMCP

cat > vercel.json << 'EOF'
{
  "builds": [
    {
      "src": "http_server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "http_server.py"
    }
  ]
}
EOF
```

**2. Deploy:**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd /Users/whom/Documents/watsonxMCP
vercel

# Follow instructions (login via GitHub)
```

**3. Production deploy:**
```bash
vercel --prod
```

Get permanent URL:
```
https://watsonx-onboarding-mcp.vercel.app
```

---

## 📝 Submission Checklist

- [ ] Public GitHub Repository
- [ ] README.md with instructions
- [ ] Application URL (working)
- [ ] Interactive demo

### Minimum (Option 1):
- GitHub: ✅
- Application URL: ngrok URL ✅
- Swagger Docs: `/docs` ✅

### Maximum (Option 2):
- GitHub: ✅
- Streamlit UI: beautiful interface ✅
- Full functionality ✅

---

## 🆘 Troubleshooting

**Ngrok URL changed?**
```bash
# Update in .streamlit/secrets.toml
API_URL = "https://NEW_NGROK_URL.ngrok-free.app"

# Or use paid ngrok for static URL
ngrok http 8000 --domain=your-static-domain.ngrok-free.app
```

**Streamlit can't see API?**
- Check that `http_server.py` is running
- Check that ngrok is working
- Check URL in secrets

**GitHub push fails?**
```bash
# Use Personal Access Token
# Settings → Developer settings → Personal access tokens
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/repo.git
```

---

## 🎯 Recommendation

**For quick submission:** Use **Option 1** (2 minutes)

**For impression:** Use **Option 2** (10 minutes)

**For production:** Use **Option 3** (15 minutes)

Good luck! 🚀

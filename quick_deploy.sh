#!/bin/bash
# Quick deploy script for watsonx Onboarding MCP

echo "🚀 Quick Deploy Script"
echo "====================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: HR Onboarding Checklist MCP"
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

echo ""
echo "📝 Next steps:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo "   Name: watsonx-onboarding-mcp"
echo "   Public: ✅"
echo ""
echo "2. Run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/watsonx-onboarding-mcp.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Your Application URLs:"
echo "   - GitHub: https://github.com/YOUR_USERNAME/watsonx-onboarding-mcp"
echo "   - API Docs: https://c16f287ee8a0.ngrok-free.app/docs"
echo "   - API Base: https://c16f287ee8a0.ngrok-free.app"
echo ""
echo "4. Optional - Deploy Streamlit UI:"
echo "   - Go to: https://share.streamlit.io/"
echo "   - Connect your GitHub repo"
echo "   - Deploy streamlit_app.py"
echo ""
echo "✅ Ready to submit!"


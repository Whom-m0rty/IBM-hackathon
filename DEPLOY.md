# 🚀 Быстрый Deploy (5-10 минут)

## ⚡ Вариант 1: GitHub + Ngrok (ПРЯМО СЕЙЧАС - 2 минуты)

Ваш API уже работает! Нужно только залить на GitHub.

### Шаги:

```bash
cd /Users/whom/Documents/watsonxMCP

# 1. Создайте .gitignore
cat > .gitignore << 'EOF'
*.pyc
__pycache__/
.venv/
venv/
*.log
.DS_Store
.streamlit/secrets.toml
EOF

# 2. Инициализируйте git
git init
git add .
git commit -m "Initial commit: HR Onboarding Checklist"

# 3. Создайте репозиторий на GitHub.com
# Перейдите на https://github.com/new
# Имя: watsonx-onboarding-mcp
# Public ✅
# Не добавляйте README (у нас уже есть)

# 4. Залейте код
git remote add origin https://github.com/YOUR_USERNAME/watsonx-onboarding-mcp.git
git branch -M main
git push -u origin main
```

### Ваши ссылки:

- **GitHub Repository:** `https://github.com/YOUR_USERNAME/watsonx-onboarding-mcp`
- **Application URL:** `https://c16f287ee8a0.ngrok-free.app`
- **API Docs:** `https://c16f287ee8a0.ngrok-free.app/docs`

✅ **Готово за 2 минуты!**

---

## 🎨 Вариант 2: Streamlit Cloud (10 минут, красивый UI)

Создайте веб-интерфейс на Streamlit Cloud (бесплатно).

### Шаги:

**1. Залейте на GitHub (если еще не сделали):**
```bash
# См. Вариант 1 выше
```

**2. Запустите локально для теста:**
```bash
cd /Users/whom/Documents/watsonxMCP

# Убедитесь, что http_server.py запущен
python3 http_server.py  # Терминал 1

# В другом терминале:
☁  watsonxMCP  streamlit run streamlit_app.py
zsh: command not found: streamlit
```

Откроется `http://localhost:8501` - проверьте, что все работает!

**3. Deploy на Streamlit Cloud:**

1. Перейдите на https://share.streamlit.io/
2. Войдите через GitHub
3. Нажмите **"New app"**
4. Выберите:
   - Repository: `YOUR_USERNAME/watsonx-onboarding-mcp`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
5. **Advanced settings** → **Secrets** → добавьте:
   ```toml
   API_URL = "https://c16f287ee8a0.ngrok-free.app"
   ```
6. Нажмите **Deploy**

**4. Ждите 2-3 минуты**

Ваше приложение будет доступно на:
```
https://YOUR_USERNAME-watsonx-onboarding-mcp-streamlit-app-xyz123.streamlit.app
```

✅ **У вас теперь есть:**
- Public GitHub Repository ✅
- Beautiful Web UI ✅
- Live Application URL ✅

---

## 🔥 Вариант 3: Vercel (для продакшен)

Deploy FastAPI на Vercel (бесплатно, постоянный URL).

**1. Создайте `vercel.json`:**
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
# Установите Vercel CLI
npm install -g vercel

# Deploy
cd /Users/whom/Documents/watsonxMCP
vercel

# Следуйте инструкциям (войдите через GitHub)
```

**3. Production deploy:**
```bash
vercel --prod
```

Получите постоянный URL:
```
https://watsonx-onboarding-mcp.vercel.app
```

---

## 📝 Чеклист для сдачи

- [ ] Public GitHub Repository
- [ ] README.md с инструкциями
- [ ] Application URL (работает)
- [ ] Интерактивная демка

### Минимум (Вариант 1):
- GitHub: ✅
- Application URL: ngrok URL ✅
- Swagger Docs: `/docs` ✅

### Максимум (Вариант 2):
- GitHub: ✅
- Streamlit UI: красивый интерфейс ✅
- Полная функциональность ✅

---

## 🆘 Troubleshooting

**Ngrok URL изменился?**
```bash
# Обновите в .streamlit/secrets.toml
API_URL = "https://NEW_NGROK_URL.ngrok-free.app"

# Или используйте платный ngrok для статичного URL
ngrok http 8000 --domain=your-static-domain.ngrok-free.app
```

**Streamlit не видит API?**
- Проверьте, что `http_server.py` запущен
- Проверьте, что ngrok работает
- Проверьте URL в secrets

**GitHub push fails?**
```bash
# Используйте Personal Access Token
# Settings → Developer settings → Personal access tokens
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/repo.git
```

---

## 🎯 Рекомендация

**Для быстрой сдачи:** Используйте **Вариант 1** (2 минуты)

**Для впечатления:** Используйте **Вариант 2** (10 минут)

**Для production:** Используйте **Вариант 3** (15 минут)

Удачи! 🚀


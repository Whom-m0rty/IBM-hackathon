# HTTP API для Onboarding Checklist

FastAPI версия сервера для работы через HTTP запросы. Можно использовать с nginx, curl, или любым HTTP клиентом.

## Запуск сервера

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск на порту 8000

```bash
python http_server.py
```

Или через uvicorn:

```bash
uvicorn http_server:app --host 0.0.0.0 --port 8000 --reload
```

Сервер будет доступен на: `http://localhost:8000`

## API Endpoints

### 1. Корневой endpoint

```bash
GET /
```

Возвращает информацию об API и список доступных endpoints.

**Пример:**
```bash
curl http://localhost:8000/
```

### 2. Получить чек-лист

```bash
GET /api/checklist
```

Возвращает полный чек-лист онбординга, сгруппированный по дням.

**Пример:**
```bash
curl http://localhost:8000/api/checklist
```

**Ответ:**
```json
{
  "checklist": {
    "1": [
      {"id": 1, "task": "Meet your manager"},
      {"id": 2, "task": "Meet your buddy / mentor"},
      ...
    ],
    "2": [...],
    "3": [...]
  },
  "total_tasks": 9,
  "total_days": 3
}
```

### 3. Получить прогресс пользователя

```bash
GET /api/users/{email}/progress
```

Получает прогресс конкретного пользователя по email. Если пользователя нет - создается автоматически.

**Параметры:**
- `email` (path) - Email пользователя

**Пример:**
```bash
curl http://localhost:8000/api/users/john.doe@company.com/progress
```

**Ответ:**
```json
{
  "email": "john.doe@company.com",
  "completed_tasks": [1, 2, 4],
  "created_at": "2025-11-23T10:00:00",
  "last_updated": "2025-11-23T15:30:00",
  "progress_percentage": 33.3,
  "total_tasks": 9,
  "tasks_by_day": {
    "day_1": [
      {"id": 1, "task": "Meet your manager", "completed": true},
      {"id": 2, "task": "Meet your buddy / mentor", "completed": true},
      {"id": 3, "task": "Read the company handbook", "completed": false},
      {"id": 4, "task": "Complete basic security training", "completed": true}
    ],
    "day_2": [...],
    "day_3": [...]
  }
}
```

### 4. Отметить задачу как выполненную

```bash
POST /api/users/tasks/complete
```

Отмечает задачу как выполненную для пользователя.

**Тело запроса (JSON):**
```json
{
  "email": "john.doe@company.com",
  "task_id": 1
}
```

**Пример с curl:**
```bash
curl -X POST http://localhost:8000/api/users/tasks/complete \
  -H "Content-Type: application/json" \
  -d '{"email": "john.doe@company.com", "task_id": 1}'
```

**Ответ:**
```json
{
  "success": true,
  "message": "Task 1 marked as completed",
  "task": "Meet your manager",
  "email": "john.doe@company.com",
  "completed_tasks": [1],
  "progress_percentage": 11.1,
  "was_already_completed": false
}
```

### 5. Получить прогресс всех пользователей (только для менторов)

```bash
POST /api/admin/users
```

Возвращает прогресс всех пользователей. Доступно только менторам из `config.json`.

**Тело запроса (JSON):**
```json
{
  "mentor_email": "mentor@company.com"
}
```

**Пример с curl:**
```bash
curl -X POST http://localhost:8000/api/admin/users \
  -H "Content-Type: application/json" \
  -d '{"mentor_email": "mentor@company.com"}'
```

**Ответ:**
```json
{
  "users": {
    "john.doe@company.com": {
      "completed_tasks": [1, 2, 4],
      "progress_percentage": 33.3,
      "completed_count": 3,
      "total_tasks": 9,
      "created_at": "2025-11-23T10:00:00",
      "last_updated": "2025-11-23T15:30:00"
    },
    "jane.smith@company.com": {
      "completed_tasks": [1, 2, 3, 4, 5, 6],
      "progress_percentage": 66.7,
      "completed_count": 6,
      "total_tasks": 9,
      "created_at": "2025-11-22T09:00:00",
      "last_updated": "2025-11-23T11:00:00"
    }
  },
  "total_users": 2
}
```

**Ошибка доступа (403):**
```json
{
  "detail": "Access denied. user@company.com is not authorized as a mentor."
}
```

### 6. Health Check

```bash
GET /health
```

Проверка работоспособности сервера.

**Пример:**
```bash
curl http://localhost:8000/health
```

**Ответ:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-23T16:45:00"
}
```

## Автоматическая документация

FastAPI автоматически генерирует интерактивную документацию:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Там можно тестировать все endpoints прямо из браузера!

## Настройка Nginx

### Конфигурация nginx

Создайте файл `/etc/nginx/sites-available/onboarding-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Замените на ваш домен

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Включение конфигурации

```bash
sudo ln -s /etc/nginx/sites-available/onboarding-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### С SSL (Let's Encrypt)

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

## Запуск в production

### С systemd

Создайте файл `/etc/systemd/system/onboarding-api.service`:

```ini
[Unit]
Description=Onboarding Checklist API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/watsonxMCP
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn http_server:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Запуск:

```bash
sudo systemctl daemon-reload
sudo systemctl enable onboarding-api
sudo systemctl start onboarding-api
sudo systemctl status onboarding-api
```

### С gunicorn (для production)

```bash
pip install gunicorn

gunicorn http_server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

## CORS

По умолчанию CORS настроен на `allow_origins=["*"]` для разработки. 

**В production** измените в `http_server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],  # Конкретные домены
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Примеры использования

### Python с requests

```python
import requests

# Получить прогресс
response = requests.get("http://localhost:8000/api/users/john@company.com/progress")
print(response.json())

# Отметить задачу
response = requests.post(
    "http://localhost:8000/api/users/tasks/complete",
    json={"email": "john@company.com", "task_id": 1}
)
print(response.json())
```

### JavaScript (fetch)

```javascript
// Получить прогресс
const response = await fetch('http://localhost:8000/api/users/john@company.com/progress');
const data = await response.json();
console.log(data);

// Отметить задачу
const response = await fetch('http://localhost:8000/api/users/tasks/complete', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'john@company.com', task_id: 1 })
});
const data = await response.json();
console.log(data);
```

### curl скрипт для тестирования

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"
EMAIL="test@company.com"

echo "=== Получаем чек-лист ==="
curl -s "$BASE_URL/api/checklist" | jq

echo -e "\n=== Получаем прогресс пользователя ==="
curl -s "$BASE_URL/api/users/$EMAIL/progress" | jq

echo -e "\n=== Отмечаем задачу 1 ==="
curl -s -X POST "$BASE_URL/api/users/tasks/complete" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"task_id\": 1}" | jq

echo -e "\n=== Проверяем обновленный прогресс ==="
curl -s "$BASE_URL/api/users/$EMAIL/progress" | jq
```

## Мониторинг

### Логирование

Uvicorn автоматически логирует все запросы в stdout. Для сохранения в файл:

```bash
uvicorn http_server:app --host 0.0.0.0 --port 8000 \
  --log-file /var/log/onboarding-api.log
```

### Health check с curl

```bash
curl http://localhost:8000/health
```

Используйте этот endpoint для мониторинга с помощью Nagios, Zabbix, или подобных инструментов.

## Безопасность

### Рекомендации для production:

1. **Используйте HTTPS** (SSL/TLS)
2. **Ограничьте CORS** конкретными доменами
3. **Добавьте аутентификацию** (JWT, OAuth)
4. **Rate limiting** для защиты от DDoS
5. **Валидация входных данных** (уже реализована через Pydantic)
6. **Файрвол** - открыть только нужные порты

### Пример с JWT (опционально)

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

Добавьте middleware для проверки токенов в `http_server.py`.

## Отличия от MCP версии

| Особенность | MCP (server.py) | HTTP API (http_server.py) |
|-------------|-----------------|---------------------------|
| Протокол | stdio (stdin/stdout) | HTTP REST API |
| Использование | Claude Desktop, MCP клиенты | Любой HTTP клиент |
| Порт | Нет | 8000 (по умолчанию) |
| Документация | Нет | Swagger UI (/docs) |
| CORS | Не применимо | Да |
| nginx | Не нужен | Можно использовать |

Обе версии используют одинаковые файлы данных (`data.json`, `config.json`), поэтому можно использовать их параллельно!


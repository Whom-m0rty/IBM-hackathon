# HTTP API for Onboarding Checklist

FastAPI version of the server for working via HTTP requests. Can be used with nginx, curl, or any HTTP client.

## Starting the Server

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Running on Port 8000

```bash
python http_server.py
```

Or via uvicorn:

```bash
uvicorn http_server:app --host 0.0.0.0 --port 8000 --reload
```

Server will be available at: `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint

```bash
GET /
```

Returns API information and list of available endpoints.

**Example:**
```bash
curl http://localhost:8000/
```

### 2. Get Checklist

```bash
GET /api/checklist
```

Returns full onboarding checklist, grouped by days.

**Example:**
```bash
curl http://localhost:8000/api/checklist
```

**Response:**
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

### 3. Get User Progress

```bash
GET /api/users/{email}/progress
```

Gets progress for specific user by email. If user doesn't exist - created automatically.

**Parameters:**
- `email` (path) - User's email

**Example:**
```bash
curl http://localhost:8000/api/users/john.doe@company.com/progress
```

**Response:**
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

### 4. Mark Task as Completed

```bash
POST /api/users/tasks/complete
```

Marks a task as completed for user.

**Request Body (JSON):**
```json
{
  "email": "john.doe@company.com",
  "task_id": 1
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/users/tasks/complete \
  -H "Content-Type: application/json" \
  -d '{"email": "john.doe@company.com", "task_id": 1}'
```

**Response:**
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

### 5. Get All Users' Progress (Mentors Only)

```bash
POST /api/admin/users
```

Returns progress for all users. Only available to mentors from `config.json`.

**Request Body (JSON):**
```json
{
  "mentor_email": "mentor@company.com"
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/admin/users \
  -H "Content-Type: application/json" \
  -d '{"mentor_email": "mentor@company.com"}'
```

**Response:**
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

**Access Denied Error (403):**
```json
{
  "detail": "Access denied. user@company.com is not authorized as a mentor."
}
```

### 6. Health Check

```bash
GET /health
```

Server health check.

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-23T16:45:00"
}
```

## Automatic Documentation

FastAPI automatically generates interactive documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

You can test all endpoints directly from the browser!

## Nginx Configuration

### Nginx Config

Create file `/etc/nginx/sites-available/onboarding-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain

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

### Enable Configuration

```bash
sudo ln -s /etc/nginx/sites-available/onboarding-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### With SSL (Let's Encrypt)

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

## Running in Production

### With systemd

Create file `/etc/systemd/system/onboarding-api.service`:

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

Start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable onboarding-api
sudo systemctl start onboarding-api
sudo systemctl status onboarding-api
```

### With gunicorn (for production)

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

By default CORS is configured as `allow_origins=["*"]` for development. 

**In production** change in `http_server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],  # Specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Usage Examples

### Python with requests

```python
import requests

# Get progress
response = requests.get("http://localhost:8000/api/users/john@company.com/progress")
print(response.json())

# Mark task
response = requests.post(
    "http://localhost:8000/api/users/tasks/complete",
    json={"email": "john@company.com", "task_id": 1}
)
print(response.json())
```

### JavaScript (fetch)

```javascript
// Get progress
const response = await fetch('http://localhost:8000/api/users/john@company.com/progress');
const data = await response.json();
console.log(data);

// Mark task
const response = await fetch('http://localhost:8000/api/users/tasks/complete', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'john@company.com', task_id: 1 })
});
const data = await response.json();
console.log(data);
```

### curl script for testing

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"
EMAIL="test@company.com"

echo "=== Get checklist ==="
curl -s "$BASE_URL/api/checklist" | jq

echo -e "\n=== Get user progress ==="
curl -s "$BASE_URL/api/users/$EMAIL/progress" | jq

echo -e "\n=== Mark task 1 ==="
curl -s -X POST "$BASE_URL/api/users/tasks/complete" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"task_id\": 1}" | jq

echo -e "\n=== Check updated progress ==="
curl -s "$BASE_URL/api/users/$EMAIL/progress" | jq
```

## Monitoring

### Logging

Uvicorn automatically logs all requests to stdout. To save to file:

```bash
uvicorn http_server:app --host 0.0.0.0 --port 8000 \
  --log-file /var/log/onboarding-api.log
```

### Health check with curl

```bash
curl http://localhost:8000/health
```

Use this endpoint for monitoring with Nagios, Zabbix, or similar tools.

## Security

### Production Recommendations:

1. **Use HTTPS** (SSL/TLS)
2. **Restrict CORS** to specific domains
3. **Add authentication** (JWT, OAuth)
4. **Rate limiting** for DDoS protection
5. **Input validation** (already implemented via Pydantic)
6. **Firewall** - open only necessary ports

### Example with JWT (optional)

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

Add middleware for token verification in `http_server.py`.

## Differences from MCP Version

| Feature | MCP (server.py) | HTTP API (http_server.py) |
|---------|----------------|---------------------------|
| Protocol | stdio (stdin/stdout) | HTTP REST API |
| Usage | Claude Desktop, MCP clients | Any HTTP client |
| Port | None | 8000 (default) |
| Documentation | None | Swagger UI (/docs) |
| CORS | Not applicable | Yes |
| nginx | Not needed | Can be used |

Both versions use the same data files (`data.json`, `config.json`), so you can use them in parallel!

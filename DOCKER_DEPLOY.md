# 🐳 Docker Deployment Guide

Полное руководство по развертыванию MCP сервера в Docker контейнере и публикации в облачные платформы.

## 📦 Быстрый старт

### Локальный запуск

```bash
# Сборка образа
docker build -t watsonx-mcp:latest .

# Запуск контейнера
docker run -d \
  --name watsonx-mcp \
  -p 8000:8000 \
  -v $(pwd)/data.json:/app/data.json \
  -v $(pwd)/config.json:/app/config.json \
  watsonx-mcp:latest

# Проверка работы
curl http://localhost:8000/health
```

### Docker Compose (рекомендуется)

```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Остановка с удалением volumes
docker-compose down -v
```

## 🚀 Публикация в Container Registry

### 1. Docker Hub

```bash
# Логин
docker login

# Тегирование образа
docker tag watsonx-mcp:latest YOUR_USERNAME/watsonx-mcp:latest
docker tag watsonx-mcp:latest YOUR_USERNAME/watsonx-mcp:v1.0.0

# Публикация
docker push YOUR_USERNAME/watsonx-mcp:latest
docker push YOUR_USERNAME/watsonx-mcp:v1.0.0

# Запуск из Docker Hub
docker run -d -p 8000:8000 YOUR_USERNAME/watsonx-mcp:latest
```

### 2. GitHub Container Registry (ghcr.io)

```bash
# Логин (используйте Personal Access Token с правами write:packages)
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin

# Тегирование
docker tag watsonx-mcp:latest ghcr.io/YOUR_GITHUB_USERNAME/watsonx-mcp:latest
docker tag watsonx-mcp:latest ghcr.io/YOUR_GITHUB_USERNAME/watsonx-mcp:v1.0.0

# Публикация
docker push ghcr.io/YOUR_GITHUB_USERNAME/watsonx-mcp:latest
docker push ghcr.io/YOUR_GITHUB_USERNAME/watsonx-mcp:v1.0.0

# Запуск из GHCR
docker run -d -p 8000:8000 ghcr.io/YOUR_GITHUB_USERNAME/watsonx-mcp:latest
```

### 3. Google Container Registry (gcr.io)

```bash
# Настройка gcloud
gcloud auth configure-docker

# Тегирование
docker tag watsonx-mcp:latest gcr.io/YOUR_PROJECT_ID/watsonx-mcp:latest

# Публикация
docker push gcr.io/YOUR_PROJECT_ID/watsonx-mcp:latest

# Запуск
docker run -d -p 8000:8000 gcr.io/YOUR_PROJECT_ID/watsonx-mcp:latest
```

### 4. Amazon ECR

```bash
# Логин
aws ecr get-login-password --region YOUR_REGION | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com

# Создание репозитория (если еще не создан)
aws ecr create-repository --repository-name watsonx-mcp --region YOUR_REGION

# Тегирование
docker tag watsonx-mcp:latest YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/watsonx-mcp:latest

# Публикация
docker push YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/watsonx-mcp:latest
```

## ☁️ Развертывание в облаке

### Render.com

1. Создайте аккаунт на [Render.com](https://render.com)
2. Нажмите "New +" → "Web Service"
3. Подключите ваш GitHub репозиторий
4. Настройки:
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Port**: 8000
   - **Health Check Path**: `/health`
5. Добавьте переменные окружения (если нужно)
6. Нажмите "Create Web Service"

**Стоимость**: Бесплатный tier доступен

### Railway.app

```bash
# Установка Railway CLI
npm install -g @railway/cli

# Логин
railway login

# Инициализация проекта
railway init

# Развертывание
railway up

# Открыть в браузере
railway open
```

**Dockerfile будет автоматически определен и использован**

### Google Cloud Run

```bash
# Сборка и публикация
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/watsonx-mcp

# Развертывание
gcloud run deploy watsonx-mcp \
  --image gcr.io/YOUR_PROJECT_ID/watsonx-mcp \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000

# Получить URL
gcloud run services describe watsonx-mcp --region us-central1 --format 'value(status.url)'
```

**Особенности Cloud Run:**
- Автоматическое масштабирование
- Оплата за использование
- HTTPS по умолчанию

### AWS App Runner

1. Опубликуйте образ в Amazon ECR (см. выше)
2. Откройте [AWS App Runner Console](https://console.aws.amazon.com/apprunner)
3. Нажмите "Create service"
4. Выберите "Container registry" → "Amazon ECR"
5. Выберите ваш образ
6. Настройки:
   - **Port**: 8000
   - **Health check path**: `/health`
7. Создайте сервис

### Azure Container Instances

```bash
# Создание группы ресурсов
az group create --name watsonx-mcp-rg --location eastus

# Создание container registry
az acr create --resource-group watsonx-mcp-rg --name watsonxmcpregistry --sku Basic

# Логин в registry
az acr login --name watsonxmcpregistry

# Тегирование
docker tag watsonx-mcp:latest watsonxmcpregistry.azurecr.io/watsonx-mcp:latest

# Публикация
docker push watsonxmcpregistry.azurecr.io/watsonx-mcp:latest

# Развертывание
az container create \
  --resource-group watsonx-mcp-rg \
  --name watsonx-mcp-container \
  --image watsonxmcpregistry.azurecr.io/watsonx-mcp:latest \
  --dns-name-label watsonx-mcp-unique-name \
  --ports 8000

# Получить URL
az container show \
  --resource-group watsonx-mcp-rg \
  --name watsonx-mcp-container \
  --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}" \
  --out table
```

### Heroku

```bash
# Установка Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Логин
heroku login
heroku container:login

# Создание приложения
heroku create your-app-name

# Сборка и публикация
heroku container:push web -a your-app-name

# Релиз
heroku container:release web -a your-app-name

# Открыть
heroku open -a your-app-name

# Логи
heroku logs --tail -a your-app-name
```

**Примечание**: Heroku требует процесс `web` на порту из переменной `$PORT`

### DigitalOcean App Platform

1. Зайдите в [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Нажмите "Create App"
3. Выберите GitHub репозиторий
4. DigitalOcean автоматически определит Dockerfile
5. Настройки:
   - **Port**: 8000
   - **Health Check Path**: `/health`
6. Выберите план
7. Нажмите "Launch App"

## 🔧 Продвинутая конфигурация

### Переменные окружения

Создайте файл `.env`:

```env
# Порт сервера
PORT=8000

# Путь к данным
DATA_FILE=/app/data/data.json
CONFIG_FILE=/app/data/config.json

# Логирование
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1
```

Используйте в docker-compose.yml:

```yaml
services:
  mcp-http-server:
    env_file:
      - .env
```

### Персистентность данных с именованными volumes

```yaml
volumes:
  mcp-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /path/to/your/data
```

### Использование secrets для конфиденциальных данных

```yaml
services:
  mcp-http-server:
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

### Health checks

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Multi-stage build для меньшего размера

```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
CMD ["python", "http_server.py"]
```

## 🔒 Безопасность

### Запуск от непривилегированного пользователя

Добавьте в Dockerfile:

```dockerfile
# Создаем пользователя
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

USER mcpuser
```

### Сканирование образа на уязвимости

```bash
# Используя Docker Scout
docker scout cves watsonx-mcp:latest

# Используя Trivy
trivy image watsonx-mcp:latest
```

## 📊 Мониторинг

### Логи

```bash
# Docker
docker logs -f watsonx-mcp

# Docker Compose
docker-compose logs -f mcp-http-server

# Экспорт логов в файл
docker logs watsonx-mcp > logs.txt 2>&1
```

### Метрики

```bash
# Статистика контейнера
docker stats watsonx-mcp

# Детальная информация
docker inspect watsonx-mcp
```

## 🔄 CI/CD

### GitHub Actions

Создайте `.github/workflows/docker-publish.yml`:

```yaml
name: Docker Build and Publish

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## 🆘 Troubleshooting

### Контейнер не запускается

```bash
# Проверьте логи
docker logs watsonx-mcp

# Запустите интерактивно
docker run -it watsonx-mcp:latest /bin/bash
```

### Проблемы с permissions

```bash
# Проверьте владельца файлов
docker exec watsonx-mcp ls -la /app

# Измените права
docker exec watsonx-mcp chown -R 1000:1000 /app/data
```

### Данные не сохраняются

```bash
# Проверьте volumes
docker volume ls
docker volume inspect mcp-data

# Проверьте mount points
docker inspect watsonx-mcp | grep -A 10 Mounts
```

## 📚 Полезные команды

```bash
# Удалить все остановленные контейнеры
docker container prune

# Удалить неиспользуемые образы
docker image prune -a

# Удалить неиспользуемые volumes
docker volume prune

# Полная очистка
docker system prune -a --volumes

# Экспорт образа
docker save watsonx-mcp:latest | gzip > watsonx-mcp.tar.gz

# Импорт образа
docker load < watsonx-mcp.tar.gz

# Копирование файлов из контейнера
docker cp watsonx-mcp:/app/data.json ./data.json.backup

# Копирование файлов в контейнер
docker cp ./config.json watsonx-mcp:/app/config.json
```

## 📖 Дополнительные ресурсы

- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)


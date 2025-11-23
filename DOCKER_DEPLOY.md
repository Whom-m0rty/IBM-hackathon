# 🐳 Docker Deployment Guide

Complete guide for deploying the MCP server in a Docker container and publishing to cloud platforms.

## 📦 Quick Start

### Local Run

```bash
# Build image
docker build -t watsonx-mcp:latest .

# Run container
docker run -d \
  --name watsonx-mcp \
  -p 8000:8000 \
  -v $(pwd)/data.json:/app/data.json \
  -v $(pwd)/config.json:/app/config.json \
  watsonx-mcp:latest

# Check operation
curl http://localhost:8000/health
```

### Docker Compose (recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🚀 Publishing to Container Registry

### 1. Docker Hub

```bash
# Login
docker login

# Tag image
docker tag watsonx-mcp:latest YOUR_USERNAME/watsonx-mcp:latest
docker tag watsonx-mcp:latest YOUR_USERNAME/watsonx-mcp:v1.0.0

# Publish
docker push YOUR_USERNAME/watsonx-mcp:latest
docker push YOUR_USERNAME/watsonx-mcp:v1.0.0

# Run from Docker Hub
docker run -d -p 8000:8000 YOUR_USERNAME/watsonx-mcp:latest
```

### 2. GitHub Container Registry (ghcr.io)

```bash
# Login (use Personal Access Token with write:packages permissions)
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin

# Tag
docker tag watsonx-mcp:latest ghcr.io/YOUR_GITHUB_USERNAME/watsonx-mcp:latest
docker tag watsonx-mcp:latest ghcr.io/YOUR_GITHUB_USERNAME/watsonx-mcp:v1.0.0

# Publish
docker push ghcr.io/YOUR_GITHUB_USERNAME/watsonx-mcp:latest
docker push ghcr.io/YOUR_GITHUB_USERNAME/watsonx-mcp:v1.0.0

# Run from GHCR
docker run -d -p 8000:8000 ghcr.io/YOUR_GITHUB_USERNAME/watsonx-mcp:latest
```

### 3. Google Container Registry (gcr.io)

```bash
# Setup gcloud
gcloud auth configure-docker

# Tag
docker tag watsonx-mcp:latest gcr.io/YOUR_PROJECT_ID/watsonx-mcp:latest

# Publish
docker push gcr.io/YOUR_PROJECT_ID/watsonx-mcp:latest

# Run
docker run -d -p 8000:8000 gcr.io/YOUR_PROJECT_ID/watsonx-mcp:latest
```

### 4. Amazon ECR

```bash
# Login
aws ecr get-login-password --region YOUR_REGION | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com

# Create repository (if not already created)
aws ecr create-repository --repository-name watsonx-mcp --region YOUR_REGION

# Tag
docker tag watsonx-mcp:latest YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/watsonx-mcp:latest

# Publish
docker push YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/watsonx-mcp:latest
```

## ☁️ Cloud Deployment

### Render.com

1. Create account at [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Settings:
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Port**: 8000
   - **Health Check Path**: `/health`
5. Add environment variables (if needed)
6. Click "Create Web Service"

**Cost**: Free tier available

### Railway.app

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Open in browser
railway open
```

**Dockerfile will be automatically detected and used**

### Google Cloud Run

```bash
# Build and publish
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/watsonx-mcp

# Deploy
gcloud run deploy watsonx-mcp \
  --image gcr.io/YOUR_PROJECT_ID/watsonx-mcp \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000

# Get URL
gcloud run services describe watsonx-mcp --region us-central1 --format 'value(status.url)'
```

**Cloud Run Features:**
- Automatic scaling
- Pay per use
- HTTPS by default

### AWS App Runner

1. Publish image to Amazon ECR (see above)
2. Open [AWS App Runner Console](https://console.aws.amazon.com/apprunner)
3. Click "Create service"
4. Select "Container registry" → "Amazon ECR"
5. Select your image
6. Settings:
   - **Port**: 8000
   - **Health check path**: `/health`
7. Create service

### Azure Container Instances

```bash
# Create resource group
az group create --name watsonx-mcp-rg --location eastus

# Create container registry
az acr create --resource-group watsonx-mcp-rg --name watsonxmcpregistry --sku Basic

# Login to registry
az acr login --name watsonxmcpregistry

# Tag
docker tag watsonx-mcp:latest watsonxmcpregistry.azurecr.io/watsonx-mcp:latest

# Publish
docker push watsonxmcpregistry.azurecr.io/watsonx-mcp:latest

# Deploy
az container create \
  --resource-group watsonx-mcp-rg \
  --name watsonx-mcp-container \
  --image watsonxmcpregistry.azurecr.io/watsonx-mcp:latest \
  --dns-name-label watsonx-mcp-unique-name \
  --ports 8000

# Get URL
az container show \
  --resource-group watsonx-mcp-rg \
  --name watsonx-mcp-container \
  --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}" \
  --out table
```

### Heroku

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login
heroku container:login

# Create app
heroku create your-app-name

# Build and publish
heroku container:push web -a your-app-name

# Release
heroku container:release web -a your-app-name

# Open
heroku open -a your-app-name

# Logs
heroku logs --tail -a your-app-name
```

**Note**: Heroku requires `web` process on port from `$PORT` variable

### DigitalOcean App Platform

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Select GitHub repository
4. DigitalOcean will automatically detect Dockerfile
5. Settings:
   - **Port**: 8000
   - **Health Check Path**: `/health`
6. Select plan
7. Click "Launch App"

## 🔧 Advanced Configuration

### Environment Variables

Create `.env` file:

```env
# Server port
PORT=8000

# Data path
DATA_FILE=/app/data/data.json
CONFIG_FILE=/app/data/config.json

# Logging
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1
```

Use in docker-compose.yml:

```yaml
services:
  mcp-http-server:
    env_file:
      - .env
```

### Data Persistence with Named Volumes

```yaml
volumes:
  mcp-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /path/to/your/data
```

### Using Secrets for Sensitive Data

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

### Health Checks

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Multi-stage Build for Smaller Size

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

## 🔒 Security

### Run as Non-privileged User

Add to Dockerfile:

```dockerfile
# Create user
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

USER mcpuser
```

### Scan Image for Vulnerabilities

```bash
# Using Docker Scout
docker scout cves watsonx-mcp:latest

# Using Trivy
trivy image watsonx-mcp:latest
```

## 📊 Monitoring

### Logs

```bash
# Docker
docker logs -f watsonx-mcp

# Docker Compose
docker-compose logs -f mcp-http-server

# Export logs to file
docker logs watsonx-mcp > logs.txt 2>&1
```

### Metrics

```bash
# Container statistics
docker stats watsonx-mcp

# Detailed information
docker inspect watsonx-mcp
```

## 🔄 CI/CD

### GitHub Actions

Create `.github/workflows/docker-publish.yml`:

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

### Container Won't Start

```bash
# Check logs
docker logs watsonx-mcp

# Run interactively
docker run -it watsonx-mcp:latest /bin/bash
```

### Permission Issues

```bash
# Check file ownership
docker exec watsonx-mcp ls -la /app

# Change permissions
docker exec watsonx-mcp chown -R 1000:1000 /app/data
```

### Data Not Persisting

```bash
# Check volumes
docker volume ls
docker volume inspect mcp-data

# Check mount points
docker inspect watsonx-mcp | grep -A 10 Mounts
```

## 📚 Useful Commands

```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Full cleanup
docker system prune -a --volumes

# Export image
docker save watsonx-mcp:latest | gzip > watsonx-mcp.tar.gz

# Import image
docker load < watsonx-mcp.tar.gz

# Copy files from container
docker cp watsonx-mcp:/app/data.json ./data.json.backup

# Copy files to container
docker cp ./config.json watsonx-mcp:/app/config.json
```

## 📖 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

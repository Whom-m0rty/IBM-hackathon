#!/bin/bash
# Quick Docker container launch with proper settings

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

IMAGE_NAME="watsonx-mcp"
CONTAINER_NAME="watsonx-mcp-server"
PORT="${PORT:-8000}"

echo -e "${GREEN}🚀 Starting watsonxMCP Docker container${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Stop existing container
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo -e "${YELLOW}⚠️  Stopping existing container...${NC}"
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
fi

# Check if image exists
if ! docker images ${IMAGE_NAME} | grep -q ${IMAGE_NAME}; then
    echo -e "${YELLOW}📦 Image not found, building...${NC}"
    docker build -t ${IMAGE_NAME}:latest .
fi

# Create data directory if it doesn't exist
mkdir -p ./data

# Start container
echo -e "${YELLOW}🐳 Starting container...${NC}"
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:8000 \
    -v "$(pwd)/data.json:/app/data.json" \
    -v "$(pwd)/config.json:/app/config.json" \
    -v "$(pwd)/data:/app/data" \
    -e PYTHONUNBUFFERED=1 \
    --restart unless-stopped \
    ${IMAGE_NAME}:latest

# Wait for startup
echo -e "${YELLOW}⏳ Waiting for server to start...${NC}"
sleep 3

# Check status
if docker ps | grep -q ${CONTAINER_NAME}; then
    echo -e "${GREEN}✅ Container started successfully!${NC}"
    echo ""
    echo "📊 Information:"
    echo "   Container:  ${CONTAINER_NAME}"
    echo "   Port:       ${PORT}"
    echo "   URL:        http://localhost:${PORT}"
    echo "   API Docs:   http://localhost:${PORT}/docs"
    echo "   Health:     http://localhost:${PORT}/health"
    echo ""
    echo "🔧 Useful commands:"
    echo "   Logs:          docker logs -f ${CONTAINER_NAME}"
    echo "   Stop:          docker stop ${CONTAINER_NAME}"
    echo "   Restart:       docker restart ${CONTAINER_NAME}"
    echo "   Remove:        docker rm -f ${CONTAINER_NAME}"
    echo "   Shell access:  docker exec -it ${CONTAINER_NAME} /bin/bash"
    echo ""
    
    # Test health endpoint
    echo -e "${YELLOW}🏥 Health check...${NC}"
    sleep 2
    if curl -s http://localhost:${PORT}/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Server is running correctly!${NC}"
    else
        echo -e "${YELLOW}⚠️  Unable to connect to health endpoint${NC}"
        echo "Check logs: docker logs ${CONTAINER_NAME}"
    fi
else
    echo -e "${RED}❌ Error starting container${NC}"
    echo "Logs:"
    docker logs ${CONTAINER_NAME}
    exit 1
fi


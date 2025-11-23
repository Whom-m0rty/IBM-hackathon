#!/bin/bash
# Script for building and publishing Docker image

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="watsonx-mcp"
VERSION="${1:-latest}"
REGISTRY="${DOCKER_REGISTRY:-docker.io}"  # Docker Hub by default
USERNAME="${DOCKER_USERNAME}"

echo -e "${GREEN}🐳 Building Docker image for watsonxMCP${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}❌ Error: Dockerfile not found${NC}"
    exit 1
fi

# Build image
echo -e "${YELLOW}📦 Building image...${NC}"
docker build -t ${IMAGE_NAME}:${VERSION} .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Image built successfully: ${IMAGE_NAME}:${VERSION}${NC}"
else
    echo -e "${RED}❌ Error building image${NC}"
    exit 1
fi

# Tag image
echo -e "${YELLOW}🏷️  Tagging image...${NC}"
docker tag ${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}:latest

# Show image size
echo -e "${YELLOW}📊 Image size:${NC}"
docker images ${IMAGE_NAME} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo ""
echo -e "${GREEN}✨ Build complete!${NC}"
echo ""
echo "Available commands:"
echo "  Run locally:           docker run -d -p 8000:8000 ${IMAGE_NAME}:${VERSION}"
echo "  Run with compose:      docker-compose up -d"
echo "  View logs:             docker logs -f ${IMAGE_NAME}"
echo ""

# Optional publishing
if [ ! -z "$USERNAME" ]; then
    echo -e "${YELLOW}📤 Do you want to publish the image? (y/n)${NC}"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${YELLOW}🔐 Logging into ${REGISTRY}...${NC}"
        docker login ${REGISTRY}
        
        # Tag for registry
        FULL_IMAGE="${REGISTRY}/${USERNAME}/${IMAGE_NAME}"
        docker tag ${IMAGE_NAME}:${VERSION} ${FULL_IMAGE}:${VERSION}
        docker tag ${IMAGE_NAME}:${VERSION} ${FULL_IMAGE}:latest
        
        echo -e "${YELLOW}📤 Publishing image...${NC}"
        docker push ${FULL_IMAGE}:${VERSION}
        docker push ${FULL_IMAGE}:latest
        
        echo -e "${GREEN}✅ Image published:${NC}"
        echo "   ${FULL_IMAGE}:${VERSION}"
        echo "   ${FULL_IMAGE}:latest"
        echo ""
        echo "To use:"
        echo "   docker pull ${FULL_IMAGE}:${VERSION}"
        echo "   docker run -d -p 8000:8000 ${FULL_IMAGE}:${VERSION}"
    fi
else
    echo -e "${YELLOW}💡 To publish, set environment variables:${NC}"
    echo "   export DOCKER_USERNAME=your-username"
    echo "   export DOCKER_REGISTRY=docker.io  # or ghcr.io, gcr.io, etc."
    echo "   ./docker-build.sh ${VERSION}"
fi


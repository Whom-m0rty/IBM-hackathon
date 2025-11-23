#!/bin/bash
# Скрипт для сборки и публикации Docker образа

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Конфигурация
IMAGE_NAME="watsonx-mcp"
VERSION="${1:-latest}"
REGISTRY="${DOCKER_REGISTRY:-docker.io}"  # По умолчанию Docker Hub
USERNAME="${DOCKER_USERNAME}"

echo -e "${GREEN}🐳 Сборка Docker образа для watsonxMCP${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Проверка наличия Dockerfile
if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}❌ Ошибка: Dockerfile не найден${NC}"
    exit 1
fi

# Сборка образа
echo -e "${YELLOW}📦 Сборка образа...${NC}"
docker build -t ${IMAGE_NAME}:${VERSION} .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Образ успешно собран: ${IMAGE_NAME}:${VERSION}${NC}"
else
    echo -e "${RED}❌ Ошибка при сборке образа${NC}"
    exit 1
fi

# Тегирование образа
echo -e "${YELLOW}🏷️  Тегирование образа...${NC}"
docker tag ${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}:latest

# Показываем размер образа
echo -e "${YELLOW}📊 Размер образа:${NC}"
docker images ${IMAGE_NAME} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo ""
echo -e "${GREEN}✨ Сборка завершена!${NC}"
echo ""
echo "Доступные команды:"
echo "  Запустить локально:    docker run -d -p 8000:8000 ${IMAGE_NAME}:${VERSION}"
echo "  Запустить compose:     docker-compose up -d"
echo "  Просмотр логов:        docker logs -f ${IMAGE_NAME}"
echo ""

# Опциональная публикация
if [ ! -z "$USERNAME" ]; then
    echo -e "${YELLOW}📤 Хотите опубликовать образ? (y/n)${NC}"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${YELLOW}🔐 Вход в ${REGISTRY}...${NC}"
        docker login ${REGISTRY}
        
        # Тегирование для registry
        FULL_IMAGE="${REGISTRY}/${USERNAME}/${IMAGE_NAME}"
        docker tag ${IMAGE_NAME}:${VERSION} ${FULL_IMAGE}:${VERSION}
        docker tag ${IMAGE_NAME}:${VERSION} ${FULL_IMAGE}:latest
        
        echo -e "${YELLOW}📤 Публикация образа...${NC}"
        docker push ${FULL_IMAGE}:${VERSION}
        docker push ${FULL_IMAGE}:latest
        
        echo -e "${GREEN}✅ Образ опубликован:${NC}"
        echo "   ${FULL_IMAGE}:${VERSION}"
        echo "   ${FULL_IMAGE}:latest"
        echo ""
        echo "Для использования:"
        echo "   docker pull ${FULL_IMAGE}:${VERSION}"
        echo "   docker run -d -p 8000:8000 ${FULL_IMAGE}:${VERSION}"
    fi
else
    echo -e "${YELLOW}💡 Для публикации установите переменные:${NC}"
    echo "   export DOCKER_USERNAME=your-username"
    echo "   export DOCKER_REGISTRY=docker.io  # или ghcr.io, gcr.io и т.д."
    echo "   ./docker-build.sh ${VERSION}"
fi


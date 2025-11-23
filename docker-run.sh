#!/bin/bash
# Быстрый запуск Docker контейнера с правильными настройками

set -e

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

IMAGE_NAME="watsonx-mcp"
CONTAINER_NAME="watsonx-mcp-server"
PORT="${PORT:-8000}"

echo -e "${GREEN}🚀 Запуск watsonxMCP Docker контейнера${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Остановка существующего контейнера
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo -e "${YELLOW}⚠️  Остановка существующего контейнера...${NC}"
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
fi

# Проверка наличия образа
if ! docker images ${IMAGE_NAME} | grep -q ${IMAGE_NAME}; then
    echo -e "${YELLOW}📦 Образ не найден, запускаем сборку...${NC}"
    docker build -t ${IMAGE_NAME}:latest .
fi

# Создание директории для данных если не существует
mkdir -p ./data

# Запуск контейнера
echo -e "${YELLOW}🐳 Запуск контейнера...${NC}"
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:8000 \
    -v "$(pwd)/data.json:/app/data.json" \
    -v "$(pwd)/config.json:/app/config.json" \
    -v "$(pwd)/data:/app/data" \
    -e PYTHONUNBUFFERED=1 \
    --restart unless-stopped \
    ${IMAGE_NAME}:latest

# Ожидание запуска
echo -e "${YELLOW}⏳ Ожидание запуска сервера...${NC}"
sleep 3

# Проверка статуса
if docker ps | grep -q ${CONTAINER_NAME}; then
    echo -e "${GREEN}✅ Контейнер успешно запущен!${NC}"
    echo ""
    echo "📊 Информация:"
    echo "   Контейнер:  ${CONTAINER_NAME}"
    echo "   Порт:       ${PORT}"
    echo "   URL:        http://localhost:${PORT}"
    echo "   API Docs:   http://localhost:${PORT}/docs"
    echo "   Health:     http://localhost:${PORT}/health"
    echo ""
    echo "🔧 Полезные команды:"
    echo "   Логи:          docker logs -f ${CONTAINER_NAME}"
    echo "   Остановить:    docker stop ${CONTAINER_NAME}"
    echo "   Рестарт:       docker restart ${CONTAINER_NAME}"
    echo "   Удалить:       docker rm -f ${CONTAINER_NAME}"
    echo "   Войти в sh:    docker exec -it ${CONTAINER_NAME} /bin/bash"
    echo ""
    
    # Тест health endpoint
    echo -e "${YELLOW}🏥 Проверка здоровья...${NC}"
    sleep 2
    if curl -s http://localhost:${PORT}/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Сервер работает корректно!${NC}"
    else
        echo -e "${YELLOW}⚠️  Не удалось подключиться к health endpoint${NC}"
        echo "Проверьте логи: docker logs ${CONTAINER_NAME}"
    fi
else
    echo -e "${RED}❌ Ошибка при запуске контейнера${NC}"
    echo "Логи:"
    docker logs ${CONTAINER_NAME}
    exit 1
fi


#!/bin/bash
# Скрипт для тестирования HTTP API

BASE_URL="${1:-http://localhost:8000}"
EMAIL="test@company.com"
MENTOR_EMAIL="mentor@company.com"

echo "🧪 Тестирование Onboarding Checklist API"
echo "URL: $BASE_URL"
echo ""

echo "=== 1. Health Check ==="
curl -s "$BASE_URL/health" | jq
echo ""

echo "=== 2. Получаем полный чек-лист ==="
curl -s "$BASE_URL/api/checklist" | jq
echo ""

echo "=== 3. Получаем прогресс пользователя (создается автоматически) ==="
curl -s "$BASE_URL/api/users/$EMAIL/progress" | jq
echo ""

echo "=== 4. Отмечаем задачу 1 как выполненную ==="
curl -s -X POST "$BASE_URL/api/users/tasks/complete" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"task_id\": 1}" | jq
echo ""

echo "=== 5. Отмечаем задачу 2 как выполненную ==="
curl -s -X POST "$BASE_URL/api/users/tasks/complete" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"task_id\": 2}" | jq
echo ""

echo "=== 6. Проверяем обновленный прогресс ==="
curl -s "$BASE_URL/api/users/$EMAIL/progress" | jq '.progress_percentage, .completed_tasks'
echo ""

echo "=== 7. Пробуем невалидный task_id (должна быть ошибка) ==="
curl -s -X POST "$BASE_URL/api/users/tasks/complete" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"task_id\": 999}" | jq
echo ""

echo "=== 8. Получаем всех пользователей (для ментора) ==="
echo "Попытка с mentor email из config.json..."
curl -s -X POST "$BASE_URL/api/admin/users" \
  -H "Content-Type: application/json" \
  -d "{\"mentor_email\": \"$MENTOR_EMAIL\"}" | jq
echo ""

echo "✅ Тестирование завершено!"
echo ""
echo "💡 Swagger документация доступна на: $BASE_URL/docs"


#!/bin/bash
# Script for testing HTTP API

BASE_URL="${1:-http://localhost:8000}"
EMAIL="test@company.com"
MENTOR_EMAIL="mentor@company.com"

echo "🧪 Testing Onboarding Checklist API"
echo "URL: $BASE_URL"
echo ""

echo "=== 1. Health Check ==="
curl -s "$BASE_URL/health" | jq
echo ""

echo "=== 2. Get full checklist ==="
curl -s "$BASE_URL/api/checklist" | jq
echo ""

echo "=== 3. Get user progress (created automatically) ==="
curl -s "$BASE_URL/api/users/$EMAIL/progress" | jq
echo ""

echo "=== 4. Mark task 1 as completed ==="
curl -s -X POST "$BASE_URL/api/users/tasks/complete" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"task_id\": 1}" | jq
echo ""

echo "=== 5. Mark task 2 as completed ==="
curl -s -X POST "$BASE_URL/api/users/tasks/complete" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"task_id\": 2}" | jq
echo ""

echo "=== 6. Check updated progress ==="
curl -s "$BASE_URL/api/users/$EMAIL/progress" | jq '.progress_percentage, .completed_tasks'
echo ""

echo "=== 7. Try invalid task_id (should error) ==="
curl -s -X POST "$BASE_URL/api/users/tasks/complete" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"task_id\": 999}" | jq
echo ""

echo "=== 8. Get all users (for mentor) ==="
echo "Attempting with mentor email from config.json..."
curl -s -X POST "$BASE_URL/api/admin/users" \
  -H "Content-Type: application/json" \
  -d "{\"mentor_email\": \"$MENTOR_EMAIL\"}" | jq
echo ""

echo "✅ Testing complete!"
echo ""
echo "💡 Swagger documentation available at: $BASE_URL/docs"


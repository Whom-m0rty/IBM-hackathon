# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения
COPY server.py .
COPY http_server.py .
COPY streamlit_app.py .
COPY agent_prompt.txt .
COPY agent_prompt_simple.txt .
COPY openapi.json .

# Копируем конфигурационные файлы (если они существуют, иначе создаем дефолтные)
COPY config.json* ./
COPY data.json* ./

# Создаем дефолтные файлы, если они не были скопированы
RUN if [ ! -f config.json ]; then echo '{"mentors": ["mentor@company.com", "admin@company.com"]}' > config.json; fi
RUN if [ ! -f data.json ]; then echo '{}' > data.json; fi

# Создаем volume для персистентности данных
VOLUME ["/app/data"]

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app/data

# Экспонируем порт для HTTP API (если используется)
EXPOSE 8000

# Устанавливаем порт для Streamlit (если используется)
EXPOSE 8501

# Команда по умолчанию - запуск HTTP сервера
# Можно переопределить при запуске контейнера
CMD ["python", "http_server.py"]


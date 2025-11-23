# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY server.py .
COPY http_server.py .
COPY streamlit_app.py .
COPY agent_prompt.txt .
COPY agent_prompt_simple.txt .
COPY openapi.json .

# Copy configuration files (if they exist, otherwise create defaults)
COPY config.json* ./
COPY data.json* ./

# Create default files if they weren't copied
RUN if [ ! -f config.json ]; then echo '{"mentors": ["mentor@company.com", "admin@company.com"]}' > config.json; fi
RUN if [ ! -f data.json ]; then echo '{}' > data.json; fi

# Create volume for data persistence
VOLUME ["/app/data"]

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app/data

# Expose port for HTTP API (if used)
EXPOSE 8000

# Expose port for Streamlit (if used)
EXPOSE 8501

# Default command - run HTTP server
# Can be overridden when starting container
CMD ["python", "http_server.py"]


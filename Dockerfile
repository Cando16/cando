FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if required by any python package
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject config and install dependencies directly
# (Using pip to install packages directly to avoid build-backend issues)
RUN pip install --no-cache-dir fastapi uvicorn pydantic pydantic-settings python-dotenv httpx python-docx pypdf python-multipart

# Copy application code
COPY backend/ ./backend/

# Expose port 8080 (standard for Cloud Run, Render, etc.)
EXPOSE 8080

# Set Python path
ENV PYTHONPATH=/app

# Start the FastAPI application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]

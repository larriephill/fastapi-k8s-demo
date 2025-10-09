# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Non-root user
RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app

# Install runtime deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source last for caching
COPY app ./app

EXPOSE 8000
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

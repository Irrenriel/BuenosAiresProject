# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set environment variables:
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD requirements.txt .

# Install dependencies:
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip & pip install --no-cache-dir -r requirements.txt

ADD . .

# Run app:
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
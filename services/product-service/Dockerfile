FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Shared library is mounted in docker-compose, but we need the folder to exist
RUN mkdir -p /app/shared

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

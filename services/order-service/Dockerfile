FROM python:3.11-slim

# Install uv
RUN pip install uv

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY requirements.txt .

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --no-cache -r requirements.txt

COPY . .

# Shared library is mounted in docker-compose, but we need the folder to exist
RUN mkdir -p /app/shared

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

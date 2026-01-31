# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv sync --frozen --no-dev --no-install-project

# Финальный образ
FROM python:3.12-slim

WORKDIR /app

# Копируем виртуальное окружение из builder
COPY --from=builder /app/.venv /app/.venv

# Добавляем venv в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Копируем код приложения
COPY . .

# Порт приложения
EXPOSE 8000

# Запуск приложения
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]

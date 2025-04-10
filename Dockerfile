FROM python:3.12-slim as builder

RUN pip install poetry

COPY backend/pyproject.toml backend/poetry.lock ./

# Настройка Poetry для создания виртуального окружения
RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi

FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    tzdata \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /usr/local/lib/python3.12/site-packages

WORKDIR /app

COPY ./ ./
#COPY .env ./

RUN chown -R appuser:appuser /app

USER appuser

ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Проверка наличия uvicorn
RUN pip show uvicorn || echo "Uvicorn is not installed!"

COPY --chmod=755 docker-entrypoint.sh /usr/local/bin/
# RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]

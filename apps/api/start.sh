#!/bin/bash
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting server on port $PORT..."
exec uvicorn api.main:app --host 0.0.0.0 --port "$PORT" --timeout-keep-alive 75

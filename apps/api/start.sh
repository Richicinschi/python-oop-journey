#!/bin/bash
# Start the FastAPI development server

set -e

export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

./venv/bin/python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

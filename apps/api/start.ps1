#!/usr/bin/env pwsh
# Start the FastAPI development server

$env:PYTHONDONTWRITEBYTECODE = 1
$env:PYTHONUNBUFFERED = 1

& .\venv\Scripts\python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

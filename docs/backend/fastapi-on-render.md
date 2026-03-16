# FastAPI on Render

## Overview

FastAPI is our Python web framework. It runs on Render as a web service.

## Project Structure

```
apps/api/
├── api/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── config.py         # Settings
│   ├── database.py       # SQLAlchemy setup
│   ├── models/           # Database models
│   ├── routers/          # API endpoints
│   ├── services/         # Business logic
│   └── middleware/       # Custom middleware
├── migrations/           # Alembic migrations
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container config
└── alembic.ini          # Migration config
```

## Render Configuration

### Build Command
```bash
pip install -r apps/api/requirements.txt
```

### Start Command
```bash
cd apps/api && alembic upgrade head && uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

**Why this order?**
1. `cd apps/api` - Move to API directory
2. `alembic upgrade head` - Run database migrations
3. `uvicorn ...` - Start the web server

### Port Binding

**CRITICAL:** Must bind to `0.0.0.0` and use `$PORT`:
```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

## Main Application (main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Python OOP Journey API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(users.router, prefix="/api/v1/users")
# ... etc

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}
```

## Dependencies (requirements.txt)

Key dependencies:
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.29.0
alembic>=1.12.0
redis>=5.0.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
httpx>=0.25.0
```

## Database Setup

### Async SQLAlchemy
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine(
    "postgresql+asyncpg://...",
    echo=False,
    pool_size=10,
    max_overflow=20,
)
```

### Getting DB Session
```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

## Environment Variables

Required:
```
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=rediss://...
SECRET_KEY=...
JWT_SECRET=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
FRONTEND_URL=https://...
ENVIRONMENT=production
```

## Common Issues

### "Module not found"
- Check `requirements.txt` has all dependencies
- Verify import paths are correct

### "Port already in use"
- Use `$PORT` environment variable
- Don't hardcode port numbers

### "Database connection failed"
- Check `DATABASE_URL` format
- Verify SSL settings (`ssl=require`)
- Check network access

### "Migration failed"
- Check migration order
- Verify models are imported in `env.py`
- Check for syntax errors

## Testing Locally

```bash
cd apps/api

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Test API
curl http://localhost:8000/api/v1/health
```

## Health Check Endpoint

Add to `main.py`:
```python
@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}
```

Configure in Render Dashboard → Advanced → Health Check Path: `/api/v1/health`

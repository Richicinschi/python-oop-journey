# Troubleshooting Checklist

Use this checklist when deployments fail.

## Step 1: Check Logs

In Render Dashboard:
1. Go to your service
2. Click **Logs** tab
3. Search for "error" or "Error"
4. Find the first red error message

## Step 2: Identify Error Type

### Build Errors (during `pip install`)
| Symptom | Solution |
|---------|----------|
| "Module not found" | Add to `requirements.txt` |
| "Syntax error" | Fix Python code |
| "Version conflict" | Pin versions in requirements |

### Migration Errors (during `alembic upgrade`)
| Symptom | Solution |
|---------|----------|
| "relation does not exist" | Create parent table first |
| "Multiple head revisions" | Fix `down_revision` chain |
| "Column already exists" | Migration already ran, skip |
| "UndefinedTable" | Check table creation order |

### Runtime Errors (during `uvicorn` start)
| Symptom | Solution |
|---------|----------|
| "Port not bound" | Add `--host 0.0.0.0 --port $PORT` |
| "Address already in use" | Use `$PORT` env var |
| "Module not found" | Check import paths |
| "Database connection failed" | Check `DATABASE_URL` |

### Database Connection Errors
| Symptom | Solution |
|---------|----------|
| "sslmode unexpected" | Use `ssl=require` not `sslmode` |
| "Connection refused" | Check host/port |
| "Authentication failed" | Wrong password |
| "Database does not exist" | Check database name |

## Step 3: Common Fixes

### Fix 1: Check Environment Variables
All required env vars set?
- DATABASE_URL
- REDIS_URL
- SECRET_KEY
- JWT_SECRET
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET

### Fix 2: Check Migration Chain
```bash
# Check current migration
alembic current

# View history
alembic history

# Check for multiple heads
alembic heads
```

### Fix 3: Test Database Connection
```python
# Test script
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def test():
    engine = create_async_engine("your-url")
    async with engine.connect() as conn:
        result = await conn.execute("SELECT 1")
        print(result.scalar())

asyncio.run(test())
```

### Fix 4: Check Import Errors
```python
# Test imports
python -c "from api.models import User, Activity"
```

## Step 4: Redeploy

After fixing:
```bash
git add .
git commit -m "Fix: description"
git push
```

Render will auto-redeploy.

## Quick Fixes Reference

### "Multiple head revisions"
```python
# In migration file, fix down_revision:
down_revision = 'correct_previous_migration'
```

### "relation 'users' does not exist"
```python
# Create users table BEFORE auth_tokens
# In migration, reorder operations
```

### "sslmode unexpected keyword"
```
# Change URL from:
postgresql+asyncpg://...?sslmode=require
# To:
postgresql+asyncpg://...?ssl=require
```

### "Cannot determine CockroachDB version"
```python
# Already patched in database.py
# Returns (14, 0, 0) for compatibility
```

## Getting Help

1. Check Render docs: https://render.com/docs
2. Check CockroachDB docs: https://www.cockroachlabs.com/docs
3. Search error message on Google/Stack Overflow
4. Check our docs in `/docs` folder

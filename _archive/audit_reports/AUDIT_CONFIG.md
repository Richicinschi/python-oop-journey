# Environment Configuration Audit Report

**Date:** 2026-03-12  
**Application:** Python OOP Journey API  
**Target:** Production Deployment on Render  
**Status:** ❌ CRITICAL ISSUES FOUND

---

## 🚨 CRITICAL ISSUES

### 1. DATABASE_URL Format Issues

**Problem:** The default DATABASE_URL format is incompatible with CockroachDB Cloud.

**Current (config.py line 40):**
```python
default="postgresql+asyncpg://postgres:postgres@localhost:5432/oop_journey"
```

**Required for CockroachDB Cloud:**
```
postgresql+asyncpg://<user>:<password>@<host>:26257/<database>?ssl=require
```

**Specific Issues:**
- ❌ Port should be `26257` (not 5432) for CockroachDB
- ❌ Must use `ssl=require` parameter (NOT `sslmode=require`)
- ❌ Missing SSL parameter entirely in defaults

**Files Affected:**
- `website-playground/apps/api/api/config.py` (line 40)
- `website-playground/apps/api/alembic.ini` (line 60)
- `website-playground/apps/api/.env.example` (line 13)

---

### 2. Unsafe Default Values for Production

**SECRET_KEY (config.py line 24):**
```python
secret_key: str = Field(default="dev-secret", description="...")
```
- ❌ Default is "dev-secret" - extremely unsafe for production
- ❌ No minimum length validation
- ❌ Should fail startup if not set in production

**CORS Origins (config.py line 31):**
```python
allowed_origins_raw: str = Field(default="http://localhost:3000", alias="ALLOWED_ORIGINS")
```
- ❌ Defaults to localhost - will break production frontend
- ❌ Should be explicitly set for production

**ENVIRONMENT (config.py line 23):**
```python
environment: str = "development"
```
- ❌ Defaults to "development" - could expose debug endpoints

---

### 3. Missing Required Environment Variables in .env.example

The following **required** environment variables are used in code but NOT documented in `.env.example`:

| Variable | Used In | Required For |
|----------|---------|--------------|
| `GOOGLE_CLIENT_ID` | `google_auth.py:22` | Google OAuth login |
| `GOOGLE_CLIENT_SECRET` | `google_auth.py:23` | Google OAuth callback |
| `FRONTEND_URL` | `google_auth.py:24` | OAuth redirect URLs |
| `SENDGRID_API_KEY` | `config.py:57` | Production email sending |
| `OPENAI_API_KEY` | `config.py:74` | AI hints feature |
| `ANTHROPIC_API_KEY` | `config.py:75` | AI hints (optional) |
| `MAGIC_LINK_BASE_URL` | `config.py:67` | Magic link URLs |

---

### 4. Render Start Command Issues

**Current start.sh (development only):**
```bash
#!/bin/bash
./venv/bin/python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Problems:**
- ❌ Uses `--reload` (development only)
- ❌ Hardcoded port 8000 (should use `$PORT`)
- ❌ **Missing migrations:** No `alembic upgrade head`
- ❌ No working directory setup for Render

**Required Render Start Command:**
```bash
cd apps/api && alembic upgrade head && uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

---

### 5. CockroachDB Connection Issues

**Current database.py (lines 37-48):**
```python
connect_args = {"prepare_threshold": None}
if "cockroach" in settings.database_url.lower():
    connect_args["server_settings"] = {"application_name": "oop-journey"}
```

**Issues:**
- ✅ Version patch is present (lines 17-34) - GOOD
- ❌ SSL mode not explicitly set in connection args
- ❌ No connection retry logic for cloud disconnects

---

## 📋 REQUIRED ENVIRONMENT VARIABLES FOR PRODUCTION

### Tier 1: Critical (Application won't start)

| Variable | Format | Example |
|----------|--------|---------|
| `DATABASE_URL` | `postgresql+asyncpg://user:pass@host:26257/db?ssl=require` | See CockroachDB dashboard |
| `SECRET_KEY` | Min 32 random chars | `openssl rand -hex 32` |
| `ENVIRONMENT` | `production` | `production` |
| `REDIS_URL` | `redis://host:port/db` | Redis Cloud URL |

### Tier 2: Authentication (Required for login)

| Variable | Format | Where to Get |
|----------|--------|--------------|
| `GOOGLE_CLIENT_ID` | OAuth client ID | Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | OAuth client secret | Google Cloud Console |
| `FRONTEND_URL` | `https://your-app.vercel.app` | Vercel dashboard |
| `ALLOWED_ORIGINS` | Comma-separated URLs | Same as FRONTEND_URL |

### Tier 3: Features (Required for full functionality)

| Variable | Purpose | Provider |
|----------|---------|----------|
| `SENDGRID_API_KEY` | Magic link emails | SendGrid |
| `OPENAI_API_KEY` | AI hints/reviews | OpenAI |
| `MAGIC_LINK_BASE_URL` | Magic link URLs | Same as FRONTEND_URL |

---

## 🔧 REQUIRED CONFIGURATION CHANGES

### 1. Update config.py

Add production validation:

```python
@field_validator("secret_key")
@classmethod
def validate_secret_key(cls, v: str, info) -> str:
    """Ensure secret_key is safe for production."""
    values = info.data
    if values.get("environment") == "production":
        if v == "dev-secret" or len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 chars in production")
    return v

@field_validator("database_url")
@classmethod
def validate_database_url(cls, v: str, info) -> str:
    """Ensure DATABASE_URL uses correct format for CockroachDB."""
    if "cockroach" in v.lower() or ":26257" in v:
        # Check for common mistakes
        if "sslmode=" in v:
            raise ValueError("Use 'ssl=require' not 'sslmode=require' for CockroachDB")
        if ":5432" in v:
            raise ValueError("CockroachDB uses port 26257, not 5432")
    return v
```

### 2. Update .env.example

Add missing variables:

```bash
# =============================================================================
# Google OAuth (Required for authentication)
# =============================================================================
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
FRONTEND_URL=http://localhost:3000

# =============================================================================
# SendGrid (Required for production email)
# =============================================================================
SENDGRID_API_KEY=SG.xxx

# =============================================================================
# AI Integration (Required for hints)
# =============================================================================
OPENAI_API_KEY=sk-...
```

### 3. Create Production Start Script

Create `start-production.sh`:

```bash
#!/bin/bash
set -e

echo "Starting production server..."

# Run database migrations
echo "Running migrations..."
alembic upgrade head

# Start server with production settings
echo "Starting uvicorn..."
exec uvicorn api.main:app --host 0.0.0.0 --port "${PORT:-8000}" --workers 4
```

---

## ✅ RENDER DEPLOYMENT CHECKLIST

### Environment Variables to Set in Render Dashboard:

- [ ] `DATABASE_URL` - From CockroachDB Cloud (must include `?ssl=require`)
- [ ] `REDIS_URL` - From Redis Cloud or Upstash
- [ ] `SECRET_KEY` - Generate with `openssl rand -hex 32`
- [ ] `ENVIRONMENT` - Set to `production`
- [ ] `GOOGLE_CLIENT_ID` - From Google Cloud Console
- [ ] `GOOGLE_CLIENT_SECRET` - From Google Cloud Console
- [ ] `FRONTEND_URL` - Your Vercel frontend URL
- [ ] `ALLOWED_ORIGINS` - Same as FRONTEND_URL
- [ ] `SENDGRID_API_KEY` - From SendGrid
- [ ] `OPENAI_API_KEY` - From OpenAI (for AI features)
- [ ] `MAGIC_LINK_BASE_URL` - Same as FRONTEND_URL

### Build Command:
```bash
cd apps/api && pip install -r requirements.txt
```

### Start Command:
```bash
cd apps/api && alembic upgrade head && uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

---

## 🔍 VERIFICATION STEPS

After deployment, verify:

1. **Health check passes:**
   ```bash
   curl https://your-api.render.com/health
   ```

2. **Database connection works:**
   ```bash
   curl https://your-api.render.com/ready
   ```

3. **Google OAuth config returns:**
   ```bash
   curl https://your-api.render.com/api/v1/auth/google/config
   # Should show: {"client_id": "...", "enabled": true}
   ```

4. **No debug endpoints in production:**
   ```bash
   curl https://your-api.render.com/docs
   # Should return 404 in production
   ```

---

## 📝 FILES REQUIRING CHANGES

| File | Change Required |
|------|-----------------|
| `api/config.py` | Add validators, safer defaults |
| `api/.env.example` | Add missing env vars |
| `start.sh` | Create separate production script |
| `alembic.ini` | Update default SQLAlchemy URL |
| `Dockerfile` | Add `alembic upgrade head` to CMD |

---

## ⚠️ IMMEDIATE ACTION ITEMS

1. **BEFORE deploying to Render:**
   - Generate a strong SECRET_KEY
   - Get CockroachDB connection string with correct format
   - Verify DATABASE_URL uses `ssl=require` (not sslmode)
   - Verify DATABASE_URL uses port 26257

2. **Set all environment variables in Render dashboard BEFORE first deploy**

3. **Test database connection locally first:**
   ```bash
   cd website-playground/apps/api
   export DATABASE_URL="your-cockroachdb-url"
   python -c "from api.database import engine; print('Connection OK')"
   ```

---

**Audit Completed:** Configuration has CRITICAL issues that will cause production deployment failures. Address all items in this report before deploying.

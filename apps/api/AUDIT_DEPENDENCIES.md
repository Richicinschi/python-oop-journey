# Dependency Compatibility Audit Report

**Project:** website-playground/apps/api  
**Audit Date:** 2026-03-12  
**Auditor:** Dependency Compatibility Auditor

---

## Executive Summary

The `requirements.txt` is generally well-structured with most critical dependencies present. However, **1 CRITICAL missing dependency** was identified that will cause deployment failures, along with several version compatibility recommendations.

---

## 1. MISSING DEPENDENCIES (Critical)

### 🔴 CRITICAL: `sentry-sdk` is missing

**Location:** `api/monitoring.py` imports `sentry_sdk`

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
```

**Impact:** Application will fail to start with `ModuleNotFoundError` if Sentry is configured via `SENTRY_DSN` environment variable.

**Recommendation:**
```txt
sentry-sdk[fastapi]>=1.40.0
```

The `[fastapi]` extra includes FastAPI integration dependencies.

---

## 2. ASYNC SUPPORT CHECK

| Component | Status | Notes |
|-----------|--------|-------|
| SQLAlchemy | ⚠️ WARNING | Should use `sqlalchemy[asyncio]` extra |
| asyncpg | ✅ OK | Present at `>=0.29.0` |
| DB Operations | ✅ OK | All use `AsyncSession` |

### Issue: SQLAlchemy Async Extra

**Current:** `sqlalchemy>=2.0.25`

**Recommended:** `sqlalchemy[asyncio]>=2.0.25`

The `[asyncio]` extra ensures `greenlet` is installed, which is required for SQLAlchemy async operations.

---

## 3. VERSION COMPATIBILITY CHECK

### ✅ Compatible Versions

| Package | Version | Compatible With |
|---------|---------|-----------------|
| fastapi | >=0.110.0 | ✅ Pydantic v2+ |
| pydantic | >=2.6.0 | ✅ FastAPI 0.100+ |
| pydantic-settings | >=2.1.0 | ✅ Pydantic v2+ |

### ⚠️ Version Range Risks

**Celery + Kombu + Billiard Stack:**
- `celery[redis]>=5.3.0` pulls in kombu and billiard
- Using `>=` allows major version updates
- **Risk:** Celery 6.x may have breaking changes

**AI Libraries:**
- `openai>=1.30.0` - OpenAI SDK v1.x is stable
- `anthropic>=0.28.0` - Anthropic SDK pre-1.0, API may change

---

## 4. COCKROACHDB COMPATIBILITY

| Driver | Status | Compatible |
|--------|--------|------------|
| asyncpg | ✅ Present | ✅ Yes |
| psycopg2 | ✅ Not used | N/A |
| sqlalchemy[asyncio] | ⚠️ Missing extra | Should add |

**Current URL Pattern:** `postgresql+asyncpg://`

**CockroachDB Compatibility:** CockroachDB is PostgreSQL-wire compatible. The `database.py` includes a monkey-patch for CockroachDB version detection which is appropriate.

---

## 5. SECURITY DEPENDENCIES

| Package | Status | Purpose |
|---------|--------|---------|
| `python-jose[cryptography]` | ✅ Present | JWT signing/verification |
| `passlib[bcrypt]` | ✅ Present | Password hashing |

Both security dependencies are correctly specified with their crypto extras.

---

## 6. VERSION PINNING RECOMMENDATIONS

### For Production Stability

Current `>=` constraints allow automatic updates. Consider pinning for reproducible builds:

```txt
# Instead of:
fastapi>=0.110.0

# Use in production:
fastapi==0.115.0  # Pin to specific version
```

### Recommended Production Pins

```txt
# Core framework - pin for stability
fastapi==0.115.0
uvicorn[standard]==0.34.0
pydantic==2.10.0
pydantic-settings==2.7.0

# Database - critical for stability  
sqlalchemy[asyncio]==2.0.36
asyncpg==0.30.0
alembic==1.14.0

# Security - pin for compliance
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Async support
greenlet==3.1.0  # Required by sqlalchemy[asyncio]
```

---

## 7. DEPENDENCY ANALYSIS BY MODULE

| Module | Imports | In requirements.txt |
|--------|---------|---------------------|
| `api/main.py` | fastapi, sentry_sdk | ❌ sentry_sdk missing |
| `api/database.py` | sqlalchemy, asyncpg | ⚠️ needs [asyncio] extra |
| `api/services/auth.py` | jose, sqlalchemy | ✅ Yes |
| `api/services/ai_hints.py` | httpx, openai | ✅ Yes |
| `api/services/email.py` | httpx, smtplib | ✅ Yes |
| `api/celery_app.py` | celery | ✅ Yes |
| `api/monitoring.py` | sentry_sdk | ❌ MISSING |
| `migrations/env.py` | alembic, sqlalchemy | ✅ Yes |

---

## 8. OPTIONAL DEPENDENCIES NOTE

The following are present but may not be needed in minimal deployments:

| Package | Usage | Can Remove? |
|---------|-------|-------------|
| `flower` | Celery monitoring dashboard | Yes, if not using monitoring UI |
| `ast-decompiler` | Code analysis | Yes, if not doing code analysis |
| `psutil` | System resource monitoring | Yes, if not using health checks |
| `slowapi` | Rate limiting | Check if actually used |
| `limits` | Rate limiting | Check if actually used |

---

## 9. RECOMMENDED ACTIONS

### Immediate (Before Deployment)

1. **Add missing sentry-sdk:**
   ```txt
   sentry-sdk[fastapi]>=1.40.0
   ```

2. **Update SQLAlchemy to include asyncio extra:**
   ```txt
   sqlalchemy[asyncio]>=2.0.25
   ```

### Short-term (Production Hardening)

3. **Create separate requirements files:**
   - `requirements.txt` - Production pins
   - `requirements-dev.txt` - Development with test tools
   - `requirements-minimal.txt` - Core only

4. **Add dependency verification to CI:**
   ```bash
   pip install -r requirements.txt
   pip check  # Verify no conflicts
   python -c "import api.main"  # Smoke test
   ```

### Long-term

5. **Consider pip-tools or poetry** for deterministic dependency resolution
6. **Set up Dependabot** for automated security updates

---

## 10. UPDATED REQUIREMENTS.TXT

```txt
# FastAPI and web framework
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.9

# Data validation
pydantic>=2.6.0
pydantic-settings>=2.1.0
email-validator>=2.0.0

# Database
sqlalchemy[asyncio]>=2.0.25  # Added [asyncio] extra
alembic>=1.13.0
asyncpg>=0.29.0

# Redis
redis>=5.0.0

# Docker SDK
docker>=7.0.0

# Security
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4

# HTTP client
httpx>=0.27.0

# Rate limiting
slowapi>=0.1.9
limits>=3.0.0

# Task queue
celery[redis]>=5.3.0

# Testing
pytest>=8.0.0
pytest-asyncio>=0.23.0

# Development
python-dotenv>=1.0.0

# Monitoring
sentry-sdk[fastapi]>=1.40.0  # ADDED - was missing
flower>=2.0.0  # Celery monitoring (optional)

# Code analysis
ast-decompiler>=0.7.0  # Optional

# AI Integration
openai>=1.30.0
anthropic>=0.28.0

# Performance & Compression
brotli>=1.1.0
psutil>=5.9.0  # Optional - for health checks
```

---

## Summary

| Category | Count |
|----------|-------|
| Critical Missing | 1 (sentry-sdk) |
| Warnings | 1 (sqlalchemy[asyncio] extra) |
| Version Conflicts | 0 |
| Security Issues | 0 |

**Overall Assessment:** GOOD with minor fixes required before production deployment.

# Frontend-Backend Integration Audit Report

**Date:** 2026-03-12  
**Auditor:** Frontend Integration Auditor  
**Scope:** `website-playground/apps/web`

---

## Executive Summary

⚠️ **CRITICAL ISSUES FOUND:** 7 issues require immediate attention before frontend deployment.

| Severity | Count | Categories |
|----------|-------|------------|
| 🔴 Critical | 3 | Build config, Missing env files, CORS mismatch |
| 🟡 Warning | 3 | Inconsistent URLs, Missing Google OAuth config |
| 🔵 Info | 2 | Code organization improvements |

---

## 1. API URL Configuration Issues

### 🔴 CRITICAL: Inconsistent API Fallback URLs

**Problem:** Multiple fallback API URLs are defined across the codebase with different ports:

| File | Fallback URL | Issue |
|------|--------------|-------|
| `lib/api.ts` | `http://localhost:3001` | Inconsistent with auth files |
| `contexts/auth-context.tsx` | `http://localhost:8000` | **Correct** (matches backend) |
| `app/auth/login/page.tsx` | `http://localhost:8000` | **Correct** (matches backend) |
| `lib/verification-api.ts` | `http://localhost:3001` | Inconsistent with auth files |

**Impact:** During development without env vars, different parts of the app will try to connect to different ports (3001 vs 8000), causing authentication and API failures.

**Fix:** Standardize all fallback URLs to `http://localhost:8000` (backend default port):

```typescript
// lib/api.ts - Line 1
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// lib/verification-api.ts - Line 5
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
```

---

## 2. Build Configuration Issues

### 🔴 CRITICAL: Wrong Output Mode for Cloudflare Pages

**File:** `apps/web/next.config.js`

**Current Setting:**
```javascript
output: 'standalone',  // Line 4
```

**Problem:** 
- `standalone` mode is designed for Docker/containerized deployments
- Cloudflare Pages requires **static export** (`output: 'export'`)
- No `distDir` is specified (defaults to `.next/`)

**Required Changes:**
```javascript
const nextConfig = {
  // Production output configuration for Cloudflare Pages
  output: 'export',
  distDir: 'dist',
  // ... rest of config
};
```

**Impact:** Without this change, the build will not generate static files suitable for Cloudflare Pages deployment.

---

## 3. Missing Environment Variables

### 🔴 CRITICAL: Missing `.env.production` File

**Problem:** No `apps/web/.env.production` file exists.

**Required Content for `apps/web/.env.production`:**
```bash
# Next.js App Configuration
NEXT_PUBLIC_APP_URL=https://oopjourney.com

# API Configuration
NEXT_PUBLIC_API_URL=https://api.oopjourney.com

# Google OAuth (if using Google auth)
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com

# Feature Flags
NEXT_PUBLIC_ENABLE_AI_HINTS=true
NEXT_PUBLIC_ENABLE_PROGRESS_SYNC=true
```

### 🟡 WARNING: Missing Google Client ID Configuration

**Problem:** The backend has Google OAuth implementation (`api/routers/google_auth.py`), but no `NEXT_PUBLIC_GOOGLE_CLIENT_ID` is defined in any environment file.

**Files to Check:**
- Backend: `website-playground/apps/api/api/routers/google_auth.py`
- Frontend: No Google OAuth implementation found in login page (uses magic link only)

**Recommendation:** Either:
1. Remove Google OAuth if not needed, or
2. Add `NEXT_PUBLIC_GOOGLE_CLIENT_ID` to environment files and implement Google sign-in on frontend

---

## 4. CORS Configuration Mismatch

### 🔴 CRITICAL: Environment Variable Name Mismatch

**Backend Config** (`api/api/config.py`):
```python
allowed_origins_raw: str = Field(default="http://localhost:3000", alias="ALLOWED_ORIGINS")
```

**Production Template** (`website-playground/.env.production.example`):
```bash
CORS_ORIGINS=https://oopjourney.com,https://www.oopjourney.com
```

**Problem:** 
- Backend expects `ALLOWED_ORIGINS`
- Production template defines `CORS_ORIGINS`
- These don't match! The backend will use default `http://localhost:3000` in production.

**Fix Options:**

**Option A:** Update backend config to use `CORS_ORIGINS`:
```python
allowed_origins_raw: str = Field(default="http://localhost:3000", alias="CORS_ORIGINS")
```

**Option B:** Update `.env.production.example` and documentation:
```bash
ALLOWED_ORIGINS=https://oopjourney.com,https://www.oopjourney.com
```

---

## 5. Cloudflare Pages Configuration

### 🟡 WARNING: No Cloudflare Pages Config Found

**Missing Files:**
- `wrangler.toml` - Wrangler configuration
- `apps/web/wrangler.toml` - Web-specific Wrangler config

**Required Configuration:**

Create `website-playground/apps/web/wrangler.toml`:
```toml
name = "oopjourney-web"
compatibility_date = "2024-01-01"

[build]
command = "npm install && npm run build"
directory = "dist"

[site]
bucket = "dist"

# Environment variables (reference only - set in Cloudflare dashboard)
[vars]
NEXT_PUBLIC_APP_URL = "https://oopjourney.com"
NEXT_PUBLIC_API_URL = "https://api.oopjourney.com"
```

**Build Settings for Cloudflare Dashboard:**
| Setting | Value |
|---------|-------|
| Build Command | `npm install && npm run build` |
| Build Output Directory | `apps/web/dist` |
| Root Directory | `apps/web` |

---

## 6. API Client Issues

### 🟡 WARNING: Duplicate API Client Configuration

**Files with duplicate base URL logic:**
1. `lib/api.ts` - Main API client
2. `lib/verification-api.ts` - Verification-specific client
3. `contexts/auth-context.tsx` - Auth-specific client

**Recommendation:** Consolidate all API calls through the main `lib/api.ts` client to ensure consistent:
- Error handling
- Authentication header injection
- Base URL configuration
- Request/response interceptors

### 🔵 INFO: Error Handling is Adequate

The API client in `lib/api.ts` has proper error handling with `ApiError` class and network error catching. No changes required.

---

## 7. Authentication Flow Issues

### 🔵 INFO: Middleware Auth Check Mismatch

**File:** `apps/web/middleware.ts`

**Issue:** The middleware checks for `auth_token` cookie, but the `auth-context.tsx` stores the token in `localStorage`, not cookies.

```typescript
// middleware.ts line 21
const authToken = request.cookies.get(AUTH_COOKIE_NAME)?.value;
```

```typescript
// auth-context.tsx line 39-40
const TOKEN_KEY = "auth_token";
// Stored via: localStorage.setItem(TOKEN_KEY, data.access_token);
```

**Impact:** Server-side auth protection in middleware won't work because the token is never in cookies.

**Fix Options:**
1. Set cookie when token is received (recommended):
```typescript
// In auth-context.tsx after receiving token
document.cookie = `auth_token=${data.access_token}; path=/; secure; samesite=strict`;
```

2. Or remove cookie-based middleware check and rely on client-side auth only.

---

## Action Items Checklist

### Pre-Deployment (Must Fix)

- [ ] **Fix 1:** Change `lib/api.ts` fallback URL from `3001` to `8000`
- [ ] **Fix 2:** Change `lib/verification-api.ts` fallback URL from `3001` to `8000`
- [ ] **Fix 3:** Change `next.config.js` output from `standalone` to `export`
- [ ] **Fix 4:** Add `distDir: 'dist'` to `next.config.js`
- [ ] **Fix 5:** Create `apps/web/.env.production` with production API URLs
- [ ] **Fix 6:** Fix CORS env var - change `CORS_ORIGINS` to `ALLOWED_ORIGINS` in `.env.production.example`
- [ ] **Fix 7:** Create `apps/web/wrangler.toml` for Cloudflare Pages

### Recommended Improvements

- [ ] **Fix 8:** Consolidate duplicate API clients into single `lib/api.ts`
- [ ] **Fix 9:** Fix middleware auth check - sync cookie with localStorage
- [ ] **Fix 10:** Decide on Google OAuth - implement frontend or remove backend code

---

## Environment Variable Reference

### Required for Frontend Build

| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | `https://api.oopjourney.com` | Backend API URL |
| `NEXT_PUBLIC_APP_URL` | `http://localhost:3000` | `https://oopjourney.com` | Frontend URL |
| `NEXT_PUBLIC_GOOGLE_CLIENT_ID` | *(optional)* | *(optional)* | Google OAuth client ID |
| `NEXT_PUBLIC_ENABLE_AI_HINTS` | `false` | `true` | AI feature flag |
| `NEXT_PUBLIC_ENABLE_PROGRESS_SYNC` | `true` | `true` | Sync feature flag |

### Required for Backend CORS

| Variable | Value | Location |
|----------|-------|----------|
| `ALLOWED_ORIGINS` | `https://oopjourney.com,https://www.oopjourney.com` | Backend `.env` |

---

## Verification Commands

After fixes, verify with:

```bash
# Build for production (should generate static files in dist/)
cd website-playground/apps/web
npm install
npm run build

# Verify dist folder exists and has index.html
ls -la dist/

# Verify no hardcoded localhost in built files
grep -r "localhost:3001" dist/ || echo "✓ No localhost:3001 found"
grep -r "localhost:8000" dist/ || echo "✓ No hardcoded localhost:8000 found"
```

---

## Related Backend Audit

See `AUDIT_BACKEND.md` for backend-specific issues that may affect frontend integration.

---

*End of Audit Report*

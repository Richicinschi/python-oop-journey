# Deploy to Netlify + Google OAuth Guide

Complete guide to host the Python OOP Journey platform on Netlify with Google authentication.

---

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   GoDaddy DNS   │────▶│   Netlify CDN    │     │  Backend API    │
│  yourdomain.com │     │  (Next.js App)   │────▶│  (Render/Fly)   │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                              ┌───────────────────────────┼──────────┐
                              ▼                           ▼          ▼
                    ┌─────────────────┐         ┌──────────────┐  ┌────────┐
                    │   Supabase DB   │         │  Upstash     │  │ Google │
                    │  (PostgreSQL)   │         │   Redis      │  │ OAuth  │
                    └─────────────────┘         └──────────────┘  └────────┘
```

**Services Needed:**
1. **Netlify** - Frontend hosting (Next.js)
2. **Render/Railway/Fly.io** - Backend API (FastAPI)
3. **Supabase/Neon** - PostgreSQL database
4. **Upstash** - Redis (caching, queues)
5. **Google Cloud Console** - OAuth credentials
6. **GoDaddy** - Domain DNS

---

## Step 1: Database Setup (Supabase)

### 1.1 Create Supabase Project
1. Go to https://supabase.com
2. Create new project
3. Choose region closest to your users
4. Save the database password

### 1.2 Get Connection String
1. Project Settings → Database
2. Copy "Connection string" (URI format)
3. It looks like: `postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres`

### 1.3 Enable Connection Pooling (Recommended)
1. Database → Connection Pooling
2. Copy "Transaction mode" URI
3. Update connection string for SQLAlchemy

---

## Step 2: Redis Setup (Upstash)

### 2.1 Create Upstash Database
1. Go to https://upstash.com
2. Create Redis database
3. Choose region matching Supabase

### 2.2 Get Credentials
1. Database details → Copy `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`
2. Or use Redis protocol: `rediss://default:[password]@[host]:[port]`

---

## Step 3: Backend Hosting (Render)

### 3.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub

### 3.2 Create Web Service
1. New → Web Service
2. Connect your GitHub repo
3. Configure:
   - **Name**: `oop-journey-api`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r apps/api/requirements.txt`
   - **Start Command**: `cd apps/api && uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### 3.3 Environment Variables
Add these in Render Dashboard → Environment:

```bash
# Database (from Supabase)
DATABASE_URL=postgresql+asyncpg://postgres:[password]@db.[project].supabase.co:5432/postgres

# Redis (from Upstash)
REDIS_URL=rediss://default:[password]@[host]:[port]

# Security (generate strong secrets)
SECRET_KEY=your-super-secret-64-char-key
JWT_SECRET=your-jwt-secret-32-char-key

# Google OAuth (we'll fill this in Step 5)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Frontend URL (from Netlify, we'll update later)
FRONTEND_URL=https://your-site.netlify.app

# AI (optional)
OPENAI_API_KEY=sk-...

# Environment
ENVIRONMENT=production
```

### 3.4 Deploy
1. Click "Create Web Service"
2. Wait for build to complete
3. Copy the URL: `https://oop-journey-api.onrender.com`

---

## Step 4: Google OAuth Setup

### 4.1 Create Google Cloud Project
1. Go to https://console.cloud.google.com
2. Create new project: "Python OOP Journey"
3. Enable "Google+ API" (or "Google Identity Toolkit")

### 4.2 Configure OAuth Consent Screen
1. APIs & Services → OAuth consent screen
2. Choose "External" (for public access)
3. Fill in:
   - App name: "Python OOP Journey"
   - User support email: your email
   - Developer contact: your email
4. Add scopes: `openid`, `email`, `profile`
5. Add test users (your email for testing)

### 4.3 Create OAuth Credentials
1. APIs & Services → Credentials
2. Create Credentials → OAuth client ID
3. Application type: "Web application"
4. Name: "OOP Journey Web"
5. Authorized JavaScript origins:
   - `http://localhost:3000` (for dev)
   - `https://your-site.netlify.app` (we'll update after Netlify deploy)
6. Authorized redirect URIs:
   - `http://localhost:3000/auth/callback/google` (for dev)
   - `https://your-site.netlify.app/auth/callback/google`
7. Click Create
8. **Copy Client ID and Client Secret**

### 4.4 Update Render Environment
Add to Render dashboard:
```bash
GOOGLE_CLIENT_ID=your-copied-client-id
GOOGLE_CLIENT_SECRET=your-copied-client-secret
```

---

## Step 5: Frontend (Netlify)

### 5.1 Prepare Frontend for Netlify

Create `apps/web/netlify.toml`:
```toml
[build]
  base = "apps/web"
  publish = "dist"
  command = "npm run build"

[build.environment]
  NODE_VERSION = "18"
  NPM_VERSION = "9"

[[redirects]]
  from = "/api/*"
  to = "https://oop-journey-api.onrender.com/api/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

Create `apps/web/.env.production`:
```bash
NEXT_PUBLIC_API_URL=https://oop-journey-api.onrender.com
NEXT_PUBLIC_APP_URL=https://your-site.netlify.app
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
```

### 5.2 Update Next.js Config
Update `apps/web/next.config.js`:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'dist',
  images: {
    unoptimized: true, // Required for static export
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_GOOGLE_CLIENT_ID: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID,
  },
};

module.exports = nextConfig;
```

### 5.3 Deploy to Netlify

#### Option A: Git Integration (Recommended)
1. Go to https://netlify.com
2. Add new site → Import from Git
3. Connect GitHub repo
4. Configure build:
   - **Base directory**: `apps/web`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
5. Add environment variables:
   ```
   NEXT_PUBLIC_API_URL=https://oop-journey-api.onrender.com
   NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
   ```
6. Deploy

#### Option B: Netlify CLI
```bash
# Install CLI
npm install -g netlify-cli

# Login
netlify login

# Initialize
cd apps/web
netlify init

# Set environment variables
netlify env:set NEXT_PUBLIC_API_URL https://oop-journey-api.onrender.com
netlify env:set NEXT_PUBLIC_GOOGLE_CLIENT_ID your-google-client-id

# Deploy
netlify deploy --prod
```

### 5.4 Get Netlify URL
After deploy, copy your site URL:
- Default: `https://[random-name].netlify.app`
- Or custom: `https://yourdomain.com` (if configured)

---

## Step 6: GoDaddy Domain Setup

### 6.1 Get Netlify DNS Info
1. Netlify Dashboard → Domain settings
2. Click "Add custom domain"
3. Enter your GoDaddy domain
4. Netlify will show DNS records to add

### 6.2 Configure GoDaddy DNS
1. Go to https://dcc.godaddy.com
2. Manage your domain → DNS
3. Delete existing A records
4. Add CNAME record:
   - Name: `@` (or `www`)
   - Value: `[your-site].netlify.app`
   - TTL: 600

Or use Netlify DNS (recommended):
1. Netlify → Domain settings
2. "Set up Netlify DNS"
3. Copy nameservers (e.g., `dns1.p01.nsone.net`)
4. GoDaddy → Nameservers → Custom
5. Paste Netlify nameservers
6. Save (takes 24-48 hours to propagate)

### 6.3 Enable HTTPS
1. Netlify will automatically provision SSL certificate
2. Force HTTPS: Domain settings → HTTPS → "Force HTTPS"

---

## Step 7: Update Google OAuth Redirects

1. Go back to Google Cloud Console
2. APIs & Services → Credentials → Edit OAuth client
3. Update Authorized redirect URIs with your custom domain:
   - `https://yourdomain.com/auth/callback/google`
4. Save

---

## Step 8: Implement Google OAuth (Code Changes)

### 8.1 Backend - Install Dependencies
Add to `apps/api/requirements.txt`:
```
google-auth>=2.22.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.1
```

### 8.2 Backend - Add Google Auth Router
Create `apps/api/api/routers/google_auth.py`:
```python
import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from api.models import User
from api.services.auth import generate_jwt
from api.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/auth/google", tags=["auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

@router.get("/login")
async def google_login():
    """Redirect to Google OAuth"""
    from google_auth_oauthlib.flow import Flow
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [f"{FRONTEND_URL}/auth/callback/google"],
            }
        },
        scopes=["openid", "email", "profile"],
    )
    flow.redirect_uri = f"{FRONTEND_URL}/auth/callback/google"
    
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
    )
    
    return RedirectResponse(authorization_url)

@router.get("/callback")
async def google_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Handle Google OAuth callback"""
    from google_auth_oauthlib.flow import Flow
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [f"{FRONTEND_URL}/auth/callback/google"],
            }
        },
        scopes=["openid", "email", "profile"],
    )
    flow.redirect_uri = f"{FRONTEND_URL}/auth/callback/google"
    
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    # Verify ID token
    idinfo = id_token.verify_oauth2_token(
        credentials.id_token, google_requests.Request(), GOOGLE_CLIENT_ID
    )
    
    email = idinfo.get("email")
    name = idinfo.get("name", email.split("@")[0])
    
    # Find or create user
    user = await User.find_by_email(db, email)
    if not user:
        user = await User.create(db, email=email, display_name=name)
    
    # Generate JWT
    token = generate_jwt(user.id)
    
    # Redirect to frontend with token
    return RedirectResponse(f"{FRONTEND_URL}/auth/callback?token={token}")
```

Add to `apps/api/api/main.py`:
```python
from api.routers import google_auth
app.include_router(google_auth.router)
```

### 8.3 Frontend - Update Login Page
Update `apps/web/app/auth/login/page.tsx`:
```tsx
"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Chrome } from "lucide-react";

export default function LoginPage() {
  const handleGoogleLogin = () => {
    window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/google/login`;
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-muted/50">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Welcome to Python OOP Journey</CardTitle>
          <CardDescription>
            Sign in to track your progress and save your work
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button 
            variant="outline" 
            className="w-full" 
            onClick={handleGoogleLogin}
          >
            <Chrome className="mr-2 h-4 w-4" />
            Continue with Google
          </Button>
          
          <p className="text-xs text-center text-muted-foreground">
            By signing in, you agree to our Terms of Service and Privacy Policy
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
```

### 8.4 Frontend - Update Callback Handler
Update `apps/web/app/auth/callback/page.tsx`:
```tsx
"use client";

import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";

export default function AuthCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { setToken } = useAuth();

  useEffect(() => {
    const token = searchParams.get("token");
    
    if (token) {
      setToken(token);
      router.push("/");
    } else {
      router.push("/auth/login?error=auth_failed");
    }
  }, [searchParams, router, setToken]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <p>Completing sign in...</p>
    </div>
  );
}
```

---

## Step 9: Testing Checklist

### Local Testing
```bash
# 1. Start backend
cd apps/api
uvicorn api.main:app --reload --port 8000

# 2. Start frontend
cd apps/web
npm run dev

# 3. Test Google Login
# - Visit http://localhost:3000/auth/login
# - Click "Continue with Google"
# - Should redirect to Google
# - After auth, back to app with JWT
```

### Production Testing
After deploying everything:

- [ ] Visit https://yourdomain.com
- [ ] Click "Login" → redirects to Google
- [ ] Complete Google auth → back to app
- [ ] Verify user created in database
- [ ] Solve a problem
- [ ] Run code execution
- [ ] Check progress saves
- [ ] Test AI hints (if configured)
- [ ] Test on mobile

---

## Step 10: Monitoring & Maintenance

### Set Up Uptime Monitoring
1. https://uptimerobot.com - Free monitoring
2. Add monitors:
   - `https://yourdomain.com`
   - `https://oop-journey-api.onrender.com/health`

### Set Up Error Tracking
1. https://sentry.io - Free tier
2. Add DSN to environment variables

### Database Backups
Supabase automatically backs up (daily on free tier).

### Cost Estimation (Monthly)
| Service | Free Tier | Paid (Recommended) |
|---------|-----------|-------------------|
| Netlify | 100GB bandwidth | $19 (Pro) |
| Render | 750 hours | $7 (512MB) |
| Supabase | 500MB, 2M requests | $25 (Pro) |
| Upstash | 10K requests/day | $10 |
| **Total** | **$0** | **~$61** |

---

## Troubleshooting

### CORS Errors
Add to Render environment:
```bash
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

Update FastAPI CORS middleware.

### Google OAuth Errors
- Check redirect URIs match exactly (including https)
- Ensure domain added to authorized origins
- Check client ID/secret are correct

### Database Connection Issues
- Use connection pooling URL from Supabase
- Check firewall rules

### Build Failures
- Check Node version (18+)
- Check Python version (3.11+)
- Review build logs in Netlify/Render dashboards

---

## Quick Commands Reference

```bash
# Deploy frontend only
netlify deploy --prod

# Deploy backend (pushes to Render automatically via git)
git push origin main

# Database migration (run on Render console)
alembic upgrade head

# View logs
netlify logs
render logs
```

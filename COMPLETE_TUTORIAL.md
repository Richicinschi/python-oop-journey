# Complete Tutorial: Deploy Python OOP Journey for $0

**From zero to live website - every single step explained.**

Estimated time: 2-3 hours  
Cost: $0/month (just your GoDaddy domain)  
Skill level: Beginner-friendly

---

## Table of Contents

1. [Overview](#overview)
2. [Step 1: Create All Accounts](#step-1-create-all-accounts)
3. [Step 2: Prepare Your Code](#step-2-prepare-your-code)
4. [Step 3: Set Up Database](#step-3-set-up-database)
5. [Step 4: Set Up Cache](#step-4-set-up-cache)
6. [Step 5: Configure Google OAuth](#step-5-configure-google-oauth)
7. [Step 6: Deploy Backend](#step-6-deploy-backend)
8. [Step 7: Deploy Frontend](#step-7-deploy-frontend)
9. [Step 8: Connect Your Domain](#step-8-connect-your-domain)
10. [Step 9: Test Everything](#step-9-test-everything)
11. [Troubleshooting](#troubleshooting)

---

## Overview

### What We're Building

```
User visits yourdomain.com
         │
         ▼
┌─────────────────────┐
│   Cloudflare Pages  │  ← Your Next.js app (free, fast)
│   (Frontend)        │
└──────────┬──────────┘
           │ API calls
           ▼
┌─────────────────────┐
│   Fly.io            │  ← Your FastAPI backend (free)
│   (Backend API)     │
└──────────┬──────────┘
           │
     ┌─────┴──────┐
     ▼            ▼
┌──────────┐  ┌──────────┐
│CockroachDB│  │ Upstash  │
│(Database) │  │ (Redis)  │
└──────────┘  └──────────┘
```

### Services You'll Create Accounts For

1. **GitHub** - Code hosting
2. **CockroachDB** - PostgreSQL database (free, no CC)
3. **Upstash** - Redis cache (free, no CC)
4. **Fly.io** - Backend hosting (free, no CC)
5. **Cloudflare** - Frontend hosting (free, no CC)
6. **Google Cloud** - OAuth login (free)

---

## Step 1: Create All Accounts

Do this first - create accounts for everything. It takes 15 minutes total.

### 1.1 GitHub (If You Don't Have One)

**Why:** Host your code

1. Go to https://github.com/signup
2. Enter your email
3. Create password
4. Choose username
5. Verify email
6. **Important:** Select "Free" plan

**Save your username - you'll need it**

---

### 1.2 CockroachDB (Database)

**Why:** Store user data, progress, problems

1. Go to https://cockroachlabs.cloud/signup
2. Click "Sign up with GitHub" (easier)
3. Authorize CockroachDB
4. **No credit card required!**
5. You'll land on dashboard

**What you get:**
- 5GB storage (plenty for thousands of users)
- PostgreSQL database
- Free forever

**Leave this tab open - we'll come back**

---

### 1.3 Upstash (Redis Cache)

**Why:** Store sessions, cache, job queues

1. Go to https://console.upstash.com/login
2. Click "Sign up with GitHub"
3. Authorize Upstash
4. **No credit card required!**
5. Click "Create Database"
6. Name: `oop-journey-cache`
7. Region: Choose closest to you (e.g., `us-east-1`)
8. Click "Create"

**What you get:**
- 10,000 requests/day (plenty for starting)
- Redis database
- Free forever

**Leave this tab open - we'll come back**

---

### 1.4 Fly.io (Backend Hosting)

**Why:** Run your Python backend API

**On Windows (PowerShell as Admin):**
```powershell
# Install flyctl
iwr https://fly.io/install.ps1 -useb | iex

# Restart PowerShell, then:
fly auth signup
```

**On Mac/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
fly auth signup
```

**During signup:**
1. Enter your email
2. Choose password
3. **No credit card required!** Just click past it
4. Verify email
5. You're in!

**What you get:**
- 3 free virtual machines
- 160GB bandwidth/month
- Free forever

---

### 1.5 Cloudflare (Frontend Hosting)

**Why:** Host your Next.js website (faster than Netlify)

1. Go to https://dash.cloudflare.com/sign-up
2. Enter email
3. Create password
4. **Don't add domain yet** - just create account
5. Verify email

**What you get:**
- Unlimited bandwidth
- Global CDN
- Free forever

---

### 1.6 Google Cloud Console (OAuth Login)

**Why:** "Sign in with Google" button

1. Go to https://console.cloud.google.com
2. Click "Select a project" → "New Project"
3. Project name: `python-oop-journey`
4. Click "Create"
5. You might need to accept terms and verify (free $300 credit - ignore it)

**What you get:**
- Unlimited OAuth users
- Free forever

**Leave this tab open - we'll configure later**

---

## Step 2: Prepare Your Code

### 2.1 Push Code to GitHub

If your code isn't on GitHub yet:

```bash
# Navigate to your project
cd website-playground

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Create repo on GitHub (via web interface)
# - Go to https://github.com/new
# - Name: oop-journey
# - Public or Private (your choice)
# - Click Create

# Connect and push
git remote add origin https://github.com/YOUR_USERNAME/oop-journey.git
git branch -M main
git push -u origin main
```

---

### 2.2 Add Required Files

**Create `apps/api/fly.toml`:**
```toml
app = 'oop-journey-api'
primary_region = 'ord'

[build]
  dockerfile = 'Dockerfile'

[env]
  PORT = '8000'

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ['app']

[[vm]]
  memory = '512mb'
  cpu_kind = 'shared'
  cpus = 1
```

**Create `apps/api/Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Run migrations and start
CMD ["sh", "-c", "alembic upgrade head && uvicorn api.main:app --host 0.0.0.0 --port 8000"]
```

**Update `apps/web/next.config.js`:**
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'dist',
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;
```

**Create `apps/web/.env.production`:**
```bash
# We'll fill this in after backend deploy
NEXT_PUBLIC_API_URL=https://oop-journey-api.fly.dev
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
```

---

### 2.3 Commit These Changes

```bash
git add .
git commit -m "Add deployment config"
git push
```

---

## Step 3: Set Up Database

### 3.1 Create CockroachDB Cluster

1. Go to https://cockroachlabs.cloud (you should be logged in)
2. Click "Create Cluster"
3. Select **"Serverless"** (this is the free one)
4. Choose region closest to your users:
   - US East: `us-east1`
   - US West: `us-west2`
   - Europe: `europe-west1`
   - Asia: `asia-southeast1`
5. Click "Create Cluster"

Wait 2-3 minutes for it to create.

---

### 3.2 Create Database User

1. Click on your cluster name
2. Click "SQL Users" on left
3. Click "Add User"
4. Username: `oopuser`
5. Password: Click "Generate & Save Password"
6. **SAVE THIS PASSWORD** - copy it somewhere safe
7. Click "Create"

---

### 3.3 Get Connection String

1. Still in your cluster, click "Connect"
2. Select "SQL User": `oopuser`
3. Select "Database": `defaultdb`
4. Click "General connection string"
5. Copy the connection string

It looks like:
```
postgresql://oopuser:password-here@host.cockroachlabs.cloud:26257/defaultdb?sslmode=require
```

**SAVE THIS - you'll need it 3 times**

---

## Step 4: Set Up Cache

### 4.1 Get Redis URL

1. Go to https://console.upstash.com (you should be logged in)
2. Click on your `oop-journey-cache` database
3. Click "Details" tab
4. Scroll down to "Redis Protocol"
5. Copy the endpoint (looks like `clustercfg.xxx.use1.cache.amazonaws.com`)

**SAVE THIS**

---

## Step 5: Configure Google OAuth

### 5.1 Enable Required APIs

1. Go to https://console.cloud.google.com (should be logged in)
2. Make sure project `python-oop-journey` is selected
3. Click hamburger menu (☰) → "APIs & Services" → "Library"
4. Search for "Google+ API"
5. Click it → Click "Enable"
6. Wait for it to enable

---

### 5.2 Configure Consent Screen

1. APIs & Services → "OAuth consent screen" (left menu)
2. Select **"External"** (for public users)
3. Click "Create"
4. Fill in:
   - **App name:** Python OOP Journey
   - **User support email:** your email
   - **App logo:** (optional, skip for now)
   - **App domain:** (leave blank for now)
   - **Developer contact:** your email
5. Click "Save and Continue"
6. Scopes: Click "Add or Remove Scopes"
   - Check: `openid`, `email`, `profile`
   - Click "Update"
   - Click "Save and Continue"
7. Test users: Click "Add Users"
   - Add your email
   - Click "Add"
   - Click "Save and Continue"
8. Click "Back to Dashboard"

---

### 5.3 Create OAuth Credentials

1. APIs & Services → "Credentials" (left menu)
2. Click "+ Create Credentials" → "OAuth client ID"
3. Application type: **"Web application"**
4. Name: `OOP Journey Web`
5. **Authorized JavaScript origins:**
   - Click "Add URI"
   - Add: `http://localhost:3000` (for local testing)
   - We'll add production URL later
6. **Authorized redirect URIs:**
   - Click "Add URI"
   - Add: `http://localhost:3000/auth/callback/google`
   - We'll add production URL later
7. Click "Create"
8. **COPY THE CLIENT ID AND SECRET**
   - Click the copy icon for Client ID
   - Save it somewhere
   - Click "OK" to close
9. Click the download icon (↓) to save JSON file
   - Save as `client_secret.json` somewhere safe

---

## Step 6: Deploy Backend

### 6.1 Initialize Fly.io App

```bash
# Navigate to API folder
cd apps/api

# Login to Fly.io
fly auth login

# Create app (don't deploy yet)
fly launch --name oop-journey-api --region ord --no-deploy
```

**During launch:**
- Name: `oop-journey-api` ✓
- Region: `ord` (Chicago) or pick closest
- Postgres: **No** (we're using CockroachDB)
- Redis: **No** (we're using Upstash)
- Deploy now: **No**

This creates `fly.toml` (we already created one, but this verifies it).

---

### 6.2 Set Environment Secrets

```bash
# Replace these with your actual values
fly secrets set DATABASE_URL="postgresql://oopuser:PASSWORD@HOST:26257/defaultdb?sslmode=require"
fly secrets set REDIS_URL="rediss://default:PASSWORD@HOST:6379"
fly secrets set SECRET_KEY="$(openssl rand -hex 32)"  # Generates random key
fly secrets set JWT_SECRET="$(openssl rand -hex 32)"
fly secrets set GOOGLE_CLIENT_ID="your-google-client-id-from-step-5"
fly secrets set GOOGLE_CLIENT_SECRET="your-google-secret-from-step-5"
fly secrets set FRONTEND_URL="http://localhost:3000"  # We'll update this later
fly secrets set ENVIRONMENT="production"
```

**Windows users without openssl:**
```powershell
# Generate random strings manually or use:
[Convert]::ToHexString((1..32 | ForEach-Object { Get-Random -Max 256 })) | Out-File -Encoding ascii secret.txt
```

---

### 6.3 Deploy!

```bash
fly deploy
```

This will:
1. Build Docker image
2. Push to Fly.io
3. Run migrations (creates database tables)
4. Start the API

Wait 3-5 minutes for deployment.

---

### 6.4 Verify Deployment

```bash
# Check status
fly status

# View logs
fly logs

# Test the API
curl https://oop-journey-api.fly.dev/api/v1/health
```

You should see: `{"status":"healthy"}`

**SAVE THIS URL:** `https://oop-journey-api.fly.dev`

---

## Step 7: Deploy Frontend

### 7.1 Update Environment Variables

Edit `apps/web/.env.production`:
```bash
NEXT_PUBLIC_API_URL=https://oop-journey-api.fly.dev
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
```

Commit and push:
```bash
git add .
git commit -m "Update API URL"
git push
```

---

### 7.2 Connect to Cloudflare Pages

1. Go to https://dash.cloudflare.com
2. Click "Pages" (left sidebar)
3. Click "Create a project"
4. Click "Connect to Git"
5. Select your GitHub account
6. Select your `oop-journey` repository
7. Click "Begin setup"

---

### 7.3 Configure Build Settings

Fill in:

| Field | Value |
|-------|-------|
| Project name | `oop-journey` |
| Production branch | `main` |
| Framework preset | **None** |
| Build command | `cd apps/web && npm install && npm run build` |
| Build output directory | `apps/web/dist` |
| Root directory | (leave blank) |

Click "Environment variables (advanced)":
- Add: `NEXT_PUBLIC_API_URL` = `https://oop-journey-api.fly.dev`
- Add: `NEXT_PUBLIC_GOOGLE_CLIENT_ID` = your Google client ID

Click "Save and Deploy"

Wait 2-3 minutes for build.

---

### 7.4 Verify Deployment

Once built, Cloudflare will show you a URL like:
```
https://oop-journey.pages.dev
```

Click it - your website should load!

Test:
- [ ] Homepage loads
- [ ] Can navigate to weeks
- [ ] Can see problems

---

## Step 8: Connect Your Domain

### 8.1 Get Cloudflare Nameservers

1. In Cloudflare Pages, click your project
2. Click "Custom domains" tab
3. Click "Set up a custom domain"
4. Enter your GoDaddy domain: `yourdomain.com`
5. Click "Continue"
6. Cloudflare will show you 2 nameservers like:
   - `brett.ns.cloudflare.com`
   - `dana.ns.cloudflare.com`

**COPY THESE - you'll need them**

---

### 8.2 Update GoDaddy DNS

1. Go to https://account.godaddy.com
2. Sign in
3. Click "My Products"
4. Find your domain → Click "DNS"
5. Scroll down to "Nameservers"
6. Click "Change"
7. Select **"Enter my own nameservers"**
8. Delete existing nameservers
9. Add Cloudflare nameservers:
   - Nameserver 1: `brett.ns.cloudflare.com`
   - Nameserver 2: `dana.ns.cloudflare.com`
10. Click "Save"

**Wait 5-30 minutes for DNS to propagate.**

---

### 8.3 Activate Domain in Cloudflare

1. Back in Cloudflare, click "Activate domain"
2. It will check if nameservers are updated
3. Once detected, click "Finish"

---

### 8.4 Update Google OAuth Redirects

Now that you have your domain, update Google OAuth:

1. https://console.cloud.google.com → APIs & Services → Credentials
2. Click your OAuth 2.0 Client ID
3. Add to **Authorized JavaScript origins**:
   - `https://yourdomain.com`
   - `https://www.yourdomain.com` (if you use www)
4. Add to **Authorized redirect URIs**:
   - `https://yourdomain.com/auth/callback/google`
   - `https://www.yourdomain.com/auth/callback/google`
5. Click "Save"

---

### 8.5 Update Backend Environment

```bash
# Update FRONTEND_URL to your actual domain
fly secrets set FRONTEND_URL="https://yourdomain.com"

# Redeploy
fly deploy
```

---

### 8.6 Force HTTPS

In Cloudflare:
1. Your domain overview
2. Click "SSL/TLS" tab
3. Set mode to "Full (strict)"
4. Go to "Edge Certificates"
5. Enable "Always Use HTTPS"

---

## Step 9: Test Everything

### 9.1 Basic Tests

Visit: `https://yourdomain.com`

Check:
- [ ] Homepage loads
- [ ] Can see weeks/days
- [ ] Can see problem list
- [ ] Styles look correct

---

### 9.2 Authentication Test

1. Click "Login" or "Get Started"
2. Click "Continue with Google"
3. You should redirect to Google sign-in
4. Sign in with your Google account
5. Should redirect back to your site
6. Should see your profile/name in header

**If it fails:** Check browser console for errors.

---

### 9.3 Problem Solving Test

1. Navigate to any problem
2. You should see Monaco editor
3. Type some code:
   ```python
   print("Hello, World!")
   ```
4. Click "Run"
5. Should see output: `Hello, World!`

**If code execution fails:** Check Fly.io logs:
```bash
fly logs
```

---

### 9.4 Progress Tracking Test

1. Solve a problem (write working code, verify)
2. Navigate to another problem
3. Go back to first problem
4. Your code should be saved

**If progress doesn't save:** Check browser console for API errors.

---

### 9.5 Mobile Test

On your phone:
1. Visit `https://yourdomain.com`
2. Login
3. Try solving a problem
4. Should be usable (may be cramped, but functional)

---

## You're Live! 🎉

Your Python OOP Journey platform is now:
- ✅ Hosted on your GoDaddy domain
- ✅ Using Google OAuth for login
- ✅ Saving progress to database
- ✅ Running code in sandbox
- ✅ Completely free ($0/month)

---

## Troubleshooting

### "Site not found" / DNS issues

**Wait longer.** DNS propagation takes 5-30 minutes, sometimes 24 hours.

Check:
```bash
# Test DNS
nslookup yourdomain.com
```

Should show Cloudflare IPs.

---

### "Cannot connect to backend"

Check CORS settings:
```bash
# In Fly.io, verify FRONTEND_URL
fly secrets list
```

Must match your domain exactly (including `https://`).

---

### "Google OAuth error: redirect_uri_mismatch"

1. Check Google Console → Credentials
2. Authorized redirect URIs must match EXACTLY:
   - Correct: `https://yourdomain.com/auth/callback/google`
   - Wrong: `https://www.yourdomain.com/auth/callback/google`
   - Wrong: `http://yourdomain.com/auth/callback/google`
   - Wrong: `https://yourdomain.com/auth/callback/google/`

---

### "Database connection failed"

Check CockroachDB connection string:
- Must have `sslmode=require`
- Password must be URL-encoded if it has special characters

Test:
```bash
psql "your-connection-string"
```

---

### "Build failed" on Cloudflare

1. Cloudflare Pages → your project
2. Click failed deployment
3. View logs
4. Common issues:
   - Missing `npm install` in build command
   - Wrong output directory (should be `apps/web/dist`)
   - TypeScript errors

---

## Next Steps

### Add Monitoring (Free)

**Uptime monitoring:**
1. https://uptimerobot.com
2. Add monitor: `https://yourdomain.com`
3. Add monitor: `https://oop-journey-api.fly.dev/api/v1/health`
4. Get email alerts if site goes down

**Error tracking:**
1. https://sentry.io
2. Create project
3. Add DSN to environment variables
4. Get alerts for crashes

---

### Share With Friends!

Your platform is ready for users. Share the link and gather feedback.

---

## Commands Reference

```bash
# Deploy backend updates
cd apps/api && fly deploy

# View backend logs
fly logs

# SSH into backend
fly ssh console

# Restart backend
fly apps restart oop-journey-api

# Frontend auto-deploys on git push
# Just commit and push:
git add . && git commit -m "Update" && git push
```

---

**Questions? Check the troubleshooting section or run the verification commands.**

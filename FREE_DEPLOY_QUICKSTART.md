# Zero-Cost Quickstart - Fly.io + CockroachDB

Deploy Python OOP Journey for **$0/month** (no credit card required).

---

## What We're Building

```
┌─────────────────────────────────────────────────────────────┐
│                      YOUR DOMAIN (GoDaddy)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
┌──────────────────┐       ┌──────────────────┐
│  Cloudflare Pages│       │     Fly.io       │
│   (Next.js App)  │──────▶│  (FastAPI API)   │
│    $0/month      │       │    $0/month      │
└──────────────────┘       └────────┬─────────┘
                                    │
              ┌─────────────────────┼──────────┐
              ▼                     ▼          ▼
    ┌─────────────────┐  ┌────────────────┐  ┌──────────┐
    │   CockroachDB   │  │  Upstash Redis │  │  Google  │
    │   (PostgreSQL)  │  │   (Cache)      │  │  OAuth   │
    │    $0/month     │  │    $0/month    │  │  $0/mo   │
    └─────────────────┘  └────────────────┘  └──────────┘
```

**Total: $0/month + $12/year for domain**

---

## Sign Up (No Credit Card!)

### 1. CockroachDB (Database)
```
🔗 https://cockroachlabs.cloud
✅ Sign up with GitHub
✅ Create "Serverless" cluster
```

### 2. Upstash (Redis)
```
🔗 https://upstash.com
✅ Sign up with GitHub
✅ Create Redis database
```

### 3. Fly.io (Backend Hosting)
```bash
# Install
iwr https://fly.io/install.ps1 -useb | iex

# Sign up (NO CREDIT CARD!)
fly auth signup
```

### 4. Cloudflare (Frontend Hosting)
```
🔗 https://dash.cloudflare.com/sign-up
✅ Use email (not domain yet)
```

### 5. Google Cloud (OAuth)
```
🔗 https://console.cloud.google.com
✅ Create project
✅ Enable Google+ API
```

---

## Deploy in 5 Steps

### Step 1: Get Database URL

**CockroachDB Dashboard:**
1. SQL Users → Create SQL User
2. Connection Parameters → General connection string
3. Copy: `postgresql://user:pass@host:26257/defaultdb?sslmode=require`

### Step 2: Get Redis URL

**Upstash Dashboard:**
1. Redis → your database
2. Copy `UPSTASH_REDIS_REST_URL` and token
3. Or use Redis protocol: `rediss://default:pass@host:6379`

### Step 3: Deploy Backend to Fly.io

```bash
# Navigate to backend
cd apps/api

# Launch app (creates fly.toml)
fly launch --name oop-journey-api --region ord --no-deploy

# Set secrets (database, redis, auth)
fly secrets set DATABASE_URL="your-cockroachdb-url"
fly secrets set REDIS_URL="your-redis-url"
fly secrets set SECRET_KEY="paste-random-64-char-string"
fly secrets set JWT_SECRET="paste-random-32-char-string"
fly secrets set GOOGLE_CLIENT_ID="your-google-client-id"
fly secrets set GOOGLE_CLIENT_SECRET="your-google-secret"
fly secrets set FRONTEND_URL="https://yourdomain.com"

# Deploy
fly deploy

# Get URL (save this!)
fly info
# → https://oop-journey-api.fly.dev
```

### Step 4: Deploy Frontend to Cloudflare Pages

```bash
# Build locally first (to test)
cd apps/web
npm run build

# Should create 'dist' folder
ls dist/
```

**Cloudflare Dashboard:**
1. Pages → Create a project
2. Connect to GitHub
3. Select your repo
4. Build settings:
   - **Framework preset:** None
   - **Build command:** `cd apps/web && npm run build`
   - **Build output directory:** `apps/web/dist`
5. Environment variables:
   ```
   NEXT_PUBLIC_API_URL=https://oop-journey-api.fly.dev
   NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
   ```
6. Deploy!

### Step 5: Connect Your GoDaddy Domain

**Cloudflare Pages:**
1. Project → Custom domains
2. "Set up a custom domain"
3. Enter: `yourdomain.com`
4. Copy the 2 nameservers shown (like `brett.ns.cloudflare.com`)

**GoDaddy:**
1. DNS → Nameservers
2. Change to Custom
3. Paste Cloudflare nameservers
4. Save (takes 24-48 hours)

**Google Cloud Console:**
1. APIs & Services → Credentials
2. Edit OAuth 2.0 Client
3. Add Authorized origins:
   - `https://yourdomain.com`
4. Add Authorized redirect URIs:
   - `https://yourdomain.com/auth/callback/google`
5. Save

---

## Verify Everything Works

```bash
# Test API
curl https://oop-journey-api.fly.dev/api/v1/health

# Test auth
curl https://oop-journey-api.fly.dev/api/v1/auth/google/config
```

Then visit:
- ✅ `https://yourdomain.com` (should load)
- ✅ Click Login → redirects to Google
- ✅ Sign in → back to app
- ✅ Solve a problem
- ✅ Progress saves

---

## Free Tier Limits

| Service | Limit | Your Usage |
|---------|-------|------------|
| CockroachDB | 5GB storage, 1M req/month | ~50MB for start |
| Upstash | 10K requests/day | ~100/day for start |
| Fly.io | 3 VMs, 160GB bandwidth | 1 VM for API |
| Cloudflare | Unlimited | Your traffic |
| Google OAuth | Unlimited | Your users |

**You can handle ~1000 users before hitting limits.**

---

## Commands Cheat Sheet

```bash
# Deploy updates
cd apps/api && fly deploy
cd apps/web && npm run build && # push to GitHub for Cloudflare

# View logs
fly logs

# SSH into backend
fly ssh console

# Run database migrations
fly ssh console -C "cd apps/api && alembic upgrade head"

# Scale up (if you pay later)
fly scale count 2
```

---

## Troubleshooting

### "App won't start"
```bash
fly logs  # Check error messages
fly status  # Check VM status
```

### "Database connection failed"
- Check CockroachDB URL has `sslmode=require`
- Verify SQL user exists and password is correct

### "CORS errors"
- Check `FRONTEND_URL` in Fly.io matches your domain exactly
- Must include `https://`

### "Google OAuth error"
- Verify redirect URI in Google Console matches exactly
- No trailing slash
- Must be `https`

---

## Migration from Other Providers

Already set up Supabase/Render? Easy switch:

```bash
# 1. Export data
pg_dump "old-database-url" > backup.sql

# 2. Import to CockroachDB
psql "cockroachdb-url" < backup.sql

# 3. Update Fly.io secrets
fly secrets set DATABASE_URL="new-cockroachdb-url"

# 4. Redeploy
fly deploy
```

---

**Ready? Start with Step 1 above!**

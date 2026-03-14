# 100% Free Deployment Options - No Credit Card Required

Complete guide to host Python OOP Journey for **$0 forever**.

---

## Quick Comparison Table

| Service | Provider | Free Tier Limits | Best For |
|---------|----------|------------------|----------|
| **Database** | CockroachDB | 5GB storage, 1M requests/mo | Primary data |
| **Cache** | Upstash Redis | 10K requests/day | Sessions, cache |
| **Backend** | Fly.io | 3 shared VMs, 160GB/mo | FastAPI hosting |
| **Frontend** | Cloudflare Pages | Unlimited bandwidth | Next.js static |
| **Auth** | Google OAuth | Unlimited users | Social login |
| **File Storage** | Cloudflare R2 | 10GB/month | User uploads |

**Total Cost: $0**

---

## Option 1: CockroachDB (Recommended - Easiest)

### Why CockroachDB?
- ✅ **No credit card required**
- ✅ PostgreSQL compatible (no code changes!)
- ✅ 5GB storage (enough for thousands of users)
- ✅ 1M request units/month
- ✅ Serverless (scales to zero)

### Setup (10 minutes)

1. **Create Account**
   ```
   https://cockroachlabs.cloud
   ```
   - Sign up with GitHub (no CC)
   - Create "Serverless" cluster
   - Choose region closest to your users

2. **Get Connection String**
   - SQL Users → Create SQL User
   - Connection parameters → General connection string
   - Copy the URL

3. **Update Backend Code**
   ```python
   # apps/api/.env
   DATABASE_URL=postgresql://user:password@host:26257/defaultdb?sslmode=require
   ```

4. **Run Migrations**
   ```bash
   cd apps/api
   alembic upgrade head
   ```

**Limits:**
- 5GB storage
- 1M request units/month
- 1 cluster per account

---

## Option 2: TiDB Serverless (MySQL Compatible)

### Why TiDB?
- ✅ No credit card
- ✅ 5GB storage + 50M request units
- ✅ MySQL compatible
- ✅ Auto-scaling

### Setup
1. https://tidbcloud.com
2. Create Serverless Tier
3. Get connection string
4. Update SQLAlchemy dialect:
   ```python
   # Use pymysql instead of asyncpg
   DATABASE_URL=mysql+pymysql://user:pass@host:4000/db
   ```

---

## Option 3: Self-Hosted PocketBase (SQLite)

### What is PocketBase?
- Single Go binary (~20MB)
- SQLite database (embedded)
- Built-in auth, file storage, real-time
- Can run on free Render/Railway

### Architecture Change
```
Before: FastAPI + PostgreSQL + Redis
After:  FastAPI + PocketBase (auth, DB, files)
```

### Setup (15 minutes)

1. **Download PocketBase**
   ```bash
   wget https://github.com/pocketbase/pocketbase/releases/latest/download/pocketbase_linux_amd64.zip
   unzip pocketbase_linux_amd64.zip
   ```

2. **Create Fly.io App for PocketBase**
   ```bash
   # Install flyctl
   curl -L https://fly.io/install.sh | sh
   
   # Login (no CC required!)
   fly auth signup
   
   # Create app
   fly launch --name oop-journey-db --region ord
   
   # Deploy
   fly deploy
   ```

3. **Use PocketBase from FastAPI**
   ```python
   # apps/api/api/services/pocketbase.py
   from pocketbase import PocketBase
   
   pb = PocketBase('https://oop-journey-db.fly.dev')
   
   # Auth
   auth_data = pb.collection('users').auth_with_password(email, password)
   
   # Database
   records = pb.collection('progress').get_full_list()
   ```

**Pros:**
- One service does everything (auth, DB, files)
- SQLite is plenty for < 10K users
- Real-time subscriptions

**Cons:**
- Requires code changes (migrate from SQLAlchemy)
- SQLite not ideal for high concurrency

---

## Option 4: Appwrite (Firebase Alternative)

### What is Appwrite?
- Open-source Firebase alternative
- Database, Auth, Storage, Functions
- Cloud version has generous free tier

### Free Tier
- 750K executions/month
- 2GB database storage
- 2GB file storage
- Unlimited users

### Setup
1. https://cloud.appwrite.io
2. Create project
3. Use Appwrite SDK instead of custom backend

**Architecture Change:**
```
Before: Next.js → FastAPI → PostgreSQL
After:  Next.js → Appwrite (direct)
```

**Pros:**
- No backend server needed!
- Built-in auth, DB, storage
- Real-time subscriptions

**Cons:**
- Requires significant code changes
- Vendor lock-in

---

## Option 5: Fly.io Everything (Recommended - Most Control)

### Why Fly.io?
- ✅ **No credit card required**
- ✅ 3 shared VMs free (256MB RAM each)
- ✅ 160GB outbound bandwidth
- ✅ 3GB persistent volumes
- ✅ PostgreSQL included
- ✅ Redis included

### Complete Stack on Fly.io

**1. PostgreSQL**
```bash
# Create Postgres cluster (FREE!)
fly postgres create --name oop-db --region ord --vm-size shared-cpu-1x

# Attach to app
fly postgres attach --app oop-api oop-db
```

**2. Redis (Upstash on Fly)**
```bash
# Create Upstash Redis
fly ext redis create --name oop-cache --region ord
```

**3. FastAPI Backend**
```bash
# Create app
cd apps/api
fly launch --name oop-api --region ord

# Deploy
fly deploy
```

**4. Next.js Frontend (Static)**
```bash
cd apps/web
# Build locally
npm run build

# Or deploy to Cloudflare Pages (better for static)
```

**Fly.toml for Backend:**
```toml
app = 'oop-api'
primary_region = 'ord'

[build]
  dockerfile = 'Dockerfile'

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ['app']

[[vm]]
  size = 'shared-cpu-1x'
  memory = '256mb'
```

**Limits:**
- 3 VMs (can run 3 services or 1 service with 3 replicas)
- 160GB outbound bandwidth/month
- VMs sleep after 5 min idle (cold start ~2s)

---

## Option 6: Railway (Free $5 Credit/Month)

### Why Railway?
- $5 free credit monthly (enough for small app)
- Easy deployments from GitHub
- PostgreSQL, Redis, etc.

### Setup
1. https://railway.app
2. New project → Deploy from GitHub
3. Add PostgreSQL plugin (free tier)
4. Add Redis plugin
5. Deploy

**Free Tier:**
- $5 credit/month (~512MB RAM, shared CPU)
- Enough for development + light production

---

## Recommended 100% Free Stack

### Best Option: Fly.io + CockroachDB + Cloudflare

| Component | Service | Cost | Why |
|-----------|---------|------|-----|
| Database | **CockroachDB** | $0 | 5GB Postgres, no CC |
| Cache | **Upstash Redis** | $0 | 10K req/day, no CC |
| Backend | **Fly.io** | $0 | 3 VMs free, no CC |
| Frontend | **Cloudflare Pages** | $0 | Unlimited bandwidth |
| Auth | **Google OAuth** | $0 | Unlimited users |
| Domain | **GoDaddy** | $12/year | Already purchased |

**Total: $0/month + $12/year for domain**

---

## Step-by-Step: Deploy to 100% Free Stack

### Step 1: Database (CockroachDB) - 10 min
```bash
# 1. Sign up: https://cockroachlabs.cloud (GitHub, no CC)
# 2. Create cluster → Serverless
# 3. Create SQL user
# 4. Copy connection string
```

### Step 2: Redis (Upstash) - 5 min
```bash
# 1. Sign up: https://upstash.com (GitHub, no CC)
# 2. Create Redis database
# 3. Copy REST URL and token
```

### Step 3: Backend (Fly.io) - 15 min
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login (no CC required!)
fly auth signup

# Create app
cd apps/api
fly launch --name oop-journey-api --region ord

# Set secrets
fly secrets set \
  DATABASE_URL="postgresql://user:pass@host:26257/db?sslmode=require" \
  REDIS_URL="rediss://default:pass@host:port" \
  SECRET_KEY="$(openssl rand -hex 32)" \
  GOOGLE_CLIENT_ID="your-google-id" \
  GOOGLE_CLIENT_SECRET="your-google-secret"

# Deploy
fly deploy
```

### Step 4: Frontend (Cloudflare Pages) - 10 min
```bash
# 1. Push code to GitHub
# 2. https://dash.cloudflare.com → Pages
# 3. Create project → Connect GitHub
# 4. Build settings:
#    - Framework preset: Next.js (Static HTML Export)
#    - Build command: cd apps/web && npm run build
#    - Output directory: apps/web/dist
# 5. Add environment variables:
#    - NEXT_PUBLIC_API_URL: https://oop-journey-api.fly.dev
# 6. Deploy
```

### Step 5: Domain (GoDaddy) - 5 min
1. Cloudflare Pages → Custom domains
2. Add your GoDaddy domain
3. GoDaddy DNS → Add CNAME:
   - Name: `@`
   - Value: `your-project.pages.dev`

---

## SpacetimeDB: Should You Use It?

### What is SpacetimeDB?
- Real-time, multiplayer database
- Written in Rust, runs as embedded module
- Different paradigm from PostgreSQL

### Pros
- ✅ Extremely fast (in-memory)
- ✅ Built-in real-time sync
- ✅ Free tier available

### Cons
- ❌ **Not SQL** (proprietary query language)
- ❌ Requires significant code rewrite
- ❌ Smaller ecosystem
- ❌ Newer (less mature)

### Verdict
**Don't use SpacetimeDB for this project.** It would require rewriting:
- All SQLAlchemy models
- All queries
- Migration system
- Authentication

**Use CockroachDB instead** - it's PostgreSQL compatible with zero code changes.

---

## Free Tier Limits Summary

| Service | Storage | Requests | Bandwidth | Sleep? |
|---------|---------|----------|-----------|--------|
| CockroachDB | 5GB | 1M/month | - | No |
| Upstash Redis | - | 10K/day | - | No |
| Fly.io | 3GB vol | - | 160GB/mo | Yes (5min) |
| Cloudflare Pages | - | - | Unlimited | No |
| Railway | 1GB | - | 100GB/mo | No* |

*Railway free tier requires activity

---

## Migration Guide (From Supabase)

If you already set up Supabase, migrating to CockroachDB is easy:

```bash
# 1. Export from Supabase
pg_dump "postgresql://user:pass@supabase.co:5432/postgres" > backup.sql

# 2. Import to CockroachDB
psql "postgresql://user:pass@cockroachlabs.cloud:26257/defaultdb?sslmode=require" < backup.sql

# 3. Update connection string in Fly.io
fly secrets set DATABASE_URL="new-cockroachdb-url"

# 4. Redeploy
fly deploy
```

---

## Monitoring (Free)

| Service | Free Tier | Setup |
|---------|-----------|-------|
| UptimeRobot | 50 monitors | https://uptimerobot.com |
| Sentry | 5K errors/mo | https://sentry.io |

---

## Final Recommendation

### For Learning/Development:
**Fly.io Everything** - easiest, all-in-one

### For Production (Free Forever):
**CockroachDB + Upstash + Fly.io + Cloudflare Pages**

### For Zero Backend Maintenance:
**Firebase** or **Appwrite** (more code changes)

---

## Quick Commands Reference

```bash
# Deploy backend to Fly.io
cd apps/api
fly deploy

# View logs
fly logs

# SSH into app
fly ssh console

# Run migrations
fly ssh console -C "cd apps/api && alembic upgrade head"

# Scale (if you upgrade)
fly scale count 2
```

---

**All services listed require NO credit card and are FREE forever (within limits).**

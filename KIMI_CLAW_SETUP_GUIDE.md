# Kimi Claw Setup Guide - Python OOP Journey
## Complete Configuration & Deployment Instructions

**Project:** Python OOP Journey Website  
**Repository:** https://github.com/Richicinschi/python-oop-journey  
**Last Updated:** March 16, 2026  

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Claw Environment Setup](#claw-environment-setup)
3. [Repository Clone & Configuration](#repository-clone--configuration)
4. [Node.js Installation](#nodejs-installation)
5. [Dependency Installation](#dependency-installation)
6. [Environment Variables](#environment-variables)
7. [Database Setup](#database-setup)
8. [Running Locally](#running-locally)
9. [Building for Production](#building-for-production)
10. [Deployment to Render](#deployment-to-render)
11. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts
- [ ] GitHub account (for repository access)
- [ ] Render account (for deployment) - https://render.com
- [ ] CockroachDB account (for database) - https://cockroachlabs.cloud
- [ ] Redis Cloud account (for caching) - https://redis.io/cloud
- [ ] Google Cloud account (for OAuth) - https://console.cloud.google.com

### Required Tools
- [ ] Git
- [ ] Node.js 20.x
- [ ] Python 3.11+
- [ ] PostgreSQL client (optional, for DB management)

---

## Claw Environment Setup

### Step 1: Create Claw Workspace

```bash
# In Kimi Claw terminal
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/Richicinschi/python-oop-journey.git
cd python-oop-journey/website-playground
```

### Step 2: Verify Claw Environment

```bash
# Check available tools
which git
which python3
which pip
node --version  # Should show v20.x
npm --version   # Should show 10.x
```

If Node.js is missing, see [Node.js Installation](#nodejs-installation) below.

---

## Repository Clone & Configuration

### Clone the Repository

```bash
cd ~/projects
git clone https://github.com/Richicinschi/python-oop-journey.git
cd python-oop-journey
```

### Repository Structure

```
python-oop-journey/
├── website-playground/          # MAIN PROJECT
│   ├── apps/
│   │   ├── api/                 # FastAPI backend
│   │   │   ├── api/
│   │   │   ├── migrations/
│   │   │   ├── data/
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   └── web/                 # Next.js frontend
│   │       ├── app/
│   │       ├── components/
│   │       ├── lib/
│   │       ├── hooks/
│   │       ├── public/
│   │       ├── Dockerfile
│   │       └── next.config.js
│   ├── packages/
│   │   └── types/
│   ├── render.yaml              # Render deployment config
│   └── package.json             # Root package.json
│
├── python-oop-journey-v2/       # Curriculum content (separate)
├── agency-agents/               # Agent definitions
├── docs/                        # Documentation
└── _archive/                    # Archived files
```

---

## Node.js Installation

### Option A: Using Node Version Manager (nvm)

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc

# Install Node.js 20
nvm install 20
nvm use 20
nvm alias default 20

# Verify
node --version  # v20.x.x
npm --version   # 10.x.x
```

### Option B: Using Package Manager

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version
npm --version
```

### Option C: Using Pre-built Binary

```bash
# Download and extract Node.js 20
cd /tmp
wget https://nodejs.org/dist/v20.11.0/node-v20.11.0-linux-x64.tar.xz
tar -xf node-v20.11.0-linux-x64.tar.xz
sudo mv node-v20.11.0-linux-x64 /usr/local/node

# Add to PATH
echo 'export PATH=/usr/local/node/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Verify
node --version
```

---

## Dependency Installation

### Step 1: Install Root Dependencies

```bash
cd ~/projects/python-oop-journey/website-playground
npm install
```

This will install:
- Turborepo (monorepo management)
- Husky (git hooks)
- All workspace dependencies

### Step 2: Install Frontend Dependencies

```bash
cd apps/web
npm install
```

### Step 3: Install Backend Dependencies

```bash
cd ../api
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Check frontend
cd apps/web
npm run type-check

# Check backend
cd ../api
python -c "from api.main import app; print('Backend OK')"
```

---

## Environment Variables

### Step 1: Create Environment Files

```bash
cd ~/projects/python-oop-journey/website-playground

# Copy example files
cp apps/api/.env.production.example apps/api/.env.local
cp apps/web/.env.example apps/web/.env.local
```

### Step 2: Configure Backend (.env.local)

```bash
cd apps/api
nano .env.local
```

Add these values:

```env
# Environment
ENVIRONMENT=development
DEBUG=true
APP_NAME=Python OOP Journey API

# Security (generate new!)
SECRET_KEY=your-super-secret-key-change-this

# Database (CockroachDB)
DATABASE_URL=postgresql+asyncpg://username:password@host:26257/database?sslmode=verify-full

# Redis
REDIS_URL=redis://default:password@host:port

# JWT
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Frontend URL
FRONTEND_URL=http://localhost:3000

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Google OAuth (optional for local)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
```

### Step 3: Configure Frontend (.env.local)

```bash
cd apps/web
nano .env.local
```

Add these values:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Feature Flags
NEXT_PUBLIC_FEATURE_AI_HINTS=true
NEXT_PUBLIC_FEATURE_AI_REVIEW=true
NEXT_PUBLIC_FEATURE_COMMUNITY=false

# Google OAuth (optional)
NEXT_PUBLIC_GOOGLE_CLIENT_ID=

# Development
NEXT_PUBLIC_DEBUG=true
```

---

## Database Setup

### Step 1: Create CockroachDB Cluster

1. Go to https://cockroachlabs.cloud
2. Create new cluster (Serverless is free)
3. Create SQL user and save password
4. Download CA certificate
5. Get connection string

### Step 2: Configure Database URL

```bash
# Format:
# postgresql+asyncpg://username:password@host:26257/defaultdb?sslmode=verify-full&sslrootcert=/path/to/cert

# Example:
export DATABASE_URL="postgresql+asyncpg://kimi:password@host.cockroachlabs.cloud:26257/oop-journey?sslmode=verify-full"
```

### Step 3: Run Migrations

```bash
cd ~/projects/python-oop-journey/website-playground/apps/api

# Install alembic if not installed
pip install alembic

# Run migrations
alembic upgrade head

# Verify
alembic current
```

### Step 4: Verify Database Connection

```bash
# Test connection
python -c "
import asyncio
from api.database import get_db
async def test():
    async for db in get_db():
        result = await db.execute('SELECT 1')
        print('Database connected!')
asyncio.run(test())
"
```

---

## Running Locally

### Option A: Run Frontend Only

```bash
cd ~/projects/python-oop-journey/website-playground/apps/web
npm run dev

# Open http://localhost:3000
```

### Option B: Run Backend Only

```bash
cd ~/projects/python-oop-journey/website-playground/apps/api

# Option 1: Direct Python
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: With docker-entrypoint
./docker-entrypoint.sh

# API will be at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Option C: Run Full Stack (Recommended)

```bash
cd ~/projects/python-oop-journey/website-playground

# Terminal 1: Backend
cd apps/api && python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd apps/web && npm run dev

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Option D: Using Docker Compose

```bash
cd ~/projects/python-oop-journey/website-playground

# Start all services
docker-compose up --build

# Or in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Building for Production

### Step 1: Build Frontend

```bash
cd ~/projects/python-oop-journey/website-playground/apps/web

# Install dependencies
npm install

# Type check
npm run type-check

# Build
npm run build

# Verify build output
ls -la .next/
```

### Step 2: Build Backend

```bash
cd ~/projects/python-oop-journey/website-playground/apps/api

# Install dependencies
pip install -r requirements.txt

# Test import
python -c "from api.main import app; print('Build OK')"

# Optional: Build Docker image
docker build -t oop-journey-api .
```

### Step 3: Verify Production Build

```bash
cd ~/projects/python-oop-journey/website-playground/apps/web

# Start production server
npm start

# Or with Next.js standalone
cd .next/standalone
node server.js
```

---

## Deployment to Render

### Step 1: Connect Repository

1. Go to https://dashboard.render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Select `website-playground/render.yaml`

### Step 2: Configure Services

Render will automatically detect these services from `render.yaml`:

#### Web Service (Frontend)
- **Name:** python-oop-journey
- **Build Command:** `npm install && npm run build`
- **Start Command:** `npm start`
- **Environment:** Node

#### API Service (Backend)
- **Name:** oop-journey-api
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `./docker-entrypoint.sh`
- **Environment:** Docker

#### Worker Service
- **Name:** oop-journey-worker
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `celery -A api.core.celery_app worker --loglevel=info`

#### Redis Service
- **Name:** oop-journey-redis
- **Type:** Redis

### Step 3: Set Environment Variables

In Render dashboard, set these for each service:

#### For API Service:
```
SECRET_KEY=<generate-random-64-char-string>
DATABASE_URL=<cockroachdb-connection-string>
REDIS_URL=<redis-cloud-url>
FRONTEND_URL=https://python-oop-journey.onrender.com
ALLOWED_ORIGINS=https://python-oop-journey.onrender.com
```

#### For Web Service:
```
NEXT_PUBLIC_API_URL=https://oop-journey-api.onrender.com
NEXT_PUBLIC_APP_URL=https://python-oop-journey.onrender.com
```

### Step 4: Deploy

1. Click "Apply" in Render dashboard
2. Wait for build to complete
3. Check logs for any errors
4. Visit deployed URL

---

## Troubleshooting

### Issue: Node.js not found

```bash
# Check if installed
which node

# If not, install via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20
```

### Issue: npm install fails

```bash
# Clear cache
npm cache clean --force

# Delete node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Issue: TypeScript errors

```bash
cd apps/web

# Check specific errors
npx tsc --noEmit

# Fix auto-fixable issues
npx eslint . --fix
```

### Issue: Database connection fails

```bash
# Test connection string
psql $DATABASE_URL -c "SELECT 1"

# Check if migrations applied
cd apps/api
alembic current
alembic history

# Reset migrations (DANGER: deletes data)
# alembic downgrade base
# alembic upgrade head
```

### Issue: Build fails on Render

1. Check Render logs for specific error
2. Ensure environment variables are set
3. Verify `render.yaml` syntax
4. Try manual deploy from Render dashboard

---

## Quick Start Commands

### Daily Development

```bash
# 1. Navigate to project
cd ~/projects/python-oop-journey/website-playground

# 2. Pull latest changes
git pull origin main

# 3. Install any new dependencies
npm install
cd apps/api && pip install -r requirements.txt && cd ../..

# 4. Start development
cd apps/api && python -m uvicorn api.main:app --reload &
cd apps/web && npm run dev
```

### Before Committing

```bash
# 1. Type check
cd apps/web && npm run type-check

# 2. Build test
cd apps/web && npm run build

# 3. Test backend
cd apps/api && python -c "from api.main import app"

# 4. Commit
git add .
git commit -m "your message"
git push origin main
```

---

## Additional Resources

### Documentation
- `AGENTS.md` - Agent instructions
- `CODING_STANDARDS.md` - Code standards
- `RECURRING_MISTAKES.md` - Common issues
- `ROOT_CAUSE_ANALYSIS.md` - Issue analysis

### Useful Commands
```bash
# Check all routes
npm run build 2>&1 | grep "Route"

# Check bundle size
npm run analyze

# Test API endpoints
curl http://localhost:8000/health

# View logs
tail -f apps/api/log.txt
```

---

## Support

If you encounter issues:
1. Check `TROUBLESHOOTING_DEPLOYS.md` (in `_archive/old_docs/`)
2. Review Render logs
3. Check GitHub Issues
4. Contact project maintainer

---

**END OF SETUP GUIDE**

For updates, check the repository README or memory.md file.

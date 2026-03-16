# Render Web Services

## Overview

Render hosts web apps in various languages: Node.js, Python, Go, Ruby, Rust, Elixir.

**Our Stack:** Python (FastAPI) + Node.js (Next.js)

## Creating a Web Service

### From Git Repository (Our Method)

1. Dashboard → **New > Web Service**
2. Select **Git Provider** → Connect GitHub
3. Select repository: `python-oop-journey`
4. Configure:
   - **Name:** `oop-journey-api`
   - **Region:** Frankfurt (EU Central)
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r apps/api/requirements.txt`
   - **Start Command:** `cd apps/api && alembic upgrade head && uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**

## Critical Requirements

### Must Bind to Port

Your app MUST bind to a port on host `0.0.0.0`:

```python
# FastAPI/Uvicorn
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

**Default PORT:** `10000` (can override with env var)

### Environment Variables

Set in Dashboard → Environment:
- `DATABASE_URL`
- `REDIS_URL`
- `SECRET_KEY`
- `JWT_SECRET`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `FRONTEND_URL`
- `ENVIRONMENT`

## Build & Deploy Process

```
1. Build Command runs
   └── Install dependencies
   
2. Pre-deploy Command (optional)
   └── Database migrations
   
3. Start Command runs
   └── App starts and binds to PORT
   
4. Health check (if configured)
   └── Render verifies app is responsive
   
5. Deploy complete
   └── Zero-downtime switchover
```

## Timeouts

| Command | Timeout |
|---------|---------|
| Build | 1 hour |
| Pre-deploy | 1 hour |
| Start | 60 seconds |

## Free Tier Limitations

- **Instance:** Spins down after 15 min idle (cold start ~2s)
- **Bandwidth:** 100GB/month
- **Build minutes:** 500/month
- **Disk:** Ephemeral (data lost on deploy)
- **No:** SSH access, persistent disks, multiple instances

## Auto-Deploys

Enabled by default. On every push to `main`:
1. Render detects commit
2. Runs build command
3. Deploys new version
4. Zero-downtime switchover

**Skip auto-deploy:**
```bash
git commit -m "[skip render] Update docs"
```

## Common Errors

### "Exited with status 1"
- Check logs for Python traceback
- Usually: import error, missing env var, or migration fail

### "Bind to 0.0.0.0 required"
- Add `--host 0.0.0.0` to uvicorn command

### "Port not detected"
- App must bind within 60 seconds
- Use `$PORT` env var

### "Build successful but deploy fails"
- Check start command
- Verify all env vars set
- Check migration syntax

## Useful Commands

```bash
# View logs
render logs

# Manual deploy
render deploy

# Restart service
render deploy --restart

# SSH into instance (paid only)
render ssh
```

## Health Checks

Optional but recommended. Configure in Advanced:
- **Path:** `/api/v1/health`
- Render checks this before marking deploy as live

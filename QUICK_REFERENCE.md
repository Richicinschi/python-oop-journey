# Quick Reference - Deployment Summary

One-page reference for deploying Python OOP Journey.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    YOUR GODADDY DOMAIN                       │
│                  https://yourdomain.com                      │
└───────────────────────────┬──────────────────────────────────┘
                            │
            ┌───────────────┴────────────────┐
            ▼                                ▼
┌──────────────────────┐        ┌──────────────────────┐
│  Cloudflare Pages    │        │      Fly.io          │
│  Next.js Frontend    │───────▶│  FastAPI Backend     │
│  $0/month            │        │  $0/month            │
└──────────────────────┘        └──────────┬───────────┘
                                           │
                              ┌────────────┴───────────┐
                              ▼                        ▼
                    ┌─────────────────┐      ┌─────────────────┐
                    │   CockroachDB   │      │    Upstash      │
                    │   PostgreSQL    │      │     Redis       │
                    │   $0/month      │      │   $0/month      │
                    └─────────────────┘      └─────────────────┘
```

---

## Account Creation Checklist

- [ ] GitHub (https://github.com/signup)
- [ ] CockroachDB (https://cockroachlabs.cloud/signup) - GitHub, no CC
- [ ] Upstash (https://console.upstash.com) - GitHub, no CC
- [ ] Fly.io (`fly auth signup`) - no CC
- [ ] Cloudflare (https://dash.cloudflare.com/sign-up) - no CC
- [ ] Google Cloud (https://console.cloud.google.com) - free

---

## Deployment Commands

### 1. Database (CockroachDB)
```
Dashboard: https://cockroachlabs.cloud
→ Create Cluster (Serverless)
→ Create User
→ Copy Connection String
```

### 2. Cache (Upstash)
```
Dashboard: https://console.upstash.com
→ Copy Redis Endpoint
```

### 3. Backend (Fly.io)
```bash
cd apps/api

# Initialize
fly launch --name oop-journey-api --region ord --no-deploy

# Set secrets
fly secrets set DATABASE_URL="postgresql://..."
fly secrets set REDIS_URL="rediss://..."
fly secrets set SECRET_KEY="random-64-chars"
fly secrets set JWT_SECRET="random-32-chars"
fly secrets set GOOGLE_CLIENT_ID="..."
fly secrets set GOOGLE_CLIENT_SECRET="..."
fly secrets set FRONTEND_URL="https://yourdomain.com"

# Deploy
fly deploy
```

**URL:** `https://oop-journey-api.fly.dev`

### 4. Frontend (Cloudflare Pages)
```
Dashboard: https://dash.cloudflare.com/pages
→ Create Project
→ Connect GitHub
→ Build Command: cd apps/web && npm install && npm run build
→ Output: apps/web/dist
→ Env Vars: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_GOOGLE_CLIENT_ID
```

**URL:** `https://oop-journey.pages.dev`

### 5. Domain (GoDaddy)
```
Cloudflare: Custom Domains → Add yourdomain.com
→ Copy nameservers

GoDaddy: DNS → Nameservers → Custom
→ Paste Cloudflare nameservers
→ Save
```

**Wait:** 5-30 minutes for DNS

### 6. Google OAuth Update
```
Google Cloud: APIs & Services → Credentials
→ Add redirect URIs:
   https://yourdomain.com/auth/callback/google
→ Add JavaScript origins:
   https://yourdomain.com
→ Save
```

---

## Environment Variables

### Backend (Fly.io)
```bash
DATABASE_URL=postgresql://user:pass@host:26257/defaultdb?sslmode=require
REDIS_URL=rediss://default:pass@host:6379
SECRET_KEY=openssl rand -hex 32
JWT_SECRET=openssl rand -hex 32
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxx
FRONTEND_URL=https://yourdomain.com
ENVIRONMENT=production
```

### Frontend (Cloudflare)
```bash
NEXT_PUBLIC_API_URL=https://oop-journey-api.fly.dev
NEXT_PUBLIC_GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
```

---

## Testing Checklist

- [ ] Visit `https://yourdomain.com` - loads
- [ ] Click Login → redirects to Google
- [ ] Sign in → back to site, logged in
- [ ] Solve a problem → code runs
- [ ] Progress saves after refresh
- [ ] Works on mobile

---

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| DNS not working | Wait 30 min, clear browser cache |
| CORS errors | Update FRONTEND_URL in Fly.io |
| Google OAuth error | Check redirect URI matches exactly |
| Database fail | Verify sslmode=require in connection string |
| Build fail | Check build command has `npm install` |

---

## Useful Commands

```bash
# View backend logs
fly logs

# SSH into backend
fly ssh console

# Restart backend
fly apps restart oop-journey-api

# View secrets
fly secrets list

# Update secret
fly secrets set KEY=value

# Deploy backend
fly deploy

# Deploy frontend (auto on git push)
git add . && git commit -m "Update" && git push
```

---

## Free Tier Limits

| Service | Limit | Est. Users |
|---------|-------|------------|
| CockroachDB | 5GB, 1M req/mo | ~5,000 |
| Upstash | 10K req/day | ~1,000 |
| Fly.io | 3 VMs, 160GB | Unlimited* |
| Cloudflare | Unlimited | Unlimited |
| Google OAuth | Unlimited | Unlimited |

*Fly.io VMs sleep after 5 min idle (2s cold start)

---

## Cost Summary

| Item | Cost |
|------|------|
| GoDaddy Domain | $12/year |
| Everything Else | $0 |
| **Total** | **$12/year** |

---

## Support Resources

- Full tutorial: `COMPLETE_TUTORIAL.md`
- Free options: `FREE_DEPLOYMENT_OPTIONS.md`
- Quick deploy: `FREE_DEPLOY_QUICKSTART.md`

---

**Status: ✅ Ready to Deploy!**

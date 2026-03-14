# Deployment Checklist - Netlify + Google OAuth

Use this checklist to deploy your Python OOP Journey platform.

---

## Pre-Deployment

- [ ] **Domain Ready**
  - [ ] Purchased domain on GoDaddy
  - [ ] Access to DNS settings

- [ ] **Code Ready**
  - [ ] All features tested locally
  - [ ] Pushed to GitHub
  - [ ] Google OAuth code added (see files below)

---

## Step 1: Database (Supabase) - 10 mins

- [ ] Create account at https://supabase.com
- [ ] Create new project
- [ ] Save database password
- [ ] Copy connection string (Settings → Database)
- [ ] **SAVE:** `DATABASE_URL` for later

---

## Step 2: Redis (Upstash) - 5 mins

- [ ] Create account at https://upstash.com
- [ ] Create Redis database
- [ ] Copy REST URL and Token
- [ ] **SAVE:** `REDIS_URL` for later

---

## Step 3: Google OAuth - 15 mins

- [ ] Go to https://console.cloud.google.com
- [ ] Create new project "Python OOP Journey"
- [ ] Enable "Google People API"
- [ ] Configure OAuth Consent Screen:
  - [ ] User Type: External
  - [ ] App name: "Python OOP Journey"
  - [ ] User support email: your email
  - [ ] Developer contact: your email
  - [ ] Scopes: openid, email, profile
- [ ] Create OAuth Credentials:
  - [ ] Web application
  - [ ] Name: "OOP Journey Web"
  - [ ] Authorized origins: `http://localhost:3000`
  - [ ] Authorized redirect URIs: `http://localhost:3000/auth/callback/google`
- [ ] **SAVE:** `Client ID` and `Client Secret`

---

## Step 4: Backend (Render) - 20 mins

- [ ] Create account at https://render.com
- [ ] New Web Service
- [ ] Connect GitHub repo
- [ ] Configure:
  - [ ] Name: `oop-journey-api`
  - [ ] Environment: Python 3
  - [ ] Build: `pip install -r apps/api/requirements.txt`
  - [ ] Start: `cd apps/api && uvicorn api.main:app --host 0.0.0.0 --port $PORT`
- [ ] Add Environment Variables:
  ```
  DATABASE_URL=postgresql+asyncpg://... (from Supabase)
  REDIS_URL=rediss://... (from Upstash)
  SECRET_KEY=(generate: openssl rand -hex 32)
  JWT_SECRET=(generate: openssl rand -hex 32)
  GOOGLE_CLIENT_ID=(from Google Console)
  GOOGLE_CLIENT_SECRET=(from Google Console)
  FRONTEND_URL=http://localhost:3000 (update after Netlify)
  ENVIRONMENT=production
  ```
- [ ] Deploy
- [ ] **SAVE:** Render URL (e.g., `https://oop-journey-api.onrender.com`)

### Post-Deploy (Render Shell)
- [ ] Open Render dashboard → Shell
- [ ] Run: `cd apps/api && alembic upgrade head`
- [ ] Verify: Database tables created

---

## Step 5: Frontend (Netlify) - 15 mins

### 5.1 Prepare Code

- [ ] Create `apps/web/netlify.toml`:
  ```toml
  [build]
    base = "apps/web"
    publish = "dist"
    command = "npm run build"

  [[redirects]]
    from = "/api/*"
    to = "https://oop-journey-api.onrender.com/api/:splat"
    status = 200

  [[redirects]]
    from = "/*"
    to = "/index.html"
    status = 200
  ```

- [ ] Update `apps/web/next.config.js`:
  ```javascript
  const nextConfig = {
    output: 'export',
    distDir: 'dist',
    images: { unoptimized: true },
  };
  module.exports = nextConfig;
  ```

- [ ] Create `apps/web/.env.production`:
  ```
  NEXT_PUBLIC_API_URL=https://oop-journey-api.onrender.com
  NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
  ```

- [ ] Commit and push to GitHub

### 5.2 Deploy

- [ ] Go to https://netlify.com
- [ ] Add new site → Import from Git
- [ ] Select repo
- [ ] Configure:
  - [ ] Base directory: `apps/web`
  - [ ] Build command: `npm run build`
  - [ ] Publish: `dist`
- [ ] Add Environment Variables:
  ```
  NEXT_PUBLIC_API_URL=https://oop-journey-api.onrender.com
  NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
  ```
- [ ] Deploy
- [ ] **SAVE:** Netlify URL (e.g., `https://clever-fox-123.netlify.app`)

---

## Step 6: Connect Domain (GoDaddy) - 10 mins

### Option A: Netlify DNS (Recommended)

- [ ] Netlify Dashboard → Domain settings
- [ ] "Add custom domain" → enter your GoDaddy domain
- [ ] "Set up Netlify DNS"
- [ ] Copy 4 nameservers (e.g., `dns1.p01.nsone.net`)
- [ ] Go to GoDaddy:
  - [ ] DNS → Nameservers
  - [ ] Change to Custom
  - [ ] Paste Netlify nameservers
  - [ ] Save
- [ ] Wait 24-48 hours for propagation

### Option B: CNAME Record

- [ ] GoDaddy DNS Management
- [ ] Delete existing A records
- [ ] Add CNAME:
  - [ ] Type: CNAME
  - [ ] Name: `@` or `www`
  - [ ] Value: `your-site.netlify.app`
  - [ ] TTL: 600

---

## Step 7: Update Redirect URIs - 5 mins

- [ ] Go to Google Cloud Console
- [ ] APIs & Services → Credentials
- [ ] Edit OAuth client
- [ ] Add to Authorized origins:
  - [ ] `https://yourdomain.com`
  - [ ] `https://www.yourdomain.com`
- [ ] Add to Authorized redirect URIs:
  - [ ] `https://yourdomain.com/auth/callback/google`
  - [ ] `https://www.yourdomain.com/auth/callback/google`
- [ ] Save

---

## Step 8: Update Environment Variables - 5 mins

### Render Dashboard

- [ ] Update `FRONTEND_URL`:
  ```
  FRONTEND_URL=https://yourdomain.com
  ```
- [ ] Redeploy (Render auto-deploys on env change)

### Netlify Dashboard

- [ ] No changes needed (uses same API URL)

---

## Step 9: Enable HTTPS - Auto

- [ ] Netlify auto-provisions SSL certificate
- [ ] Verify: Domain settings → HTTPS
- [ ] Enable "Force HTTPS"

---

## Step 10: Testing - 15 mins

- [ ] Visit `https://yourdomain.com`
- [ ] **Homepage loads**
- [ ] Click "Login"
- [ ] **Redirects to Google**
- [ ] Complete Google auth
- [ ] **Back to app, logged in**
- [ ] Verify profile shows your name/email
- [ ] Navigate to a problem
- [ ] **Solve a problem**
- [ ] Run code execution
- [ ] **Progress saves**
- [ ] Logout
- [ ] Login again (should remember you)

---

## Optional: Enhancements

### Email (SendGrid) - For notifications

- [ ] Create SendGrid account
- [ ] Verify sender email
- [ ] Create API key
- [ ] Add to Render env:
  ```
  SENDGRID_API_KEY=SG.xxx
  FROM_EMAIL=noreply@yourdomain.com
  ```

### AI Hints (OpenAI)

- [ ] Get OpenAI API key
- [ ] Add to Render env:
  ```
  OPENAI_API_KEY=sk-...
  AI_HINT_MODEL=gpt-4o-mini
  ```

### Monitoring (Sentry)

- [ ] Create Sentry account
- [ ] Add project
- [ ] Copy DSN
- [ ] Add to Render env:
  ```
  SENTRY_DSN=https://...@sentry.io/...
  ```
- [ ] Add to Netlify env:
  ```
  NEXT_PUBLIC_SENTRY_DSN=same-dsn
  ```

### Uptime Monitoring

- [ ] Create UptimeRobot account
- [ ] Add monitors:
  - [ ] `https://yourdomain.com`
  - [ ] `https://oop-journey-api.onrender.com/health`

---

## Troubleshooting

### Google OAuth Error: "redirect_uri_mismatch"
- [ ] Check redirect URI in Google Console matches exactly
- [ ] Must include `https://`
- [ ] No trailing slash

### CORS Errors
- [ ] Check `FRONTEND_URL` in Render matches your domain
- [ ] Verify `NEXT_PUBLIC_API_URL` is correct

### Database Connection Failed
- [ ] Use connection pooling URL from Supabase
- [ ] Check password is correct

### Build Fails
- [ ] Check Node version 18+
- [ ] Check Python version 3.11+

---

## Post-Launch

- [ ] Share with friends!
- [ ] Monitor error logs (Sentry/Render)
- [ ] Check usage metrics (Supabase/Render dashboards)
- [ ] Collect feedback

**🎉 Congratulations! Your platform is live!**

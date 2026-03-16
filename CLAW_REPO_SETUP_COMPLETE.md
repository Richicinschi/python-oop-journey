# CLAW Repository Setup - Complete Guide

## ✅ What You Have Now

### 1. Confidentiality Verified
**Report:** `CONFIDENTIALITY_REPORT.md`

- ✅ No real API keys
- ✅ No real database credentials
- ✅ Only placeholder env values
- ✅ Safe to upload to new GitHub repo

**Low-risk items found:**
- Your Windows username `digitalnomad` in paths
- Your first name `Richard` in USER.md
- Public Render URLs (already public)
- Test data (`test@example.com`)

### 2. CLAW Memory Files (8 files)

All configured for website repair with **push permissions enabled**:

| File | Purpose | Push Permission |
|------|---------|-----------------|
| `AGENTS.md` | Mission directive + git workflow | ✅ YES |
| `IDENTITY.md` | "The Repair Daemon" persona | ✅ YES |
| `SOUL.md` | Technical, verification-obsessed | ✅ YES |
| `USER.md` | Richard/digitalnomad profile | ✅ YES |
| `MEMORY.md` | Current issues & progress | ✅ YES |
| `BOOTSTRAP.md` | 5-phase startup script | ✅ YES |
| `HEARTBEAT.md` | Periodic health checks | ✅ YES |
| `TOOLS.md` | Environment & commands | ✅ YES |

### 3. CLAW Config Files (`.claw/`)

| File | Purpose |
|------|---------|
| `soul.yaml` | Project structure, build steps |
| `instructions.md` | Setup guide |
| `test-plan.yaml` | Critical path tests |
| `shell-commands.yaml` | Common commands |
| `status.yaml` | Current task tracking |
| `git-config.yaml` | **NEW** Git permissions config |

### 4. Complete Website

**Location:** `website-playground/`
- Next.js 14 frontend
- FastAPI backend
- 40+ routes, 433 problem pages
- Monaco Editor (local)
- Current issue: 500 errors on week/problem pages

### 5. Complete Curriculum

**Location:** `python-oop-journey-v2/`
- 9 weeks (0-8)
- 453 exercises
- 7,456+ tests passing
- Production-ready

### 6. Agency Agents Library

**Location:** `agency-agents/`
- Full agent collection
- All specializations
- Ready for use

## 🚀 Setup Steps

### Step 1: Run Setup Script

```bash
cd c:\Users\digitalnomad\Documents\oopkimi

# In Git Bash or WSL:
bash setup-claw-repo.sh python-oop-journey-claw Richicinschi
```

This creates `/tmp/claw-repo-setup/` with all files ready to push.

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name:** `python-oop-journey-claw`
3. **Visibility:** Public (or Private)
4. **❌ DO NOT** check "Initialize with README"
5. **❌ DO NOT** add .gitignore
6. **❌ DO NOT** add license
7. Click "Create repository"

### Step 3: Push to GitHub

```bash
cd /tmp/claw-repo-setup

git remote add origin https://github.com/Richicinschi/python-oop-journey-claw.git
git branch -M main
git push -u origin main
```

### Step 4: Connect Kimi Claw

1. Go to Kimi Claw dashboard
2. Click "Connect Repository"
3. Select: `Richicinschi/python-oop-journey-claw`
4. Claw will auto-detect `.claw/soul.yaml`
5. Claw reads all memory files
6. **Claw starts fixing immediately**

### Step 5: Monitor Progress

Claw will:
1. ✅ Run bootstrap sequence (AGENTS.md → MEMORY.md → TOOLS.md)
2. ✅ Check current status (`.claw/status.yaml`)
3. ✅ Start backend: `cd apps/api && uvicorn api.main:app --reload`
4. ✅ Start frontend: `cd apps/web && npm run dev`
5. ✅ Test: `curl http://localhost:8000/health`
6. ✅ Diagnose 500 errors
7. ✅ Push commits as it fixes issues

## 📋 What CLAW Will Fix

### Primary Issues (from MEMORY.md)

1. **Week/Problem Detail Pages (500 Errors)**
   - Root cause: Server components fail to load curriculum data
   - Test: `curl http://localhost:8000/api/v1/curriculum/weeks/week00_getting_started`
   - Files: `apps/web/app/(dashboard)/weeks/[slug]/page.tsx`

2. **Database Migration Conflict**
   - Local: Uses SQLite (no conflict)
   - Note: Production CockroachDB requires manual fix

3. **Build vs Runtime Discrepancy**
   - Build succeeds but runtime fails
   - CLAW will test actual HTTP responses

### CLAW's Approach

```bash
# 1. Reproduce
npm run build  # Verify build works
curl http://localhost:3000/weeks/week00_getting_started  # See 500 error

# 2. Diagnose
curl http://localhost:8000/api/v1/curriculum/weeks/week00_getting_started
# Check if API returns data

# 3. Fix
# Modify data loading in page.tsx
# Commit: git commit -m "[CLAW] fix: Week detail page data loading"

# 4. Verify
curl http://localhost:3000/weeks/week00_getting_started | grep -q "week"
# Should return HTML without 500

# 5. Push
git push origin main
```

## 🔐 Git Permissions Summary

**In this dedicated CLAW repo, CLAW CAN:**

✅ Create branches: `claw/20260315-fix-500`
✅ Commit: `git commit -m "[CLAW] fix: ..."`
✅ Push: `git push origin <branch>`
✅ Merge to main after verification
✅ Delete branches after merge
✅ Force push (feature branches only)

**CLAW CANNOT:**
❌ Access production database
❌ Access your original repo
❌ Push to production Render (different repo)

## 📊 Expected Timeline

| Task | Estimate |
|------|----------|
| Bootstrap & health checks | 5 min |
| Diagnose 500 errors | 15-30 min |
| Fix data loading | 1-2 hours |
| Test all week pages | 30 min |
| Test all problem pages | 1 hour |
| Polish & commit | 30 min |
| **Total** | **4-6 hours** |

## 🔔 Notifications

Claw will commit progress every 30 minutes or after each fix:

```
[CLAW] fix: Week detail page 500 error - Part 1
[CLAW] fix: Curriculum data loading in server components
[CLAW] test: Verify all 9 week pages load correctly
[CLAW] fix: Problem detail page data fetching
[CLAW] docs: Update MEMORY.md with fixes applied
```

## 🆘 If Something Goes Wrong

Claw will:
1. Stop and document the issue
2. Update `.claw/status.yaml` with blocker
3. Ask for direction (if configured)
4. Never force push to main
5. Keep backups in git history

You can always:
- Check git log: `git log --oneline`
- Rollback: `git revert <commit>`
- Reset: `git reset --hard HEAD~1`
- Review changes: `git diff HEAD~5`

## ✅ Checklist

Before connecting to Kimi Claw:

- [ ] Run `setup-claw-repo.sh`
- [ ] Create GitHub repo `python-oop-journey-claw`
- [ ] Push to GitHub
- [ ] Verify files uploaded correctly
- [ ] Connect Kimi Claw
- [ ] Watch CLAW bootstrap
- [ ] Monitor first commits

## 📁 Files Ready

All files are in `c:\Users\digitalnomad\Documents\oopkimi\`:

```
oopkimi/
├── AGENTS.md (updated with push permissions)
├── IDENTITY.md
├── SOUL.md
├── USER.md
├── MEMORY.md
├── BOOTSTRAP.md
├── HEARTBEAT.md
├── TOOLS.md
├── .claw/
│   ├── soul.yaml
│   ├── instructions.md
│   ├── test-plan.yaml
│   ├── shell-commands.yaml
│   ├── status.yaml
│   └── git-config.yaml
├── website-playground/ (full app)
├── python-oop-journey-v2/ (curriculum)
├── agency-agents/ (agent library)
├── docs/ (documentation)
└── _archive/ (organized old files)
```

## 🎉 Next Action

Run this command:

```bash
cd c:\Users\digitalnomad\Documents\oopkimi
bash setup-claw-repo.sh
```

Then follow the printed instructions to create GitHub repo and push.

**CLAW will be fixing your website autonomously within 10 minutes!**

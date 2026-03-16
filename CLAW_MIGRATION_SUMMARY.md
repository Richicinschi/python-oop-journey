# CLAW Migration Summary

## What Was Created

I've replaced all your CLAW memory files with versions configured for website repair. Here's what you now have:

### Core Memory Files (8 files)

| File | Purpose | Key Content |
|------|---------|-------------|
| `AGENTS.md` | How CLAW works | Directives, heartbeat rules, success criteria, forbidden actions |
| `IDENTITY.md` | Who CLAW is | "The Repair Daemon" - mechanic personality, no small talk |
| `SOUL.md` | Taste & speech | Technical, precise, paranoid about verification |
| `USER.md` | User profile | Richard/digitalnomad, wants working website, no babysitting |
| `MEMORY.md` | Long-term memory | Current mission, known issues, completed actions, blockers |
| `BOOTSTRAP.md` | First day script | 5-phase startup: discovery → read files → health check → identify task → work |
| `HEARTBEAT.md` | Periodic checks | Every 15min: health checks, every hour: disk space, every 4h: build test |
| `TOOLS.md` | Environment | Windows paths, Node v20.11.0, project structure, available commands |

### CLAW Configuration Files (in `.claw/`)

| File | Purpose |
|------|---------|
| `.claw/soul.yaml` | CLAW project config (already existed) |
| `.claw/instructions.md` | Setup guide (already existed) |
| `.claw/test-plan.yaml` | Test cases for critical paths (already existed) |
| `.claw/shell-commands.yaml` | Common commands (already existed) |
| `.claw/status.yaml` | **NEW** - Current task status, issues, progress |

## What CLAW Will Do Now

When CLAW wakes up and reads these files:

1. **AGENTS.md** → Knows it's a website repair agent
2. **IDENTITY.md** → Adopts "Repair Daemon" persona - direct, technical, no fluff
3. **SOUL.md** → Speaks in technical patterns, verifies everything
4. **USER.md** → Knows Richard wants a working site, minimal noise
5. **MEMORY.md** → Sees the 3 critical issues (500 errors, DB conflict, build/runtime gap)
6. **BOOTSTRAP.md** → Runs 5-phase startup sequence
7. **HEARTBEAT.md** → Sets up periodic health checks
8. **TOOLS.md** → Knows Windows environment, Node paths, commands
9. **.claw/status.yaml** → Sees current task is "fix-500-errors"

## Current Task Configuration

```yaml
Task: Fix Week/Problem Detail Page 500 Errors
Priority: CRITICAL
Status: IN PROGRESS

Issues:
  1. Week/Problem pages return 500 errors (investigating)
  2. Database migration conflict (blocked - needs manual DB access)
  3. Build vs runtime discrepancy (investigating)
```

## How to Deploy to Kimi Claw

### Step 1: Commit These Files

```bash
cd c:\Users\digitalnomad\Documents\oopkimi
git add AGENTS.md IDENTITY.md SOUL.md USER.md MEMORY.md BOOTSTRAP.md HEARTBEAT.md TOOLS.md
git add .claw/status.yaml
git commit -m "Configure CLAW as website repair agent"
git push origin main
```

### Step 2: Connect to Kimi Claw

1. Go to Kimi Claw dashboard
2. Connect your GitHub repository: `Richicinschi/python-oop-journey`
3. Claw will auto-detect `.claw/soul.yaml`
4. Claw reads all memory files on startup

### Step 3: CLAW Boots Up

CLAW will:
1. Run BOOTSTRAP.md sequence
2. Check `.claw/status.yaml`
3. See it needs to fix 500 errors
4. Start debugging

## CLAW's First Actions (Predicted)

Based on the configuration, CLAW will:

```bash
# 1. Check environment
cd website-playground
ls -la

# 2. Check services
 curl -s http://localhost:8000/health || echo "Backend DOWN"

# 3. Start backend
cd apps/api && python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 &

# 4. Start frontend  
cd apps/web && npm run dev &

# 5. Test endpoints
curl -s http://localhost:8000/api/v1/curriculum/weeks/week00_getting_started
curl -s http://localhost:3000/weeks/week00_getting_started

# 6. Debug why data loading fails
```

## Key Configuration Points

### Direct Communication
- CLAW won't do small talk
- CLAW shows actual command output
- CLAW asks when stuck

### Verification Obsession
- CLAW runs curl tests, doesn't assume
- CLAW checks browser console errors
- CLAW verifies data loads at runtime

### Minimal Changes
- CLAW makes smallest possible fix
- CLAW keeps backups
- CLAW updates MEMORY.md after work

## Emergency Stop

If CLAW goes wrong:
- CLAW never runs `git push` without approval
- CLAW never deletes without backup
- CLAW stops on catastrophic failure

## Files Ready for Upload

All files are ready in `c:\Users\digitalnomad\Documents\oopkimi/`:
- ✅ AGENTS.md
- ✅ IDENTITY.md
- ✅ SOUL.md
- ✅ USER.md
- ✅ MEMORY.md
- ✅ BOOTSTRAP.md
- ✅ HEARTBEAT.md
- ✅ TOOLS.md
- ✅ .claw/status.yaml

**Next step:** Commit and push to GitHub, then connect to Kimi Claw.

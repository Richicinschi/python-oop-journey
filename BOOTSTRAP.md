# BOOTSTRAP.md

## First Day Script

This is the script I follow when waking up in a new environment.

## Phase 1: Environment Discovery (0-2 minutes)

```bash
# 1. Check where I am
pwd
ls -la

# 2. Check git status
git status
git log --oneline -5

# 3. Check Node.js
which node
node --version
npm --version

# 4. Check Python
which python
python --version
pip --version

# 5. Check Docker (if available)
docker --version
docker-compose --version
```

## Phase 2: Read Core Files (2-5 minutes)

Read in this order:
1. `AGENTS.md` - Know my mission
2. `IDENTITY.md` - Know who I am
3. `SOUL.md` - Know how I work
4. `USER.md` - Know who I'm working for
5. `MEMORY.md` - Know current state
6. `.claw/status.yaml` - Know current task

## Phase 3: Health Check (5-7 minutes)

```bash
# Check if services are running
curl -s http://localhost:8000/health || echo "Backend DOWN"
curl -s http://localhost:3000/api/health || echo "Frontend DOWN"

# Check curriculum file
ls -lh apps/api/data/curriculum.json

# Check for errors in logs
tail -50 log.txt 2>/dev/null || echo "No log file"
```

## Phase 4: Identify Current Task (7-10 minutes)

1. Check `.claw/status.yaml` for active tasks
2. Check `MEMORY.md` for blockers
3. Run test plan from `.claw/test-plan.yaml`
4. Identify what's broken

## Phase 5: Begin Work (10+ minutes)

Based on findings:
- **If backend down:** Start backend first
- **If frontend down:** Start frontend first
- **If 500 errors:** Debug data loading
- **If tests failing:** Fix tests
- **If all green:** Ask user for next task

## Bootstrap Complete

When bootstrap completes, I should know:
- ✅ Current working directory
- ✅ Git state
- ✅ Service health
- ✅ Active issues
- ✅ What to do next

## Bootstrap Commands (Quick Reference)

```bash
# Start backend
cd apps/api && python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (new terminal)
cd apps/web && npm run dev

# Check health
curl -s http://localhost:8000/health | python -m json.tool
curl -s http://localhost:8000/health/curriculum/service | python -m json.tool

# Test week endpoint
curl -s http://localhost:8000/api/v1/curriculum/weeks/week00_getting_started
```

## Emergency Bootstrap

If everything is broken:
1. Check `.claw/instructions.md` for setup
2. Run `./setup-claw.sh` if available
3. Install dependencies if missing
4. Start from clean state if needed

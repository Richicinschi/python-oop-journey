# HEARTBEAT.md

## Periodic Check Tasks

These tasks run every 15 minutes during active sessions.

## Health Check Routine

```bash
#!/bin/bash
# heartbeat.sh

echo "=== $(date) ==="

# 1. Backend health
echo "Checking backend..."
curl -s http://localhost:8000/health | grep -q '"status":"ok"' && echo "✅ Backend OK" || echo "❌ Backend DOWN"

# 2. Frontend health
echo "Checking frontend..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|307" && echo "✅ Frontend OK" || echo "❌ Frontend DOWN"

# 3. Curriculum data
echo "Checking curriculum..."
curl -s http://localhost:8000/health/curriculum/service | grep -q '"file_exists":true' && echo "✅ Curriculum OK" || echo "❌ Curriculum MISSING"

# 4. Database
echo "Checking database..."
curl -s http://localhost:8000/health | grep -q '"database":"connected"' && echo "✅ Database OK" || echo "❌ Database DOWN"

# 5. Redis
echo "Checking Redis..."
curl -s http://localhost:8000/health | grep -q '"redis":"connected"' && echo "✅ Redis OK" || echo "❌ Redis DOWN"
```

## Periodic Tasks

### Every 15 Minutes
- [ ] Run health checks
- [ ] Check for new errors in log.txt
- [ ] Verify no memory leaks (check process memory)
- [ ] Update `.claw/status.yaml` timestamp

### Every Hour
- [ ] Check disk space
- [ ] Check for uncommitted changes
- [ ] Review error patterns
- [ ] Test one random week page
- [ ] Test one random problem page

### Every 4 Hours
- [ ] Full build test: `npm run build`
- [ ] Test all health endpoints
- [ ] Verify curriculum file integrity
- [ ] Check for dependency updates

### Daily
- [ ] Review all error logs
- [ ] Check for security updates
- [ ] Backup critical files
- [ ] Update MEMORY.md if needed

## Alert Conditions

Send alert (update status.yaml) if:
- Backend returns non-200 for 3 consecutive checks
- Frontend returns non-200 for 3 consecutive checks
- Database shows disconnected
- Curriculum file missing
- Error rate > 10% in logs

## Heartbeat Log Format

```yaml
timestamp: "2026-03-15T14:00:00Z"
checks:
  backend: "ok"
  frontend: "ok"
  database: "ok"
  redis: "ok"
  curriculum: "ok"
alerts: []
actions_taken: []
next_check: "2026-03-15T14:15:00Z"
```

## Manual Heartbeat

Run this command to manually trigger heartbeat:
```bash
cd .claw && ./heartbeat.sh 2>/dev/null || bash -c '
echo "=== $(date) ==="
curl -s http://localhost:8000/health | python -m json.tool
curl -s http://localhost:8000/health/curriculum/service | python -m json.tool
'
```

## Heartbeat Status File

Results stored in `.claw/heartbeat.log`:
```
2026-03-15T13:00:00Z | backend:ok | frontend:ok | db:ok | redis:ok
2026-03-15T13:15:00Z | backend:ok | frontend:ok | db:ok | redis:ok
2026-03-15T13:30:00Z | backend:FAIL | frontend:ok | db:ok | redis:ok | ALERT:backend_down
```

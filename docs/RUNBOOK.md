# Operations Runbook

This runbook contains procedures for common operational tasks and incident response.

## Table of Contents

- [On-Call Procedures](#on-call-procedures)
- [Common Issues](#common-issues)
- [Scaling Procedures](#scaling-procedures)
- [Incident Response](#incident-response)
- [Maintenance Windows](#maintenance-windows)
- [Emergency Contacts](#emergency-contacts)

## On-Call Procedures

### Daily Checks

```bash
# 1. Check system health
curl https://oopjourney.com/api/health
curl https://oopjourney.com/nginx-health

# 2. Check container status
docker-compose -f docker-compose.prod.yml ps

# 3. Check recent errors
docker-compose -f docker-compose.prod.yml logs --since=24h api | grep ERROR

# 4. Check disk space
df -h

# 5. Check memory usage
free -h
```

### Alert Response

1. **Acknowledge alert** within 5 minutes
2. **Assess severity** (see Incident Severity below)
3. **Execute runbook** for specific alert type
4. **Escalate** if unable to resolve within SLA
5. **Document** actions taken in incident log

## Common Issues

### Issue: Site is Down

**Symptoms:** Health check fails, users report 502/503 errors

**Checklist:**

```bash
# 1. Check if containers are running
docker-compose -f docker-compose.prod.yml ps

# 2. Check nginx logs
docker-compose -f docker-compose.prod.yml logs nginx --tail=50

# 3. Check if web service is responding
docker-compose -f docker-compose.prod.yml exec nginx wget -qO- http://web:3000

# 4. Check API health
docker-compose -f docker-compose.prod.yml exec nginx wget -qO- http://api:8000/health

# 5. Restart services if needed
docker-compose -f docker-compose.prod.yml restart

# 6. Check for resource exhaustion
docker stats
```

**Resolution:**
- If nginx is down: `docker-compose -f docker-compose.prod.yml restart nginx`
- If web is down: `docker-compose -f docker-compose.prod.yml restart web`
- If API is down: Check database connectivity, then restart

### Issue: Database Connection Errors

**Symptoms:** API returning 500 errors, connection timeout messages

**Checklist:**

```bash
# 1. Check database is running
docker-compose -f docker-compose.prod.yml ps db

# 2. Check database logs
docker-compose -f docker-compose.prod.yml logs db --tail=50

# 3. Test connection
docker-compose -f docker-compose.prod.yml exec db pg_isready -U postgres

# 4. Check connection pool exhaustion
docker-compose -f docker-compose.prod.yml exec db psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# 5. Restart database if necessary
docker-compose -f docker-compose.prod.yml restart db
```

**Resolution:**
- If max connections reached: Restart API containers to clear connections
- If database is locked: Identify blocking queries and terminate
- If corrupted: Restore from backup

### Issue: High CPU/Memory Usage

**Symptoms:** Slow response times, monitoring alerts

**Checklist:**

```bash
# 1. Identify high usage containers
docker stats --no-stream

# 2. Check for runaway processes
docker-compose -f docker-compose.prod.yml top api

# 3. Check for memory leaks in logs
docker-compose -f docker-compose.prod.yml logs api | grep -i "memory\|killed"

# 4. Check sandbox containers (if any)
docker ps | grep sandbox
```

**Resolution:**
- Restart problematic service
- Scale workers down temporarily
- Kill orphaned sandbox containers: `docker ps -q -f name=sandbox | xargs docker rm -f`

### Issue: SSL Certificate Expired

**Symptoms:** Browser security warnings, HTTPS failures

**Checklist:**

```bash
# 1. Check certificate status
docker-compose -f docker-compose.prod.yml exec certbot certbot certificates

# 2. Check certbot logs
docker-compose -f docker-compose.prod.yml logs certbot

# 3. Test renewal
docker-compose -f docker-compose.prod.yml run --rm certbot renew --dry-run
```

**Resolution:**

```bash
# Force renewal
docker-compose -f docker-compose.prod.yml run --rm certbot renew --force-renewal

# Restart nginx to pick up new certificates
docker-compose -f docker-compose.prod.yml restart nginx
```

### Issue: Sandbox Execution Failures

**Symptoms:** Code runs but never returns, execution timeouts

**Checklist:**

```bash
# 1. Check Docker socket access
docker-compose -f docker-compose.prod.yml exec api ls -la /var/run/docker.sock

# 2. Check for stuck sandbox containers
docker ps -a | grep sandbox

# 3. Clean up old containers
docker ps -aq -f name=sandbox -f exited=0 | xargs docker rm

# 4. Check API logs for errors
docker-compose -f docker-compose.prod.yml logs api | grep -i sandbox
```

**Resolution:**

```bash
# Kill all sandbox containers
docker ps -q -f name=sandbox | xargs -r docker rm -f

# Restart API if needed
docker-compose -f docker-compose.prod.yml restart api
```

## Scaling Procedures

### Scale Web Frontend

```bash
# Scale to 3 instances
docker-compose -f docker-compose.prod.yml up -d --scale web=3

# Verify load balancing
docker-compose -f docker-compose.prod.yml ps web
```

### Scale Background Workers

```bash
# Scale workers based on queue depth
docker-compose -f docker-compose.prod.yml up -d --scale worker=5

# Monitor queue length (requires redis-cli)
docker-compose -f docker-compose.prod.yml exec redis redis-cli LLEN celery
```

### Database Read Replicas (Advanced)

If implemented, update connection string to use read replicas for GET requests.

## Incident Response

### Severity Levels

- **SEV-1**: Site completely down, data loss, security breach
  - Response time: 15 minutes
  - Update frequency: Every 30 minutes
  - Escalation: Immediate

- **SEV-2**: Major feature broken, significant performance degradation
  - Response time: 30 minutes
  - Update frequency: Every hour
  - Escalation: 2 hours

- **SEV-3**: Minor issue, workaround available
  - Response time: 2 hours
  - Update frequency: Every 4 hours
  - Escalation: Next business day

- **SEV-4**: Cosmetic issues, feature requests
  - Response time: Next business day
  - No escalation required

### Incident Response Process

1. **Detect**: Alert received or reported by user
2. **Triage**: Assign severity level
3. **Respond**: Execute appropriate runbook
4. **Communicate**: Update status page, notify stakeholders
5. **Resolve**: Confirm fix, monitor
6. **Review**: Post-incident review within 24 hours

### Communication Templates

**SEV-1 Notice:**
```
🚨 INCIDENT ALERT - SEV-1
Service: OOP Journey Platform
Impact: Complete outage
Started: [TIME UTC]
Status: Investigating
ETA: [TIME UTC]

We are investigating a complete service outage. 
Updates every 30 minutes at @channel
```

**Status Update:**
```
📊 INCIDENT UPDATE - [SEV-X]
Status: [Investigating/Identified/Monitoring/Resolved]
Update: [Brief description of progress]
Next Update: [TIME]
```

**All Clear:**
```
✅ INCIDENT RESOLVED - [SEV-X]
Duration: [X minutes]
Resolution: [Brief description]
Post-mortem: [Link or ETA]
```

## Maintenance Windows

### Scheduled Maintenance Procedure

1. **Advance Notice**: Announce 48 hours before
2. **Status Page**: Set to "Maintenance Scheduled"
3. **Backup**: Run full backup
4. **Execute**: Perform maintenance
5. **Verify**: Run smoke tests
6. **Communicate**: Update status page

### Zero-Downtime Maintenance

```bash
# 1. Put up maintenance banner (if applicable)
# Update feature flag or config

# 2. Drain connections
docker-compose -f docker-compose.prod.yml exec nginx nginx -s quit

# 3. Update service
docker-compose -f docker-compose.prod.yml up -d --no-deps --build <service>

# 4. Verify
curl https://oopjourney.com/api/health

# 5. Remove maintenance banner
```

### Database Maintenance

```bash
# 1. Schedule maintenance window
# 2. Create backup
./scripts/backup.sh

# 3. Enable maintenance mode (if needed)

# 4. Run maintenance
docker-compose -f docker-compose.prod.yml exec db psql -U postgres -d oopjourney_production -c "VACUUM ANALYZE;"

# 5. Verify and exit maintenance mode
```

## Emergency Contacts

### Team Contacts

| Role | Name | Phone | Slack |
|------|------|-------|-------|
| On-Call Engineer | Rotating | +1-XXX-XXX-XXXX | @oncall |
| Tech Lead | [Name] | +1-XXX-XXX-XXXX | @techlead |
| DevOps Lead | [Name] | +1-XXX-XXX-XXXX | @devops |
| Product Manager | [Name] | +1-XXX-XXX-XXXX | @pm |

### Vendor Contacts

| Service | Contact | URL |
|---------|---------|-----|
| Hosting Provider | [Support] | [URL] |
| Domain Registrar | [Support] | [URL] |
| Sentry | support@sentry.io | sentry.io |
| SendGrid | [Support] | sendgrid.com |

### Escalation Path

1. On-Call Engineer (0-30 min)
2. Tech Lead (30 min - 1 hour)
3. DevOps Lead (1-2 hours)
4. CTO/VP Engineering (2+ hours)

## Useful Commands Quick Reference

```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f [service]

# Shell into container
docker-compose -f docker-compose.prod.yml exec [service] sh

# Database shell
docker-compose -f docker-compose.prod.yml exec db psql -U postgres -d oopjourney_production

# Redis CLI
docker-compose -f docker-compose.prod.yml exec redis redis-cli

# Restart service
docker-compose -f docker-compose.prod.yml restart [service]

# Full restart
docker-compose -f docker-compose.prod.yml down && docker-compose -f docker-compose.prod.yml up -d

# Check resource usage
docker stats

# Clean up
docker system prune -f
docker volume prune -f
```

## Post-Incident Review Template

```markdown
# Incident Review: [INCIDENT-ID]

## Summary
- Date: [DATE]
- Duration: [X minutes]
- Severity: [SEV-X]
- Impact: [Description]

## Timeline
- [TIME]: Issue detected
- [TIME]: Response started
- [TIME]: Root cause identified
- [TIME]: Fix deployed
- [TIME]: Service restored

## Root Cause
[Description]

## Resolution
[Steps taken]

## Action Items
- [ ] [Action] - Owner - Due Date

## Lessons Learned
[What went well, what could be improved]
```

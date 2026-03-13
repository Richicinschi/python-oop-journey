# Deployment Guide

This guide covers deploying the OOP Journey platform to production.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Initial Deployment](#initial-deployment)
- [Database Migrations](#database-migrations)
- [SSL Certificates](#ssl-certificates)
- [Monitoring Setup](#monitoring-setup)
- [Updating the Application](#updating-the-application)
- [Rollback Procedures](#rollback-procedures)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Server Requirements

- **OS**: Ubuntu 22.04 LTS or similar
- **CPU**: 4+ cores
- **RAM**: 8GB+ (16GB recommended)
- **Storage**: 100GB SSD
- **Network**: Public IP, ports 80/443 open

### Software Requirements

- Docker 24.0+
- Docker Compose 2.20+
- Git
- OpenSSL (for generating secrets)

### Domain Configuration

1. Point your domain (e.g., `oopjourney.com`) to your server's IP
2. Set up `www` subdomain as CNAME or A record
3. Optional: Set up `staging` subdomain

## Environment Setup

### 1. Clone the Repository

```bash
cd /opt
git clone https://github.com/yourusername/oop-journey.git
cd oop-journey
```

### 2. Create Environment File

```bash
cp .env.production.example .env.production
nano .env.production
```

Fill in all required values:

```bash
# Generate a secure secret key
openssl rand -hex 32

# Set strong database password
openssl rand -base64 32
```

### 3. Create Required Directories

```bash
mkdir -p backups certbot/www
chmod +x scripts/*.sh
```

## Initial Deployment

### 1. Build Docker Images

```bash
docker-compose -f docker-compose.prod.yml build
```

### 2. Start Infrastructure Services

```bash
# Start database and redis first
docker-compose -f docker-compose.prod.yml up -d db redis

# Wait for database to be ready
sleep 10
```

### 3. Run Database Migrations

```bash
docker-compose -f docker-compose.prod.yml run --rm api alembic upgrade head
```

### 4. Start All Services

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 5. Verify Deployment

```bash
# Check all services are running
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Test health endpoints
curl http://localhost/api/health
curl http://localhost/nginx-health
```

## Database Migrations

### Running Migrations

```bash
# Automatic (recommended)
docker-compose -f docker-compose.prod.yml run --rm api alembic upgrade head

# Check current version
docker-compose -f docker-compose.prod.yml run --rm api alembic current

# View migration history
docker-compose -f docker-compose.prod.yml run --rm api alembic history
```

### Creating New Migrations (Development)

```bash
docker-compose -f docker-compose.prod.yml run --rm api alembic revision --autogenerate -m "description"
```

## SSL Certificates

### Automatic Setup (Let's Encrypt)

```bash
# Run the SSL setup script
./scripts/setup-ssl.sh oopjourney.com

# Or for staging
./scripts/setup-ssl.sh staging.oopjourney.com staging
```

### Manual Certificate Installation

If you have your own certificates:

```bash
# Copy certificates to nginx ssl directory
mkdir -p nginx/ssl
cp your-cert.pem nginx/ssl/
cp your-key.pem nginx/ssl/

# Update nginx.conf to use your certificates
# Restart nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### Certificate Renewal

Certificates auto-renew via the certbot container. To manually test:

```bash
docker-compose -f docker-compose.prod.yml run --rm certbot renew --dry-run
```

## Monitoring Setup

### Enable Monitoring Stack

```bash
# Start with monitoring profile
docker-compose -f docker-compose.prod.yml --profile monitoring up -d

# Access Grafana at http://your-server:3001
# Default login: admin / (password from .env.production)
```

### Configure Alerts

1. Log into Grafana (`http://your-server:3001`)
2. Go to Alerting → Notification channels
3. Add your preferred channel (Email, Slack, PagerDuty)
4. Create alert rules for:
   - High CPU/memory usage
   - Database connection errors
   - API error rates
   - SSL certificate expiry

## Updating the Application

### Automated Deployment (CI/CD)

The project includes GitHub Actions workflows for automated deployment:

1. Push to `main` branch triggers production deployment
2. Push to `develop` branch triggers staging deployment
3. Manual deployment via GitHub Actions "Run workflow"

### Manual Deployment

```bash
# Pull latest code
git fetch origin
git checkout <version-tag>

# Create backup
./scripts/backup.sh

# Pull latest images
docker-compose -f docker-compose.prod.yml pull

# Run migrations
docker-compose -f docker-compose.prod.yml run --rm api alembic upgrade head

# Restart services
docker-compose -f docker-compose.prod.yml up -d

# Verify deployment
./scripts/smoke-test.sh
```

### Zero-Downtime Deployment

The docker-compose configuration supports rolling updates:

```bash
# Scale up new instances
docker-compose -f docker-compose.prod.yml up -d --scale web=2 --no-recreate

# Wait for health checks
sleep 10

# Scale down old instances
docker-compose -f docker-compose.prod.yml up -d --scale web=1
```

## Rollback Procedures

### Database Rollback

```bash
# Restore from backup
./scripts/restore.sh backups/oopjourney_backup_YYYYMMDD_HHMMSS.sql.gz

# Or rollback migration
docker-compose -f docker-compose.prod.yml run --rm api alembic downgrade -1
```

### Application Rollback

```bash
# Checkout previous version
git checkout <previous-tag>

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Run smoke tests
./scripts/smoke-test.sh
```

### Emergency Procedures

```bash
# Stop all services immediately
docker-compose -f docker-compose.prod.yml down

# Restart with debug logging
docker-compose -f docker-compose.prod.yml -f docker-compose.debug.yml up

# Access database directly
docker-compose -f docker-compose.prod.yml exec db psql -U postgres -d oopjourney_production
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs <service-name>

# Common issues:
# 1. Port conflicts - check nothing else is using 80/443/8000/3000
# 2. Missing environment variables - verify .env.production
# 3. Database connection - ensure DB is healthy first
```

### Database Connection Issues

```bash
# Check database is running
docker-compose -f docker-compose.prod.yml ps db

# Check database logs
docker-compose -f docker-compose.prod.yml logs db

# Verify connection string in .env.production
# Test connection manually
docker-compose -f docker-compose.prod.yml exec db pg_isready -U postgres
```

### SSL Certificate Issues

```bash
# Check certificate status
docker-compose -f docker-compose.prod.yml exec certbot certbot certificates

# Renew manually
docker-compose -f docker-compose.prod.yml run --rm certbot renew

# Check nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

### High Memory Usage

```bash
# Check container stats
docker stats

# Restart services
docker-compose -f docker-compose.prod.yml restart

# Scale down workers temporarily
docker-compose -f docker-compose.prod.yml up -d --scale worker=1
```

### Logs and Debugging

```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs -f

# View specific service
docker-compose -f docker-compose.prod.yml logs -f api

# View last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 api
```

## Security Checklist

- [ ] Change default passwords
- [ ] Enable firewall (UFW/iptables)
- [ ] Configure fail2ban
- [ ] Set up automated security updates
- [ ] Enable Cloudflare or similar WAF (optional)
- [ ] Configure log rotation
- [ ] Set up log aggregation
- [ ] Enable Sentry for error tracking
- [ ] Rotate secrets regularly
- [ ] Disable root SSH login
- [ ] Use SSH key authentication only

## Support

For deployment issues:

1. Check logs: `docker-compose -f docker-compose.prod.yml logs`
2. Run smoke tests: `./scripts/smoke-test.sh`
3. Review monitoring dashboards
4. Contact: devops@oopjourney.com

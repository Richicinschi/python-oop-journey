# Production Setup - OOP Journey

This directory contains the complete production deployment configuration for the OOP Journey platform.

## 📁 Directory Structure

```
website-playground/
├── docker-compose.prod.yml      # Production Docker Compose
├── docker-compose.staging.yml   # Staging Docker Compose
├── .env.production.example      # Production environment template
├── nginx/
│   ├── nginx.conf              # Production nginx config
│   └── nginx.staging.conf      # Staging nginx config
├── scripts/
│   ├── deploy.sh               # Deployment script
│   ├── backup.sh               # Database backup script
│   ├── restore.sh              # Database restore script
│   ├── setup-ssl.sh            # SSL certificate setup
│   └── smoke-test.sh           # Health check script
├── .github/workflows/
│   ├── ci.yml                  # CI pipeline
│   └── deploy.yml              # CD pipeline
├── monitoring/
│   ├── loki-config.yml         # Log aggregation config
│   ├── prometheus.yml          # Metrics config
│   └── grafana/                # Dashboard configs
├── terraform/
│   ├── main.tf                 # AWS infrastructure
│   ├── variables.tf            # Terraform variables
│   └── outputs.tf              # Terraform outputs
├── tests/smoke/
│   ├── health-check.test.ts    # Health check tests
│   ├── critical-path.test.ts   # Critical flow tests
│   ├── auth-flow.test.ts       # Auth flow tests
│   └── problem-solving.test.ts # Problem solving tests
└── docs/
    ├── DEPLOYMENT.md           # Deployment guide
    ├── RUNBOOK.md              # Operations runbook
    └── SECURITY.md             # Security checklist
```

## 🚀 Quick Start

### Prerequisites

- Docker 24.0+
- Docker Compose 2.20+
- Git
- A server with public IP
- Domain name (for SSL)

### Initial Deployment

```bash
# 1. Clone and enter directory
cd website-playground

# 2. Set up environment
cp .env.production.example .env.production
# Edit .env.production with your values

# 3. Deploy
./scripts/deploy.sh production
```

### SSL Certificate Setup

```bash
./scripts/setup-ssl.sh oopjourney.com
```

## 🔧 Configuration

### Environment Variables

Key variables in `.env.production`:

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | JWT signing key | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `REDIS_URL` | Redis connection string | Yes |
| `SENTRY_DSN` | Error tracking (optional) | No |
| `SENDGRID_API_KEY` | Email service (optional) | No |

### Services

| Service | Port | Description |
|---------|------|-------------|
| web | 3000 | Next.js frontend |
| api | 8000 | FastAPI backend |
| db | 5432 | PostgreSQL database |
| redis | 6379 | Redis cache |
| nginx | 80/443 | Reverse proxy |
| worker | - | Background task worker |
| scheduler | - | Celery beat scheduler |

## 📊 Monitoring

### Enable Monitoring Stack

```bash
docker-compose -f docker-compose.prod.yml --profile monitoring up -d
```

### Access Dashboards

- Grafana: `http://your-server:3001`
- Prometheus: `http://your-server:9090`

### Health Endpoints

- `GET /health` - Basic health check
- `GET /ready` - Readiness probe
- `GET /nginx-health` - Nginx health check

## 🔒 Security

See [docs/SECURITY.md](./docs/SECURITY.md) for the complete security checklist.

Key features:
- HTTPS only with auto-renewal
- Security headers (HSTS, CSP, etc.)
- Rate limiting
- Non-root containers
- Secrets management

## 🔄 CI/CD

GitHub Actions workflows:

- `ci.yml` - Run on PR/push (lint, test, build)
- `deploy.yml` - Deploy to staging/production

## 📚 Documentation

- [DEPLOYMENT.md](./docs/DEPLOYMENT.md) - Detailed deployment guide
- [RUNBOOK.md](./docs/RUNBOOK.md) - Operations and incident response
- [SECURITY.md](./docs/SECURITY.md) - Security checklist and practices

## 🆘 Support

For issues or questions:
1. Check [RUNBOOK.md](./docs/RUNBOOK.md) troubleshooting section
2. Review logs: `docker-compose -f docker-compose.prod.yml logs`
3. Run smoke tests: `./scripts/smoke-test.sh`

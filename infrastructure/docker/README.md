# Docker Infrastructure

Production-ready Docker setup for the OOP Journey website platform.

## Quick Start

```bash
# Start development environment
make dev

# View logs
make logs

# Run tests
make test

# Stop everything
make dev-stop
```

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│      Web        │────▶│      API        │────▶│   PostgreSQL    │
│   (Next.js)     │     │   (FastAPI)     │     │    (Database)   │
│    Port 3000    │     │    Port 8000    │     │    Port 5432    │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │     Sandbox     │
                        │  (Code Runner)  │
                        │   Isolated      │
                        └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │     Redis       │
                        │  (Cache/Queue)  │
                        │    Port 6379    │
                        └─────────────────┘
```

## Services

### Web (Next.js)
- **Port**: 3000
- **Dockerfile**: `web.Dockerfile`
- **Features**: Multi-stage build, hot reload in dev, standalone output in prod

### API (FastAPI)
- **Port**: 8000
- **Dockerfile**: `api.Dockerfile`
- **Features**: Python 3.11, async support, auto-reload in dev, 4 workers in prod

### PostgreSQL
- **Port**: 5432
- **Image**: postgres:16-alpine
- **Features**: Persistent volume, health checks, initialized extensions

### Redis
- **Port**: 6379
- **Image**: redis:7-alpine
- **Features**: AOF persistence, memory limits, LRU eviction

### Sandbox
- **Purpose**: Secure Python code execution
- **Features**: No network, readonly filesystem, dropped capabilities, resource limits

## Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Development configuration |
| `docker-compose.prod.yml` | Production configuration |
| `web.Dockerfile` | Next.js multi-stage build |
| `api.Dockerfile` | FastAPI multi-stage build |
| `sandbox.Dockerfile` | Secure code execution |
| `redis.conf` | Redis configuration |
| `init-db/` | Database initialization scripts |
| `scripts/` | Helper scripts |

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make dev` | Start development stack |
| `make dev-stop` | Stop development stack |
| `make build` | Build all images |
| `make test` | Run all tests |
| `make migrate` | Run database migrations |
| `make db-reset` | Reset database (DESTRUCTIVE!) |
| `make logs` | View logs |
| `make clean` | Clean up containers and volumes |
| `make shell-web` | Open shell in web container |
| `make shell-api` | Open shell in API container |
| `make prod-build` | Build production images |

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Core
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-secret-key

# URLs
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/oopjourney

# Redis
REDIS_URL=redis://redis:6379

# Sandbox
SANDBOX_TIMEOUT_SECONDS=30
SANDBOX_MEMORY_LIMIT_MB=256
```

## Security

### Sandbox Security
- No network access (`network_mode: none`)
- Read-only filesystem (`read_only: true`)
- Dropped capabilities (`cap_drop: ALL`)
- Resource limits (256MB RAM, 0.5 CPU)
- Process limits (50 PIDs max)
- Non-root user execution

### Production Security
- No volume mounts (immutable containers)
- Automatic restart policies
- Resource limits enforced
- External networks for reverse proxy
- Secrets via environment files (not committed)

## Health Checks

All services include health checks:
- **Web**: HTTP check on `/api/health`
- **API**: HTTP check on `/health`
- **Database**: `pg_isready` command
- **Redis**: `redis-cli ping` command

## Log Rotation

Development: Local driver with 10MB limit per file
Production: JSON driver with 100MB limit, labeled for aggregation

## Development vs Production

| Feature | Development | Production |
|---------|-------------|------------|
| Volume mounts | Yes (hot reload) | No (immutable) |
| Auto-reload | Yes | No |
| Workers | 1 | 4 |
| Replicas | 1 | 2+ |
| Debug mode | On | Off |
| Log level | Debug | Info |
| Resource limits | Relaxed | Strict |

## Troubleshooting

### Services won't start
```bash
make clean
make dev
```

### Database issues
```bash
make db-reset
```

### Check logs
```bash
make logs SERVICE=api
```

### Rebuild images
```bash
make build-no-cache
```

## License

Same as main project.

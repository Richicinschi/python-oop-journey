# Quick Start Guide - Python OOP Journey Website

Complete guide to running the website playground locally or in production.

---

## Prerequisites

### Required Software
- **Node.js** v18+ with npm
- **Python** 3.11+
- **Docker** & Docker Compose
- **Git**

### Optional (for AI features)
- **OpenAI API Key** (for AI hints)
- **SendGrid API Key** (for email - or use console backend for dev)

---

## 1. Clone & Setup

```bash
# Clone the repository
git clone <repository-url>
cd website-playground

# Install Node.js dependencies
npm install

# Install Python dependencies
cd apps/api
pip install -r requirements.txt
cd ../..

# Copy environment files
cp apps/api/.env.example apps/api/.env
cp .env.production.example .env

# Edit .env files with your configuration
```

---

## 2. Environment Configuration

### Backend (.env)
```bash
# apps/api/.env
SECRET_KEY=your-super-secret-key-min-32-characters
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/oopjourney
REDIS_URL=redis://localhost:6379/0

# For magic link emails (optional for dev)
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
FROM_EMAIL=noreply@oopjourney.local

# For AI features (optional)
OPENAI_API_KEY=sk-...
AI_HINT_MODEL=gpt-4o-mini
```

### Frontend (.env.local)
```bash
# apps/web/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## 3. Database Setup

### Start PostgreSQL & Redis (Docker)
```bash
# Start infrastructure services
docker-compose up -d postgres redis

# Wait for services to be ready
sleep 5
```

### Run Migrations
```bash
cd apps/api

# Create database tables
alembic upgrade head

# Verify (optional)
alembic current
```

### (Optional) Seed Test Data
```bash
# Seed with sample users/progress (if you have a seed script)
python scripts/seed_data.py
```

---

## 4. Build Docker Sandbox

The code execution sandbox needs to be built:

```bash
# Build the Python sandbox image
docker build -f apps/api/sandbox.Dockerfile -t oop-journey-sandbox:latest .

# Verify it built
docker images | grep oop-journey-sandbox
```

---

## 5. Start Development Servers

You'll need **3 terminal windows/tabs**:

### Terminal 1: Backend API
```bash
cd apps/api

# Option A: Standard
uvicorn api.main:app --reload --port 8000

# Option B: With hot reload for all files
uvicorn api.main:app --reload --reload-dir . --port 8000
```

### Terminal 2: Celery Worker (for async tasks)
```bash
cd apps/api

celery -A api.celery_app worker --loglevel=info

# For production (more workers)
# celery -A api.celery_app worker --loglevel=info --concurrency=4
```

### Terminal 3: Frontend Web
```bash
cd apps/web

# Development server
npm run dev

# Or with Turbopack (faster)
# npm run dev --turbo
```

---

## 6. Access the Application

Once all services are running:

| Service | URL | Description |
|---------|-----|-------------|
| Web App | http://localhost:3000 | Main application |
| API Docs | http://localhost:8000/docs | Swagger UI |
| API | http://localhost:8000 | FastAPI endpoints |
| Redis | localhost:6379 | Cache/Queue |
| Postgres | localhost:5432 | Database |

---

## 7. First Time Setup

### Create Admin User (Optional)
```bash
cd apps/api
python scripts/create_admin.py --email admin@example.com
```

### Test the Flow
1. Visit http://localhost:3000
2. Click "Start Learning" or "Login"
3. Enter your email → Check console for magic link (or email if SMTP configured)
4. Click the magic link → You're logged in!
5. Navigate to a problem and try solving it

---

## 8. Common Development Commands

### Frontend
```bash
cd apps/web

# Type check
npx tsc --noEmit

# Lint
npm run lint

# Build for production
npm run build

# Start production build
npm start
```

### Backend
```bash
cd apps/api

# Run tests
pytest

# Run with coverage
pytest --cov=api --cov-report=html

# Format code
black api/
ruff check api/

# Database - create new migration
alembic revision --autogenerate -m "Description"

# Database - rollback one migration
alembic downgrade -1
```

### Docker
```bash
# Start all infrastructure
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all
docker-compose down

# Reset everything (WARNING: deletes data!)
docker-compose down -v
```

---

## 9. Production Deployment

### Quick Deploy (Docker Compose)
```bash
# 1. Setup production environment
cp .env.production.example .env
# Edit .env with production values

# 2. Deploy
./scripts/deploy.sh production

# 3. Verify
./scripts/smoke-test.sh https://your-domain.com
```

### AWS Deployment (Terraform)
```bash
cd terraform

# Initialize
terraform init

# Plan
terraform plan

# Apply
terraform apply

# Get outputs
terraform output
```

### Manual Steps After Deploy
```bash
# Run migrations on production DB
cd apps/api
DATABASE_URL=your-prod-db-url alembic upgrade head

# Build sandbox on production server
docker build -f sandbox.Dockerfile -t oop-journey-sandbox:latest .

# Create first admin
python scripts/create_admin.py --email your-email@example.com
```

---

## 10. Troubleshooting

### Common Issues

**Port already in use**
```bash
# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

**Database connection failed**
```bash
# Check if PostgreSQL is running
docker-compose ps

# Check logs
docker-compose logs postgres

# Reset database (WARNING: deletes all data!)
docker-compose down -v
docker-compose up -d postgres
```

**Module not found errors**
```bash
# Reinstall dependencies
cd apps/api && pip install -r requirements.txt
cd apps/web && npm install
```

**CORS errors in browser**
- Check `NEXT_PUBLIC_API_URL` matches your API URL
- Verify API is running on correct port

**Docker sandbox not working**
```bash
# Check Docker is running
docker ps

# Rebuild sandbox
docker build -f apps/api/sandbox.Dockerfile -t oop-journey-sandbox:latest .
```

---

## 11. Project Structure Overview

```
website-playground/
├── apps/
│   ├── web/              # Next.js 14 frontend
│   │   ├── app/          # App router pages
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom React hooks
│   │   └── lib/          # Utilities
│   │
│   └── api/              # FastAPI backend
│       ├── api/
│       │   ├── models/   # SQLAlchemy models
│       │   ├── routers/  # API endpoints
│       │   ├── services/ # Business logic
│       │   └── middleware/
│       └── migrations/   # Alembic migrations
│
├── docker-compose.yml    # Development services
├── docker-compose.prod.yml # Production stack
└── scripts/              # Deployment scripts
```

---

## 12. Key URLs (Development)

| URL | Purpose |
|-----|---------|
| http://localhost:3000 | Main app |
| http://localhost:3000/weeks | Browse weeks |
| http://localhost:3000/search | Search problems |
| http://localhost:3000/problems | Problem listing |
| http://localhost:3000/auth/login | Login |
| http://localhost:8000/docs | API documentation |
| http://localhost:8000/api/v1/health | Health check |

---

## Next Steps

1. **Configure email** (SendGrid/SMTP) for production magic links
2. **Add AI keys** (OpenAI) for hints feature
3. **Set up Sentry** for error tracking
4. **Configure monitoring** (Grafana/Prometheus)
5. **Set up backups** (automated S3 backups)

---

## Support

- Documentation: `/docs` folder
- API Docs: http://localhost:8000/docs (when running)
- Issues: Check `RUNBOOK.md` for common problems

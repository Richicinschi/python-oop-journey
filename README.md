# Python OOP Journey - Website Playground

> Interactive web platform for learning Python OOP with hands-on coding exercises, AI-powered hints, and progress tracking.

[![Node Version](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What This Is

The **Python OOP Journey Website** is a full-stack learning platform that transforms the static curriculum into an interactive coding experience. Learners write real Python code in the browser, get instant feedback, track their progress, and receive AI-powered hints when stuck.

### Why It Exists

Learning Python OOP shouldn't require complex local setup. This platform provides:
- **Zero-setup coding environment** - Write and run Python directly in the browser
- **Safe code execution** - Isolated Docker sandboxes for secure code running
- **Progress persistence** - Track learning across sessions
- **AI assistance** - Smart hints when learners get stuck
- **Gamification** - Streaks, achievements, and visual progress

---

## Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| **Next.js 14** | React framework with App Router |
| **TypeScript** | Type-safe development |
| **Tailwind CSS** | Utility-first styling |
| **shadcn/ui** | Modern UI components |
| **Monaco Editor** | VS Code-like code editor |
| **TanStack Query** | Server state management |
| **Sentry** | Error tracking & monitoring |

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Async Python API framework |
| **SQLAlchemy 2.0** | Async ORM with PostgreSQL |
| **Alembic** | Database migrations |
| **Redis** | Caching & task queue |
| **Celery** | Background task workers |
| **Piston** | Code execution engine |
| **OpenAI API** | AI-powered hints |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Local & production orchestration |
| **Nginx** | Reverse proxy & SSL |
| **Let's Encrypt** | Free SSL certificates |
| **Grafana** | Metrics & monitoring |
| **Prometheus** | Metrics collection |
| **Terraform** | AWS infrastructure (optional) |

---

## Features

### 🔐 Authentication & User Management
- **Magic Link (Passwordless)** - Secure email-based login
- **Google OAuth** - One-click social login
- **Guest Mode** - Try without signing up (localStorage-based)
- **Persistent Sessions** - JWT with refresh tokens

### 🎓 Learning Experience
- **Interactive Code Editor** - Monaco Editor with Python syntax highlighting
- **Safe Code Execution** - Docker-isolated Python sandbox
- **Instant Feedback** - Real-time test results and output
- **Progress Tracking** - Problem completion, streaks, time spent
- **Bookmarks** - Save problems for later review
- **Recently Visited** - Quick access to recent content

### 🔍 Search & Discovery
- **Command Palette** (⌘K) - Fast fuzzy search across all content
- **Problem Discovery** - Browse 450+ problems with filters
- **Topic Navigation** - Browse by concept (classes, inheritance, etc.)
- **Week/Day Structure** - Organized curriculum navigation

### 🤖 AI-Powered Features
- **Smart Hints** - Context-aware guidance (OpenAI GPT-4o-mini)
- **Code Explanation** - "Why does this work?" explanations
- **Error Analysis** - Helpful error interpretation

### 📊 Dashboard & Analytics
- **Learning Stats** - Problems solved, time spent, streaks
- **Activity Graph** - GitHub-style contribution graph
- **Weekly Progress** - Visual progress through curriculum
- **Continue Learning** - Resume where you left off

### 🏗️ Projects (Multi-file)
- **Project Mode** - Multi-file code editor for larger assignments
- **File Tree** - Hierarchical file explorer
- **Project Submission** - Submit complete projects for validation

### ⌨️ Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `⌘K` | Open search |
| `?` | Show shortcuts help |
| `Ctrl+Enter` | Run code |
| `Ctrl+S` | Save draft |
| `Ctrl+T` | Run tests |

---

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Git

### 1. Clone & Setup

```bash
git clone <repository-url>
cd website-playground

# Install dependencies
npm install
cd apps/api && pip install -r requirements.txt && cd ../..

# Copy environment files
cp .env.example .env
cp apps/api/.env.example apps/api/.env
```

### 2. Configure Environment

Edit `.env` and `apps/api/.env` with your settings:

```bash
# Required: Generate secret keys
openssl rand -hex 32
```

### 3. Start Infrastructure

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Run database migrations
cd apps/api && alembic upgrade head && cd ../..

# Build code execution sandbox
docker build -f apps/api/sandbox.Dockerfile -t oop-journey-sandbox:latest .
```

### 4. Start Development Servers

```bash
# Terminal 1: Backend API
cd apps/api && uvicorn api.main:app --reload --port 8000

# Terminal 2: Celery Worker
cd apps/api && celery -A api.celery_app worker --loglevel=info

# Terminal 3: Frontend
cd apps/web && npm run dev
```

### 5. Access the Application

| Service | URL |
|---------|-----|
| Web App | http://localhost:3000 |
| API Docs | http://localhost:8000/docs |
| API | http://localhost:8000 |

---

## Project Structure

```
website-playground/
├── apps/
│   ├── web/                    # Next.js 14 frontend
│   │   ├── app/                # App router pages
│   │   ├── components/         # React components
│   │   │   ├── projects/       # Project mode components
│   │   │   ├── search/         # Search components
│   │   │   └── ui/             # shadcn/ui components
│   │   ├── hooks/              # Custom React hooks
│   │   ├── lib/                # Utilities
│   │   └── types/              # TypeScript types
│   │
│   └── api/                    # FastAPI backend
│       ├── api/
│       │   ├── models/         # SQLAlchemy models
│       │   ├── routers/        # API endpoints
│       │   ├── services/       # Business logic
│       │   └── middleware/     # Auth, CORS, etc.
│       ├── migrations/         # Alembic migrations
│       └── tests/              # Test suite
│
├── docs/                       # Documentation
├── scripts/                    # Deployment scripts
├── nginx/                      # Nginx configuration
├── terraform/                  # AWS infrastructure
├── docker-compose.yml          # Development stack
├── docker-compose.prod.yml     # Production stack
└── render.yaml                 # Render.com deployment
```

---

## API Overview

### Health Endpoints
- `GET /health` - Basic health check
- `GET /api/v1/health` - Detailed health status
- `GET /ready` - Readiness probe

### Curriculum
- `GET /api/v1/curriculum` - Full curriculum
- `GET /api/v1/curriculum/weeks/{slug}` - Week details
- `GET /api/v1/curriculum/problems` - List problems
- `GET /api/v1/curriculum/problems/{slug}` - Problem details

### Code Execution
- `POST /api/v1/execute` - Execute Python code
- `POST /api/v1/execute/validate` - Validate syntax

### Authentication
- `POST /api/v1/auth/magic-link` - Request magic link
- `POST /api/v1/auth/verify` - Verify token
- `POST /api/v1/auth/google` - Google OAuth

### User (Authenticated)
- `GET /api/v1/users/me` - Profile
- `GET /api/v1/users/me/stats` - Statistics
- `GET /api/v1/users/me/progress` - Progress tracking
- `POST /api/v1/users/me/drafts` - Save code drafts

See [API Documentation](http://localhost:8000/docs) when running locally.

---

## Deployment

### Quick Deploy (Docker Compose)

```bash
# 1. Set up production environment
cp .env.production.example .env.production
# Edit with production values

# 2. Deploy
./scripts/deploy.sh production

# 3. Verify
./scripts/smoke-test.sh
```

### Cloud Platforms

- **Render** - See `render.yaml` (blueprint deployment)
- **AWS** - Terraform configuration in `terraform/`
- **Manual** - Docker Compose on any VPS

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

---

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing key | `openssl rand -hex 32` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://...` |
| `NEXT_PUBLIC_API_URL` | API URL (frontend) | `http://localhost:8000` |

### Optional

| Variable | Description | For Feature |
|----------|-------------|-------------|
| `OPENAI_API_KEY` | OpenAI API access | AI hints |
| `SENDGRID_API_KEY` | Email delivery | Magic links |
| `SENTRY_DSN` | Error tracking | Monitoring |
| `GOOGLE_CLIENT_ID` | Google OAuth | Social login |
| `REDIS_URL` | Cache/Queue | Background tasks |

See `.env.example` for complete list.

---

## Development Commands

### Frontend
```bash
cd apps/web
npm run dev          # Development server
npm run build        # Production build
npm run lint         # ESLint
npm run type-check   # TypeScript check
npm run test:e2e     # Playwright tests
```

### Backend
```bash
cd apps/api
uvicorn api.main:app --reload    # Dev server
pytest                            # Run tests
alembic upgrade head              # Run migrations
black api/                        # Format code
ruff check api/                   # Lint code
```

### Docker
```bash
docker-compose up -d              # Start services
docker-compose logs -f            # View logs
docker-compose down -v            # Stop & remove volumes
```

---

## Troubleshooting

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues.

Quick fixes:

```bash
# Port already in use
lsof -ti:3000 | xargs kill -9

# Database issues
docker-compose restart postgres

# Reset everything (WARNING: loses data)
docker-compose down -v
docker-compose up -d postgres
```

---

## Documentation

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](./QUICKSTART.md) | Complete setup guide |
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Production deployment |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Common issues |
| [docs/RUNBOOK.md](./docs/RUNBOOK.md) | Operations guide |
| [docs/SECURITY.md](./docs/SECURITY.md) | Security checklist |
| [PRODUCTION.md](./PRODUCTION.md) | Production setup overview |

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest` (backend) / `npm run test:e2e` (frontend)
5. Submit a pull request

---

## License

MIT © Python OOP Journey Team

---

## Support

- **Issues**: Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- **Documentation**: See `docs/` folder
- **API Docs**: http://localhost:8000/docs (when running)

# Documentation Hub

Welcome to the Python OOP Journey documentation!

## Quick Navigation

| Category | Folder | Contents |
|----------|--------|----------|
| **Hosting** | `hosting/` | Render, Cloudflare Pages |
| **Database** | `database/` | CockroachDB |
| **Cache** | `cache/` | Upstash Redis |
| **Auth** | `auth/` | Google OAuth |
| **Frontend** | `frontend/` | Next.js, Tailwind CSS |
| **Backend** | `backend/` | FastAPI |
| **ORM** | `orm/` | SQLAlchemy |
| **Migration** | `migration/` | Alembic |
| **Deployment** | `deployment/` | Deployment guides, troubleshooting |

## Technology Stack

### Infrastructure
- **Hosting:** Render (backend), Cloudflare Pages (frontend)
- **Database:** CockroachDB (PostgreSQL-compatible)
- **Cache:** Upstash Redis
- **Auth:** Google OAuth 2.0

### Backend
- **Framework:** FastAPI (Python)
- **ORM:** SQLAlchemy 2.0 (async)
- **Migrations:** Alembic
- **Task Queue:** Celery + Redis

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Editor:** Monaco Editor

## Common Tasks

### Deploy Backend
```bash
git add .
git commit -m "Your changes"
git push
# Render auto-deploys
```

### Run Migrations
```bash
cd apps/api
alembic upgrade head
```

### Check Logs
Render Dashboard → Service → Logs tab

### Add Environment Variable
Render Dashboard → Service → Environment → Add Variable

## Troubleshooting

See `deployment/TROUBLESHOOTING_CHECKLIST.md` for step-by-step debugging.

## External Documentation

- [Render Docs](https://render.com/docs)
- [CockroachDB Docs](https://www.cockroachlabs.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Next.js Docs](https://nextjs.org/docs)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org)

## Contributing to Docs

When you learn something new:
1. Add it to the relevant folder
2. Update this README if needed
3. Commit and push

# Python OOP Journey API

FastAPI backend for the Python OOP Journey interactive coding curriculum.

## Features

- **Async FastAPI** - Modern, fast async Python web framework
- **PostgreSQL** - SQLAlchemy 2.0 async ORM with Alembic migrations
- **Authentication** - Magic link (passwordless) authentication with JWT
- **Code Execution** - Safe Python code execution environment
- **Curriculum API** - Structured curriculum data with weeks, days, and problems

## Quick Start

### 1. Setup Environment

```bash
cd apps/api
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure

Copy `.env.example` to `.env` and adjust:

```bash
cp .env.example .env
```

### 3. Run Development Server

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

- Health check: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`

## Project Structure

```
api/
├── main.py              # FastAPI app entry with factory pattern
├── config.py            # Pydantic settings
├── database.py          # SQLAlchemy async setup
├── models/              # Database models
│   ├── user.py          # User model
│   ├── progress.py      # Progress tracking
│   └── draft.py         # Code drafts
├── routers/             # API endpoints
│   ├── curriculum.py    # Curriculum endpoints
│   ├── execute.py       # Code execution
│   ├── auth.py          # Authentication
│   └── user.py          # User/progress
├── schemas/             # Pydantic models
│   ├── curriculum.py
│   ├── execution.py
│   └── user.py
├── services/            # Business logic
│   ├── curriculum.py
│   ├── execution.py
│   └── auth.py
└── tests/               # Test suite
```

## API Endpoints

### Health
- `GET /health` - Health check

### Curriculum
- `GET /api/v1/curriculum` - Full curriculum
- `GET /api/v1/curriculum/weeks/{slug}` - Single week
- `GET /api/v1/curriculum/problems` - List all problems
- `GET /api/v1/curriculum/problems/{slug}` - Single problem

### Code Execution
- `POST /api/v1/execute` - Execute Python code
- `POST /api/v1/execute/validate` - Validate syntax only

### Authentication
- `POST /api/v1/auth/magic-link` - Request magic link
- `POST /api/v1/auth/verify` - Verify token and login
- `POST /api/v1/auth/refresh` - Refresh access token

### User (Authenticated)
- `GET /api/v1/users/me` - Current user profile
- `GET /api/v1/users/me/stats` - Learning statistics
- `GET /api/v1/users/me/progress` - All progress
- `POST /api/v1/users/me/progress` - Update progress
- `GET /api/v1/users/me/drafts` - All drafts
- `GET /api/v1/users/me/drafts/{problem_slug}` - Single draft
- `POST /api/v1/users/me/drafts` - Save draft

## Database

### Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head

# Downgrade
alembic downgrade -1
```

### Models

- **User** - `id`, `email`, `created_at`, `last_seen`
- **Progress** - `user_id`, `problem_slug`, `status`, `attempts`
- **Draft** - `user_id`, `problem_slug`, `code`, `saved_at`

## Development

### Running Tests

```bash
pytest
```

### Code Style

```bash
# Format
black api/

# Lint
ruff api/

# Type check
mypy api/
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Python OOP Journey API |
| `DEBUG` | Debug mode | false |
| `ENVIRONMENT` | dev/staging/prod | development |
| `SECRET_KEY` | JWT secret | required |
| `DATABASE_URL` | Database connection | sqlite+aiosqlite |
| `REDIS_URL` | Redis connection | redis://localhost:6379/0 |
| `ALLOWED_ORIGINS` | CORS origins | http://localhost:3000 |

## Docker

The API is designed to run in Docker with PostgreSQL and Redis:

```bash
docker-compose up api
```

## License

MIT

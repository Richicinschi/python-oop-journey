# TOOLS.md

## Environment Notes

Local development environment configuration and available tools.

## System Information

- **OS:** Windows (local development)
- **Shell:** PowerShell / Git Bash
- **Working Directory:** `c:\Users\digitalnomad\Documents\oopkimi`
- **Website Directory:** `c:\Users\digitalnomad\Documents\oopkimi\website-playground`

## Installed Tools

### Node.js
- **Path:** `/nodejs/node.exe` (local)
- **Version:** v20.11.0
- **npm:** 10.2.4
- **Usage:** `& /nodejs/node.exe --version`

### Python
- **Version:** 3.11+
- **pip:** Latest
- **Virtual env:** `apps/api/venv` (if created)

### Git
- Standard git commands available
- Repository: `python-oop-journey`

### Docker
- Docker Desktop (if installed)
- docker-compose available

## Project Structure

```
oopkimi/
├── website-playground/          # Main web application
│   ├── apps/
│   │   ├── web/                 # Next.js 14 frontend
│   │   │   ├── app/             # App router pages
│   │   │   ├── components/      # React components
│   │   │   ├── lib/             # Utilities
│   │   │   └── package.json
│   │   └── api/                 # FastAPI backend
│   │       ├── api/             # API routes
│   │       ├── data/            # curriculum.json
│   │       ├── requirements.txt
│   │       └── Dockerfile
│   ├── _archive/                # Organized old files
│   ├── docker-compose.yml
│   └── render.yaml
├── python-oop-journey-v2/       # Curriculum repository
│   ├── week_00_getting_started/
│   ├── week_01_python_fundamentals/
│   └── ... (9 weeks total)
└── .claw/                       # Claw configuration
    ├── soul.yaml
    ├── instructions.md
    ├── test-plan.yaml
    ├── shell-commands.yaml
    └── status.yaml
```

## Available Commands

### Build Commands
```bash
# TypeScript check
cd website-playground/apps/web && npx tsc --noEmit

# Next.js build
cd website-playground && npm run build

# Python compile check
cd website-playground/apps/api && python -m py_compile api/main.py
```

### Test Commands
```bash
# API health
curl -s http://localhost:8000/health

# Curriculum health
curl -s http://localhost:8000/health/curriculum/service

# Test week endpoint
curl -s http://localhost:8000/api/v1/curriculum/weeks/week00_getting_started

# Test problem endpoint
curl -s http://localhost:8000/api/v1/curriculum/problems/problem_01_assign_and_print
```

### Development Commands
```bash
# Start backend
cd website-playground/apps/api && python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend
cd website-playground/apps/web && npm run dev

# Docker compose
cd website-playground && docker-compose up --build
```

## External Services

### Production (Render)
- **Frontend:** https://oop-journey.onrender.com
- **API:** https://oop-journey-api.onrender.com
- **Health:** https://oop-journey-api.onrender.com/health

### Database (CockroachDB)
- **Type:** Serverless PostgreSQL
- **Connection:** Via `DATABASE_URL` env var
- **Status:** Check via API health endpoint

### Cache (Redis)
- **Provider:** Render
- **Connection:** Via `REDIS_URL` env var
- **Status:** Check via API health endpoint

## File Locations

### Critical Files
- **Curriculum:** `website-playground/apps/api/data/curriculum.json`
- **Backend Main:** `website-playground/apps/api/api/main.py`
- **Frontend Config:** `website-playground/apps/web/next.config.js`
- **Environment:** `website-playground/apps/api/.env.local`

### Configuration Files
- **AGENTS.md** - How I work
- **IDENTITY.md** - Who I am
- **SOUL.md** - My personality
- **USER.md** - User preferences
- **MEMORY.md** - Long-term memory
- **HEARTBEAT.md** - Periodic tasks

## SSH Hosts

None configured for this project. All work is local or via GitHub.

## Cameras / Hardware

None relevant for this project. Pure software development.

## Notes

- Use PowerShell syntax on Windows: `& /nodejs/node.exe`
- Git Bash available for Unix-like commands
- Docker may require WSL2 on Windows
- Local Node.js preferred over system Node.js

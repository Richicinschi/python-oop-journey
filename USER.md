# USER.md

## User Profile

**Name:** Richard / digitalnomad  
**Role:** Project owner, curriculum author  
**Project:** Python OOP Journey (website + curriculum)

## What User Wants

1. **Working website** - Above all else, the site must function
2. **No babysitting** - I should handle issues autonomously
3. **Clear reports** - Tell me what broke and how you fixed it
4. **Minimal noise** - Don't report every trivial detail

## User's Technical Context

- Experienced developer
- Knows Python, JavaScript, Docker
- Uses Windows locally
- Deploys to Render
- Has CockroachDB database
- Uses Git for version control

## User's Pain Points

1. **Week/Problem pages returning 500 errors** - Priority #1
2. **Database migration conflicts** - Blocking deployment
3. **Build succeeding but runtime failing** - Most frustrating
4. **Too many audit files cluttering repo** - Already moved to _archive/

## How to Work With User

- Be direct - User prefers technical accuracy over pleasantries
- Show output - User wants to see actual command results
- Ask when stuck - User prefers questions over wrong assumptions
- Update memory - User relies on memory.md for context between sessions

## User's Deployment Setup

- **Frontend:** Render (Next.js 14)
- **Backend:** Render (FastAPI)
- **Database:** CockroachDB (external)
- **Cache:** Redis (Render)
- **Local path:** `c:\Users\digitalnomad\Documents\oopkimi\website-playground`
- **GitHub:** Richicinschi/python-oop-journey

## Critical URLs

- **Production:** https://oop-journey.onrender.com
- **API:** https://oop-journey-api.onrender.com
- **Health:** https://oop-journey-api.onrender.com/health

## What User Expects From Me

1. Fix the 500 errors on week/problem detail pages
2. Resolve database migration conflicts
3. Ensure runtime matches build success
4. Keep the repository clean
5. Maintain production readiness

## User's Preferences

- Use local Node.js at `/nodejs/node.exe` when available
- Run actual curl tests, don't just assume
- Check `memory.md` for current state
- Respect the `_archive/` folder organization
- Keep CLAW config files organized

# MEMORY.md

## Long-Term Memory

This file tracks the state of the website repair mission.

## Current Mission

**Status:** IN PROGRESS  
**Started:** 2026-03-15  
**Objective:** Fix Python OOP Journey website 500 errors and deployment issues

## Known Issues

### 🔴 CRITICAL: Week/Problem Detail Pages (500 Errors)
- **URL:** `/weeks/week00_getting_started`, `/problems/problem_01_assign_and_print`
- **Error:** 500 at runtime
- **Root Cause:** Server components fail to load curriculum data
- **Data Source:** `apps/api/data/curriculum.json` (6.1MB, 433 problems)
- **Attempted Fixes:**
  - ✅ Converted to client components
  - ✅ Added error boundaries
  - ❌ Still failing at runtime

### 🔴 CRITICAL: Database Migration Conflict
- **Error:** `Multiple head revisions are present`
- **Table:** `alembic_version` in CockroachDB
- **Fix Required:** `DROP TABLE IF EXISTS alembic_version;`
- **Status:** PENDING MANUAL DB ACCESS

### 🟡 HIGH: Build vs Runtime Discrepancy
- **Build:** ✅ TypeScript compiles, Next.js builds successfully
- **Runtime:** ❌ 500 errors on dynamic pages
- **Gap:** Need actual HTTP testing, not just static analysis

## Completed Actions

### ✅ Phase 1: UI Fixes
- Theme provider import fixed
- Settings auth protection added
- Week-card docstring display fixed

### ✅ Phase 2: Monaco Editor
- Local bundling configured
- CDN removal completed
- CSRF handling implemented

### ✅ Phase 3: Data Fetching
- Converted to client components
- Error boundaries added

### ✅ Phase 4: Security
- Settings protection
- OAuth redirect fix
- Headers configured

### ✅ Phase 5: Directory Cleanup
- 42 audit/test files moved to `_archive/`
- Organized into subdirectories:
  - `audit_reports/`
  - `test_scripts/`
  - `html_exports/`
  - `verification_reports/`
  - `old_docs/`

### ✅ Phase 6: CLAW Configuration
- `.claw/soul.yaml` created
- `.claw/instructions.md` created
- `.claw/test-plan.yaml` created
- `.claw/shell-commands.yaml` created
- `KIMI_CLAW_SETUP_GUIDE.md` created
- `setup-claw.sh` created

## Blockers

1. **Database Access** - Cannot fix migration conflict without DB console access
2. **Runtime Testing** - Build succeeds but need to verify runtime behavior
3. **Git Commit** - Cleanup done but may need explicit commit

## Next Actions

1. **Test runtime behavior** - Run dev servers and hit endpoints with curl
2. **Fix curriculum data loading** - Debug why getWeekBySlug returns undefined
3. **Resolve DB conflict** - Connect to CockroachDB and clean alembic_version
4. **Verify fixes** - Confirm week/problem pages load without 500 errors

## Test Plan

```yaml
Critical Paths:
  - Week Detail: /weeks/week00_getting_started
  - Problem Detail: /problems/problem_01_assign_and_print
  - Search: /search
  - Editor: Monaco loads on problem pages

Verification Commands:
  - Health: curl -s http://localhost:8000/health
  - Curriculum: curl -s http://localhost:8000/health/curriculum/service
  - Week API: curl -s http://localhost:8000/api/v1/curriculum/weeks/week00_getting_started
```

## Configuration

### Local Development
- **Frontend Port:** 3000
- **Backend Port:** 8000
- **Node.js:** v20.11.0 at `/nodejs/node.exe`
- **Python:** 3.11+

### Environment Variables
```
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...
```

## Session Log

### 2026-03-15 Session
- **Started:** Claw configuration for remote testing
- **Completed:** Directory cleanup, CLAW config files
- **Status:** Ready for runtime testing and debugging
- **Next:** Start dev servers and diagnose 500 errors

## Notes

- Curriculum is FILE-BASED (6.1MB JSON), not database tables
- Week 0 has special nested structure (Days 20-23)
- Build generates 433 problem pages successfully
- Issue is strictly runtime data loading in server components

# 🔥 MASTER TODO LIST - Python OOP Journey
## Complete Production Readiness Plan

**Status:** Critical Issues Remain | **Goal:** Production Ready

---

## 🔴 P0: CRITICAL (Deploy Blockers)

### 1. Fix Code Execution Sandbox
**File:** `apps/api/api/services/simple_execution.py`
**Error:** `"Execution error: 'abs', 'all', 'any', 'ascii'..."`
**Root Cause:** Malformed builtins list in restricted environment
**Fix:** Debug and fix the string formatting in sandbox setup

### 2. Fix Database Connection on Render
**File:** `apps/api/api/database.py`
**Error:** `connect() got an unexpected keyword argument 'prepare_threshold'`
**Root Cause:** Driver compatibility issue on Render
**Fix:** 
- Option A: Remove prepare_threshold entirely
- Option B: Use different asyncpg configuration
- Option C: Check Render environment variables

### 3. Fix CSRF Blocking API Requests
**Files:** 
- `apps/api/api/middleware/csrf.py`
- `apps/web/contexts/csrf-context.tsx`
- `apps/web/lib/api.ts`
**Error:** All POST requests return 403 "CSRF token missing"
**Fix Options:**
- Option A: Fix frontend to properly send CSRF tokens
- Option B: Exempt API routes from CSRF (they use cookie auth)
- Option C: Simpler - remove CSRF for API, keep for forms

### 4. Fix Rate Limiting
**Files:**
- `apps/api/api/__init__.py`
- `apps/api/api/routers/execute.py`
- `apps/api/api/routers/verification.py`
**Error:** 35 requests sent, 0 rate limited
**Fix:** 
- Verify slowapi configuration
- Check if Redis required
- Ensure decorators are working

---

## 🟠 P1: HIGH (Major User Impact)

### 5. Fix Day Pages 404
**File:** `apps/web/app/weeks/[weekSlug]/days/[daySlug]/page.tsx` (check if exists)
**Error:** All `/weeks/*/days/*` return 404
**Fix:**
- Check file routing
- Check data fetching
- Verify curriculum data has days

### 6. Fix Problem Pages Loading
**Files:**
- `apps/web/app/problems/[problemSlug]/page.tsx`
- `apps/web/components/editor/code-editor.tsx`
**Error:** Only shows loading skeletons, no Monaco editor
**Fix:**
- Debug client-side data fetching
- Check Monaco initialization
- Verify problem API returns data

### 7. Fix Missing Static Assets
**Files to Create:**
- `apps/web/public/favicon.ico`
- `apps/web/public/icon-72x72.png`
- `apps/web/public/icon-192x192.png`
- `apps/web/public/icon-512x512.png`
- `apps/web/public/screenshot-wide.png`
- `apps/web/public/screenshot-narrow.png`
**Fix:** Generate or create placeholder assets

---

## 🟡 P2: MEDIUM (Should Fix)

### 8. Clean Console.log Statements
**Files:**
- `apps/web/lib/monaco.ts:298`
- `apps/web/app/(dashboard)/weeks/[weekSlug]/project/page.tsx:173,177`
**Fix:** Remove or make dev-only

### 9. Fix Unused Import
**File:** `apps/web/app/problems/[problemSlug]/page.tsx:9`
**Fix:** Remove unused `Badge` import

### 10. Add Footer to Home Page
**File:** `apps/web/app/page.tsx`
**Fix:** Add Footer component

### 11. Fix Week 8 Content Count
**Issue:** Shows "0 days, 0 problems"
**Fix:** Check curriculum data

### 12. Verify Mobile Menu
**Issue:** No mobile menu toggle visible
**Fix:** Check responsive design

---

## 🟢 P3: LOW (Nice to Have)

### 13. Add Strict TypeScript Types
**File:** `components/curriculum/theory-content.tsx`
**Fix:** Replace `any` with proper types

### 14. Add Retry Logic to API Client
**File:** `apps/web/lib/api.ts`
**Fix:** Add exponential backoff for transient failures

### 15. Optimize Images
**Task:** Run next/image optimization

### 16. Add Loading State to CSRF Context
**File:** `apps/web/contexts/csrf-context.tsx`
**Fix:** Expose loading state for UI

---

## 📋 DEPLOYMENT CHECKLIST

### Pre-Deploy
- [ ] All P0 issues fixed
- [ ] All P1 issues fixed
- [ ] Build passes locally
- [ ] Build passes on Render
- [ ] Database connected
- [ ] Code execution working
- [ ] All API endpoints responding

### Deploy
- [ ] Push to GitHub
- [ ] Render auto-deploys
- [ ] Verify deployment

### Post-Deploy Verification
- [ ] Home page loads
- [ ] Week pages load
- [ ] Day pages load
- [ ] Problem pages load with editor
- [ ] Code execution works
- [ ] Search works
- [ ] Login works
- [ ] Settings work
- [ ] All critical user flows work

---

## 🎯 AGENT DEPLOYMENT PLAN

### Phase 1: Critical Fixes (Deploy 6 agents)
1. Backend Architect - Fix code execution sandbox
2. Backend Architect - Fix database connection
3. Security Engineer - Fix CSRF blocking
4. Backend Architect - Fix rate limiting
5. Frontend Developer - Fix day pages
6. Frontend Developer - Fix problem pages

### Phase 2: High Priority (Deploy 4 agents)
7. Frontend Developer - Create static assets
8. Code Reviewer - Clean console.logs
9. Code Reviewer - Fix unused imports
10. Frontend Developer - Add footer

### Phase 3: Polish (Deploy 2 agents)
11. Code Reviewer - Add TypeScript types
12. Backend Architect - Add retry logic

**Total: 12 agents deployed in 3 phases**

---

## 📊 SUCCESS METRICS

### Must Achieve (P0)
- [ ] Code execution returns output (not error)
- [ ] Database health check returns 200
- [ ] POST requests work without CSRF blocking
- [ ] Rate limiting returns 429 after 30 requests

### Should Achieve (P1)
- [ ] Day pages load (not 404)
- [ ] Problem pages show editor (not skeletons)
- [ ] No missing asset 404s

### Nice to Have (P2)
- [ ] No console.log in production
- [ ] No unused imports
- [ ] All pages have footer

---

## 🚨 ESCALATION CRITERIA

**Escalate to User If:**
- Database issue requires Render dashboard access
- Environment variables need changing
- Domain/DNS configuration needed
- Budget approval required (upgraded services)

**Auto-Fix If:**
- Code changes only
- Configuration in repo
- No external dependencies

---

*Master TODO List - Ready for Agent Deployment*

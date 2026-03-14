# Execution Plan: Website Playground Build

## Overview
Build the perfect interactive learning platform for the Python OOP Journey curriculum.

**Timeline:** 12-16 weeks  
**Team:** Multi-agent parallel development  
**Goal:** Production-ready platform with all 9 phases complete

---

## Phase 1: Foundation (Weeks 1-2)

### Milestone: Content ingestion works, basic navigation functional

**Agent 1: Core Infrastructure** (No dependencies)
- [ ] Set up monorepo with pnpm workspaces
- [ ] Create shared TypeScript types (Curriculum, Week, Day, Problem, User, Progress)
- [ ] Build UI component library (Button, Card, Badge, Separator, ScrollArea, Tabs)
- [ ] Create theme/styling system (Tailwind config, colors, typography)
- [ ] Build navigation components (Sidebar, Breadcrumbs, NavLink)

**Agent 2: Curriculum Ingestion** (Depends on Agent 1 types)
- [ ] Finalize ingest.py script
- [ ] Test ingestion against python-oop-journey-v2
- [ ] Create data validation (schema validation)
- [ ] Build watch mode for development
- [ ] Generate TypeScript types from curriculum data

**Agent 3: Frontend Scaffold** (Depends on Agent 1)
- [ ] Initialize Next.js 14 with App Router
- [ ] Set up project structure (app/, components/, lib/, hooks/)
- [ ] Configure Tailwind, TypeScript, ESLint
- [ ] Build root layout with navigation shell
- [ ] Create curriculum context/provider

**Agent 4: Backend API Foundation** (Depends on Agent 1)
- [ ] Initialize FastAPI project
- [ ] Set up database connection (SQLAlchemy + asyncpg)
- [ ] Create Alembic migrations
- [ ] Build health check endpoints
- [ ] Set up logging and error handling

**Agent 5: Docker Infrastructure** (Independent)
- [ ] Create docker-compose.yml for all services
- [ ] Build sandbox Dockerfile
- [ ] Test sandbox security constraints
- [ ] Set up local development environment
- [ ] Create Makefile for common commands

### Phase 1 Success Criteria
- [ ] Can run `docker-compose up` and all services start
- [ ] Can ingest curriculum and get valid JSON
- [ ] Can view week list at `/weeks`
- [ ] Can navigate to individual week pages
- [ ] All agents' code integrates cleanly

---

## Phase 2: Content & Navigation (Weeks 3-4)

### Milestone: Complete curriculum browsing experience

**Agent 6: Content Pages** (Depends on Phase 1)
- [ ] Build week listing page (grid of cards)
- [ ] Build week detail page (day list, objectives, project overview)
- [ ] Build day detail page (theory summary, problem list)
- [ ] Build theory page (markdown rendering with TOC)
- [ ] Implement previous/next navigation
- [ ] Add progress indicators (started/completed states)

**Agent 7: Search & Discovery** (Can parallel with Agent 6)
- [ ] Build search index from curriculum
- [ ] Create search API endpoint
- [ ] Build search UI (modal/command palette)
- [ ] Add filters (week, difficulty, topic)
- [ ] Create "Continue Learning" widget
- [ ] Build bookmarks page structure

**Agent 8: Homepage & Dashboard** (Depends on Agent 6)
- [ ] Build learner dashboard (continue where left off)
- [ ] Create progress visualization
- [ ] Add recent activity feed
- [ ] Build curriculum map/overview
- [ ] Implement resume functionality

### Phase 2 Success Criteria
- [ ] Can browse all weeks and days
- [ ] Can read theory with good typography
- [ ] Can search and find content
- [ ] Homepage shows personalized dashboard
- [ ] Navigation is fast and intuitive

---

## Phase 3: Playground MVP (Weeks 5-6)

### Milestone: Code editing and execution works

**Agent 9: Monaco Editor Integration** (Depends on Phase 1)
- [ ] Integrate @monaco-editor/react
- [ ] Configure Python language support
- [ ] Set up theme matching (dark/light)
- [ ] Implement editor controls (reset, save, run)
- [ ] Add keyboard shortcuts
- [ ] Handle editor state (unsaved changes)

**Agent 10: Code Execution Backend** (Depends on Agent 5 Docker)
- [ ] Build /api/execute/run endpoint
- [ ] Integrate Docker SDK for Python
- [ ] Implement job queue with Celery + Redis
- [ ] Handle timeouts (10 seconds)
- [ ] Capture stdout/stderr
- [ ] Return structured execution results

**Agent 11: Problem Page** (Depends on Agents 9, 10, 6)
- [ ] Build problem page layout (instructions + editor)
- [ ] Integrate Monaco editor
- [ ] Add Run button with loading states
- [ ] Display execution output panel
- [ ] Handle errors gracefully
- [ ] Add starter code loading

**Agent 12: Verification System** (Depends on Agent 10)
- [ ] Build /api/execute/verify endpoint
- [ ] Load test code from curriculum
- [ ] Run tests in sandbox
- [ ] Parse pytest results
- [ ] Return learner-friendly feedback
- [ ] Track verification results

### Phase 3 Success Criteria
- [ ] Can edit code in Monaco editor
- [ ] Can run code and see output
- [ ] Code executes in sandbox (safe)
- [ ] Can verify solutions against tests
- [ ] Clear pass/fail feedback

---

## Phase 4: Learner State & Auth (Weeks 7-8)

### Milestone: Users can sign up, track progress, resume

**Agent 13: Authentication** (Depends on Agent 4)
- [ ] Implement magic link auth
- [ ] Build login/signup flows
- [ ] Set up JWT tokens
- [ ] Create auth middleware
- [ ] Protect routes
- [ ] Add auth UI components

**Agent 14: Database Models & API** (Depends on Agent 4)
- [ ] Create User model
- [ ] Create Progress model
- [ ] Create Draft model
- [ ] Create Bookmark model
- [ ] Build CRUD endpoints
- [ ] Add database migrations

**Agent 15: Progress Tracking** (Depends on Agent 14)
- [ ] Track theory pages read
- [ ] Track problems started
- [ ] Track problems completed
- [ ] Track verification results
- [ ] Build progress API endpoints
- [ ] Create progress UI components

**Agent 16: Persistence Features** (Depends on Agent 14)
- [ ] Auto-save code drafts
- [ ] Manual save functionality
- [ ] Resume last session
- [ ] Recently visited tracking
- [ ] Bookmarks save/load
- [ ] Personal notes (basic)

### Phase 4 Success Criteria
- [ ] Can sign up/login with magic links
- [ ] Progress persists across sessions
- [ ] Can resume where left off
- [ ] Code drafts auto-save
- [ ] Bookmarks work

---

## Phase 5: Help System (Weeks 9-10)

### Milestone: Complete hint and solution system

**Agent 17: Hint System** (Depends on Phase 3)
- [ ] Build hint storage/retrieval
- [ ] Create Hint component (3-tier)
- [ ] Add progressive reveal
- [ ] Track hint usage
- [ ] Style hints appropriately
- [ ] Add hint navigation

**Agent 18: Solution Reveal** (Depends on Phase 3)
- [ ] Load reference solutions
- [ ] Create solution reveal modal
- [ ] Add confirmation step
- [ ] Show side-by-side comparison
- [ ] Track solution views
- [ ] Add educational notes

**Agent 19: Verification Feedback** (Depends on Agent 12)
- [ ] Parse test failures
- [ ] Categorize errors (wrong output, exception, timeout)
- [ ] Create helpful error messages
- [ ] Link to relevant theory
- [ ] Suggest hints based on failures
- [ ] Show test case details

**Agent 20: Common Mistakes & Tips** (Depends on Phase 3)
- [ ] Display common mistakes section
- [ ] Add debugging tips
- [ ] Link to related problems
- [ ] Create "Why this works" explanations
- [ ] Add conceptual nudges

### Phase 5 Success Criteria
- [ ] 3-tier hint system works
- [ ] Solution reveal is intentional
- [ ] Verification feedback is helpful
- [ ] Common mistakes are documented
- [ ] Learners feel supported

---

## Phase 6: Projects (Weeks 11-12)

### Milestone: Weekly projects are first-class

**Agent 21: Project Pages** (Depends on Phase 6)
- [ ] Build project listing page
- [ ] Create project detail page
- [ ] Show project requirements
- [ ] Display starter code structure
- [ ] Add project verification
- [ ] Link to daily lessons

**Agent 22: Multi-File Editor** (Depends on Agent 9)
- [ ] Extend Monaco for multiple files
- [ ] Create file tree sidebar
- [ ] Implement file tabs
- [ ] Handle file creation/deletion
- [ ] Save multi-file drafts
- [ ] Project-specific verification

**Agent 23: Project Submission** (Depends on Agent 21)
- [ ] Build submission flow
- [ ] Run full project tests
- [ ] Create submission feedback
- [ ] Show completion criteria
- [ ] Generate completion certificate
- [ ] Archive submissions

### Phase 6 Success Criteria
- [ ] Project pages are comprehensive
- [ ] Multi-file editing works
- [ ] Projects can be verified
- [ ] Clear completion criteria
- [ ] Projects feel like capstones

---

## Phase 7: Polish & Launch Prep (Weeks 13-16)

### Milestone: Production-ready

**Agent 24: Mobile & Responsive** (Depends on all phases)
- [ ] Mobile navigation
- [ ] Responsive theory pages
- [ ] Touch-friendly editor controls
- [ ] Mobile-optimized layouts
- [ ] Test on real devices

**Agent 25: Performance & Accessibility** (Depends on all phases)
- [ ] Optimize bundle size
- [ ] Implement lazy loading
- [ ] Add accessibility attributes
- [ ] Keyboard navigation
- [ ] Screen reader support
- [ ] Performance audit

**Agent 26: Testing & QA** (Depends on all phases)
- [ ] Unit tests (Jest/Vitest)
- [ ] Integration tests (Playwright)
- [ ] API tests (pytest)
- [ ] Sandbox security tests
- [ ] Load testing
- [ ] Bug fixes

**Agent 27: Deployment & DevOps** (Depends on all phases)
- [ ] Production Docker setup
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Environment configuration
- [ ] Domain setup
- [ ] SSL certificates
- [ ] Monitoring (Sentry, logs)
- [ ] Backup strategy

**Agent 28: Documentation** (Depends on all phases)
- [ ] User documentation
- [ ] API documentation
- [ ] Deployment guide
- [ ] Content ingestion guide
- [ ] Troubleshooting guide
- [ ] Video tutorials (optional)

### Phase 7 Success Criteria
- [ ] All tests passing
- [ ] Performance targets met
- [ ] Accessibility standards met
- [ ] Production deployed
- [ ] Documentation complete
- [ ] Ready for learners

---

## Critical Path

```
Week 1-2:  Agents 1-5 (Foundation) PARALLEL
Week 3-4:  Agents 6-8 (Content) PARALLEL
Week 5-6:  Agents 9-12 (Playground) PARALLEL
Week 7-8:  Agents 13-16 (Auth/State) PARALLEL
Week 9-10: Agents 17-20 (Help) PARALLEL
Week 11-12: Agents 21-23 (Projects) PARALLEL
Week 13-16: Agents 24-28 (Polish) PARALLEL
```

## Dependencies Graph

```
Agent 1 (Types/UI) ──┬──► Agent 3 (Frontend)
                     ├──► Agent 4 (Backend)
                     └──► Agent 2 (Ingestion)

Agent 5 (Docker) ────► Agent 10 (Execution)
                      ► Agent 12 (Verification)

Agent 2 (Ingestion) ─► Agent 6 (Content)
                     ─► Agent 11 (Problem Page)

Agent 3 (Frontend) ──► Agent 6 (Content)
                     ─► Agent 9 (Editor)

Agent 4 (Backend) ───► Agent 13 (Auth)
                     ─► Agent 14 (DB)
                     ─► Agent 10 (Execution)

Agent 6 (Content) ───► Agent 8 (Dashboard)
                     ─► Agent 11 (Problem)
                     ─► Agent 21 (Projects)

Agent 9 (Editor) ────► Agent 11 (Problem)
                     ─► Agent 22 (Multi-file)

Agent 10 (Execution) ─► Agent 11 (Problem)
                      ─► Agent 12 (Verify)

Agent 13 (Auth) ─────► Agent 15 (Progress)
                     ─► Agent 16 (Persistence)

Agent 14 (DB) ───────► Agent 15 (Progress)
                     ─► Agent 16 (Persistence)

All Previous ────────► Agents 24-28 (Polish)
```

## Communication Protocol

1. **Daily Standups** (simulated): Report blockers, progress
2. **Integration Points**: End of each phase, all agents integrate
3. **Code Review**: Cross-agent review for integration points
4. **Testing**: Each agent tests their own work + integration tests

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Monaco integration issues | Have fallback (CodeMirror), test early |
| Sandbox security | Security audit at Phase 3, penetration testing |
| Performance | Profiling in Phase 7, optimization sprints |
| Scope creep | Strict phase definitions, no new features mid-phase |
| Integration failures | Daily builds, automated integration tests |

## Success Metrics

- **Phase 1:** Can browse curriculum
- **Phase 2:** Can read all theory
- **Phase 3:** Can run and verify code
- **Phase 4:** Can sign up and resume
- **Phase 5:** Hints and solutions work
- **Phase 6:** Projects are complete
- **Phase 7:** Production ready, <2s load times, 100% test pass

## Final Deliverable

A production-ready learning platform that:
1. Ingests curriculum from python-oop-journey-v2
2. Provides interactive code editing and execution
3. Tracks learner progress
4. Offers helpful hints and solutions
5. Supports weekly projects
6. Works on desktop and mobile
7. Is secure and performant
8. Is deployable to a custom domain

# Development Phases

This document outlines the phased development approach for the website playground.

## Phase 1: Foundation (Weeks 1-2)

**Goal:** Basic content ingestion and navigation

### Deliverables
- [ ] Scaffold Next.js frontend with TypeScript
- [ ] Scaffold FastAPI backend
- [ ] Implement curriculum ingestion script
- [ ] Create data models (Week, Day, Problem, Project)
- [ ] Build week/day navigation
- [ ] Render theory pages (markdown)
- [ ] Basic problem page structure
- [ ] Docker compose setup

### Success Criteria
- Can ingest curriculum from repo
- Can navigate Week → Day → Theory
- Can view problem instructions
- No code execution yet

---

## Phase 2: Playground MVP (Weeks 3-4)

**Goal:** Code editing and execution

### Deliverables
- [ ] Integrate Monaco Editor
- [ ] Implement code execution sandbox (Docker)
- [ ] Run code endpoint
- [ ] Display stdout/stderr
- [ ] Load starter code
- [ ] Basic error handling
- [ ] Timeout and resource limits

### Success Criteria
- Can edit code in browser
- Can run code and see output
- Code runs in isolated sandbox
- 10-second timeout enforced
- No verification yet

---

## Phase 3: Learner State (Weeks 5-6)

**Goal:** Progress tracking and persistence

### Deliverables
- [ ] User authentication (magic links)
- [ ] Progress tracking (problem started/solved)
- [ ] Save code drafts
- [ ] Resume functionality
- [ ] Theory read tracking
- [ ] Recently visited
- [ ] Basic profile

### Success Criteria
- Can sign up/login
- Progress persists across sessions
- Can resume where left off
- Can see completion status

---

## Phase 4: Verification & Help (Weeks 7-8)

**Goal:** Verification system and hints

### Deliverables
- [ ] Implement verify endpoint (runs tests)
- [ ] Learner-friendly verification feedback
- [ ] 3-tier hint system
- [ ] Solution reveal (intentional)
- [ ] Common mistakes display
- [ ] Theory cross-links

### Success Criteria
- Can verify solutions against tests
- Clear pass/fail feedback
- Hints work progressively
- Solution reveal requires intent

---

## Phase 5: Project Experience (Weeks 9-10)

**Goal:** Weekly projects support

### Deliverables
- [ ] Project pages
- [ ] Multi-file editing
- [ ] File tree navigation
- [ ] Project verification
- [ ] Starter/solution/reference structure

### Success Criteria
- Projects are first-class pages
- Can work on multi-file projects
- Can verify project solutions

---

## Phase 6: Product Polish (Weeks 11-12)

**Goal:** Professional polish and extras

### Deliverables
- [ ] Search functionality
- [ ] Bookmarks
- [ ] Notes per page
- [ ] Mobile reading experience
- [ ] Accessibility audit
- [ ] Performance optimization
- [ ] Error boundaries
- [ ] Loading states

### Success Criteria
- Feels like a premium product
- Works on mobile (reading)
- Accessible
- Fast navigation

---

## Phase 7: Launch Prep (Week 13+)

**Goal:** Production readiness

### Deliverables
- [ ] Domain configuration
- [ ] HTTPS setup
- [ ] Environment configuration
- [ ] Monitoring and logging
- [ ] Backup strategy
- [ ] Documentation
- [ ] Launch checklist

### Success Criteria
- Deployed to custom domain
- Production monitoring
- Ready for learners

---

## Dependencies Between Phases

```
Phase 1 (Foundation)
    ↓
Phase 2 (Playground) - needs Docker sandbox
    ↓
Phase 3 (Learner State) - needs auth
    ↓
Phase 4 (Verification) - needs tests from repo
    ↓
Phase 5 (Projects) - needs multi-file editor
    ↓
Phase 6 (Polish) - can happen in parallel with 4-5
    ↓
Phase 7 (Launch)
```

## Risk Mitigation

**Biggest Risks:**
1. **Sandbox security** - Start with Docker, audit before launch
2. **Performance** - Test with full curriculum loaded
3. **Content sync** - Automated ingestion, manual review

**Mitigation:**
- Security audit before Phase 7
- Load testing in Phase 6
- Content validation in CI

## Resource Estimates

**Development Time:** 12-16 weeks (1 developer)
**Infrastructure Cost:** ~$100-200/month
- VPS: $40-80
- Database: $15-30
- Redis: $10-20
- Domain: $10-20/year
- Monitoring: $20-50

## Success Metrics

**Phase 1-2:** Technical proof of concept
**Phase 3-4:** Core learning loop works
**Phase 5-6:** Product feels polished
**Phase 7:** Ready for paying customers

**Launch Criteria:**
- 100% tests passing
- No critical bugs
- <2 second page loads
- Sandbox secure
- Content synced

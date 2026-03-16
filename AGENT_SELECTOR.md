# Agency Agents - Quick Selector Guide

**Location:** `c:\Users\digitalnomad\Documents\oopkimi\agency-agents`

## How to Use

When you need specialized help, reference this guide and use the Task tool with the agent's file:

```
Task: <task_description>
subagent_name: coder
prompt: |
  <Read the agent file from agency-agents/ folder>
  <Include the agent's identity and critical rules>
  <Add your specific task>
```

---

## For Website Development (Python OOP Journey)

### Frontend Issues (React/Next.js/TypeScript)

| Agent | File | Use When |
|-------|------|----------|
| **Frontend Developer** | `engineering/engineering-frontend-developer.md` | React components, UI implementation, TypeScript fixes |
| **Code Reviewer** | `engineering/engineering-code-reviewer.md` | PR reviews, code quality checks, finding bugs |
| **Senior Developer** | `engineering/engineering-senior-developer.md` | Complex architecture decisions, advanced patterns |

### Backend Issues (FastAPI/Python)

| Agent | File | Use When |
|-------|------|----------|
| **Backend Architect** | `engineering/engineering-backend-architect.md` | API design, database architecture, scalability |
| **Database Optimizer** | `engineering/engineering-database-optimizer.md` | Query optimization, schema design, indexing |
| **Security Engineer** | `engineering/engineering-security-engineer.md` | Security reviews, vulnerability assessment |

### DevOps & Infrastructure

| Agent | File | Use When |
|-------|------|----------|
| **DevOps Automator** | `engineering/engineering-devops-automator.md` | CI/CD, deployment automation |
| **SRE** | `engineering/engineering-sre.md` | Production reliability, monitoring |
| **Incident Response Commander** | `engineering/engineering-incident-response-commander.md` | Production incidents |

### Testing & QA

| Agent | File | Use When |
|-------|------|----------|
| **Code Reviewer** | `engineering/engineering-code-reviewer.md` | Code quality, security review |
| **Reality Checker** | `testing/testing-reality-checker.md` | Production readiness verification |
| **Evidence Collector** | `testing/testing-evidence-collector.md` | Visual QA, screenshot-based testing |
| **Test Results Analyzer** | `testing/testing-test-results-analyzer.md` | Test suite analysis, coverage reports |

### Documentation

| Agent | File | Use When |
|-------|------|----------|
| **Technical Writer** | `engineering/engineering-technical-writer.md` | Developer docs, API reference |

---

## Common Task Patterns

### 1. Fix a Bug
```
Agent: Code Reviewer (find root cause)
Then: Frontend Developer or Backend Architect (implement fix)
Then: Reality Checker (verify the fix)
```

### 2. Build a New Feature
```
Agent: Software Architect (design)
Then: Frontend Developer (UI) + Backend Architect (API)
Then: Code Reviewer (review)
Then: Evidence Collector (QA testing)
```

### 3. Production Issue
```
Agent: Incident Response Commander (assess)
Then: SRE (implement fix)
Then: Reality Checker (verify production ready)
```

### 4. Performance Problem
```
Agent: Database Optimizer (if DB related)
Or: Frontend Developer (if UI related)
Then: Reality Checker (benchmark)
```

### 5. Security Concern
```
Agent: Security Engineer (audit)
Then: Backend Architect or Frontend Developer (fix)
Then: Code Reviewer (verify fix)
```

---

## Full Agent Inventory

### Engineering Division
- `engineering-frontend-developer.md` - React/Vue/Angular, UI implementation
- `engineering-backend-architect.md` - API design, databases, scalability
- `engineering-mobile-app-builder.md` - iOS/Android, React Native
- `engineering-ai-engineer.md` - ML models, AI integration
- `engineering-devops-automator.md` - CI/CD, infrastructure
- `engineering-rapid-prototyper.md` - Fast MVPs, proof-of-concepts
- `engineering-senior-developer.md` - Laravel/Livewire, advanced patterns
- `engineering-security-engineer.md` - Threat modeling, secure code
- `engineering-database-optimizer.md` - PostgreSQL/MySQL tuning
- `engineering-code-reviewer.md` - Constructive code reviews
- `engineering-software-architect.md` - System design, DDD
- `engineering-sre.md` - SLOs, observability, chaos engineering
- `engineering-technical-writer.md` - Developer docs
- `engineering-data-engineer.md` - Data pipelines, ETL
- `engineering-git-workflow-master.md` - Branching strategies

### Testing Division
- `testing-reality-checker.md` - Production readiness
- `testing-evidence-collector.md` - Screenshot QA, visual proof
- `testing-test-results-analyzer.md` - Test evaluation, metrics
- `testing-performance-benchmarker.md` - Performance testing
- `testing-api-tester.md` - API validation
- `testing-accessibility-auditor.md` - WCAG compliance

### Design Division
- `design-ui-designer.md` - Visual design, component libraries
- `design-ux-researcher.md` - User testing, behavior analysis
- `design-ux-architect.md` - Technical architecture, CSS systems

### Project Management
- `project-management-project-shepherd.md` - Cross-functional coordination
- `project-management-senior-project-manager.md` - Scoping, task conversion

---

## Quick Reference: Agents We've Used

| Task | Agent Used | File |
|------|-----------|------|
| Fix TypeScript errors | Frontend Developer | `engineering-frontend-developer.md` |
| Code audit | Code Reviewer | `engineering-code-reviewer.md` |
| Production readiness | Reality Checker | `testing-testing-reality-checker.md` |
| Visual QA | Evidence Collector | `testing-testing-evidence-collector.md` |
| Test analysis | Test Results Analyzer | `testing-testing-test-results-analyzer.md` |

---

## Using Agents in Commands

Example usage:

```python
# Fix a TypeScript error
Task: Fix TypeScript build error
subagent_name: coder
prompt: |
  Read the agent definition from: agency-agents/engineering/engineering-frontend-developer.md
  
  Use this agent's approach to fix the TypeScript error:
  - File: apps/web/components/ui/badge.tsx
  - Error: Type 'destructive' not assignable
  
  Follow the agent's critical rules and deliverables.
```

---

## Maintenance

Keep this agent repository updated:

```bash
cd c:\Users\digitalnomad\Documents\oopkimi\agency-agents
git pull origin main
```

---

*Last updated: 2026-03-15*

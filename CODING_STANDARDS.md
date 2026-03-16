# Python OOP Journey - Coding Standards & Best Practices
## Rules to Prevent Recurring Mistakes

**Version:** 1.0  
**Last Updated:** March 16, 2026  
**Based on:** Analysis of 233 commits

---

## Table of Contents

1. [General Principles](#general-principles)
2. [TypeScript Standards](#typescript-standards)
3. [Python Standards](#python-standards)
4. [React/Next.js Standards](#reactnextjs-standards)
5. [Database Standards](#database-standards)
6. [Docker Standards](#docker-standards)
7. [Git Standards](#git-standards)
8. [Testing Standards](#testing-standards)
9. [Security Standards](#security-standards)
10. [Pre-Commit Checklist](#pre-commit-checklist)

---

## General Principles

### 1. Test Before You Commit
**Rule:** Never commit code that has not been tested locally.

```bash
# Required checks before commit
npm run lint        # Check for linting errors
npm run type-check  # Check TypeScript types
npm run build       # Verify build succeeds
npm run test        # Run unit tests
```

### 2. Small, Focused Commits
**Rule:** Each commit should address a single concern.

```bash
# GOOD - Small, focused commits
git commit -m "fix: add missing Path import in main.py"
git commit -m "feat: add user authentication middleware"
git commit -m "docs: update API documentation"

# BAD - Large, unfocused commits
git commit -m "ROUND 5 FIXES: WebSocket auth, Config, Security, Performance"
```

### 3. Never Disable Checks
**Rule:** Fix the root cause, not the symptom.

```javascript
// BAD - Disabling checks
// next.config.js
eslint: { ignoreDuringBuilds: true },
typescript: { ignoreBuildErrors: true },

// GOOD - Fix the actual issues
// Fix TypeScript errors
// Fix ESLint violations
```

---

## TypeScript Standards

### 1. Always Use Strict Type Checking

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true
  }
}
```

### 2. Use Optional Chaining and Nullish Coalescing

```typescript
// BAD - No null check
const title = reviewQueue.problemTitle;  // May throw if reviewQueue is null

// GOOD - With null check
const title = reviewQueue?.problemTitle ?? 'Unknown';
```

### 3. Define Complete Types

```typescript
// BAD - Incomplete type
interface UserProjectProgress {
  userId: string;
  projectId: string;
  // Missing fields!
}

// GOOD - Complete type
interface UserProjectProgress {
  userId: string;
  projectId: string;
  startTime: Date;
  lastActiveTime: Date;
  totalTimeSpent: number;
  files: ProjectFile[];
}
```

### 4. Use Clear Type Naming

```typescript
// BAD - Ambiguous naming
interface ReviewQueue { ... }  // Frontend
interface ReviewQueue { ... }  // Backend (different!)

// GOOD - Clear naming
interface AdminReviewQueue { ... }      // Admin panel
interface ReviewQueueResponse { ... }   // API response
interface ReviewQueueItem { ... }       // Individual item
```

### 5. Import Types Explicitly

```typescript
// BAD - No type import
import { ReviewQueue } from './types';

// GOOD - Explicit type import
import type { ReviewQueue, ReviewQueueItem } from './types';
```

---

## Python Standards

### 1. Always Import Required Modules

```python
# BAD - Missing import
from fastapi import FastAPI

@app.get("/items/{item_id}")
async def read_item(item_id: Path(...)):  # ERROR!
    pass

# GOOD - Proper import
from fastapi import FastAPI, Path

@app.get("/items/{item_id}")
async def read_item(item_id: Path(...)):
    pass
```

### 2. Use Type Hints

```python
# BAD - No type hints
def get_user(user_id):
    return db.query(User).filter(User.id == user_id).first()

# GOOD - With type hints
from typing import Optional

def get_user(user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()
```

### 3. Use Pydantic for API Models

```python
from pydantic import BaseModel, Field

# GOOD - Documented API model
class ReviewQueueResponse(BaseModel):
    """Response model for review queue endpoint.

    Fields:
    - problem_title: Human-readable problem title
    - problem_slug: URL-friendly problem identifier
    - days_overdue: Number of days past review date
    """
    problem_title: str = Field(..., description="Human-readable problem title")
    problem_slug: str = Field(..., description="URL-friendly problem identifier")
    days_overdue: int = Field(..., description="Number of days past review date")
```

### 4. Handle Errors Properly

```python
# BAD - No error handling
@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    return db.query(User).filter(User.id == user_id).first()

# GOOD - With error handling
from fastapi import HTTPException

@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## React/Next.js Standards

### 1. Wrap Client Hooks in Suspense

```tsx
// BAD - Client hook in server component
function SearchPage() {
    const searchParams = useSearchParams();  // ERROR during SSR
    return <div>{searchParams.get('q')}</div>;
}

// GOOD - Wrapped in Suspense
function SearchPage() {
    return (
        <Suspense fallback={<Loading />}>
            <SearchContent />
        </Suspense>
    );
}

function SearchContent() {
    const searchParams = useSearchParams();  // OK - client-side only
    return <div>{searchParams.get('q')}</div>;
}
```

### 2. Use Dynamic Imports for Client Components

```tsx
// BAD - Direct import of client component
import MonacoEditor from '@monaco-editor/react';

// GOOD - Dynamic import with SSR disabled
const MonacoEditor = dynamic(
    () => import('@monaco-editor/react'),
    {
        ssr: false,
        loading: () => <div>Loading editor...</div>
    }
);
```

### 3. Use Proper Error Boundaries

```tsx
// GOOD - Error boundary for components
class ErrorBoundary extends React.Component {
    state = { hasError: false };

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error('Error:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return <ErrorFallback />;
        }
        return this.props.children;
    }
}
```

### 4. Use Custom Hooks for Reusable Logic

```tsx
// GOOD - Custom hook for API calls
function useApi<T>(url: string) {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        fetch(url)
            .then(res => res.json())
            .then(setData)
            .catch(setError)
            .finally(() => setLoading(false));
    }, [url]);

    return { data, loading, error };
}
```

---

## Database Standards

### 1. Make Migrations Idempotent

```python
# GOOD - Idempotent migration
def upgrade():
    # Check if table exists before creating
    if not op.table_exists('user_settings'):
        op.create_table(
            'user_settings',
            sa.Column('id', sa.String(32), primary_key=True),
            sa.Column('user_id', sa.String(32), nullable=False),
            # ...
        )

# BAD - Non-idempotent migration
def upgrade():
    op.create_table(
        'user_settings',
        # ...
    )  # Fails if table exists!
```

### 2. Test Migrations Locally

```bash
# Test migration down and up
alembic downgrade -1
alembic upgrade head

# Verify database state
psql $DATABASE_URL -c "SELECT * FROM user_settings LIMIT 1;"
```

### 3. Use Short Migration Names

```python
# BAD - Long name
revision = 'add_user_settings_table_with_all_columns_and_indexes'

# GOOD - Short name
revision = 'add_user_settings'
```

---

## Docker Standards

### 1. Use Exec Form for ENTRYPOINT

```dockerfile
# BAD - Shell form (creates shell process)
ENTRYPOINT python app.py

# GOOD - Exec form (direct process)
ENTRYPOINT ["python", "app.py"]
```

### 2. Set WORKDIR Properly

```dockerfile
# BAD - No WORKDIR
COPY . .
RUN python app.py  # Files in wrong location

# GOOD - Proper WORKDIR
WORKDIR /app
COPY . .
RUN python app.py
```

### 3. Test Docker Locally

```bash
# Build and test locally
docker-compose up --build

# Verify container health
docker ps
docker logs <container_id>
```

---

## Git Standards

### 1. Use Conventional Commits

```bash
# Format: <type>: <description>
git commit -m "fix: add missing Path import"
git commit -m "feat: add user authentication"
git commit -m "docs: update API documentation"
git commit -m "refactor: simplify error handling"
git commit -m "test: add unit tests for auth"
git commit -m "chore: update dependencies"
```

### 2. Write Clear Commit Messages

```bash
# BAD - Unclear
git commit -m "fix stuff"

# GOOD - Clear and descriptive
git commit -m "fix: resolve TypeScript error in review-queue-card.tsx

The ReviewQueueItem type was renamed to AdminReviewQueueItem
but the component was still using the old type name."
```

### 3. Never Commit Broken Code

```bash
# Test before commit
npm run lint
npm run type-check
npm run build
npm run test

# Only then commit
git commit -m "fix: resolve TypeScript errors"
```

---

## Testing Standards

### 1. Write Unit Tests

```typescript
// GOOD - Unit test
describe('ReviewQueueCard', () => {
    it('renders with valid data', () => {
        const item: AdminReviewQueueItem = {
            problemTitle: 'Test Problem',
            problemSlug: 'test-problem',
            daysOverdue: 3
        };

        render(<ReviewQueueCard item={item} />);

        expect(screen.getByText('Test Problem')).toBeInTheDocument();
    });
});
```

### 2. Test Edge Cases

```typescript
// GOOD - Test edge cases
it('handles null data gracefully', () => {
    render(<ReviewQueueCard item={null} />);

    expect(screen.getByText('No review items')).toBeInTheDocument();
});
```

### 3. Run Tests Before Commit

```bash
# Always run tests
npm run test

# With coverage
npm run test:coverage
```

---

## Security Standards

### 1. Implement CSRF Protection

```python
# BAD - No CSRF protection
@app.post("/api/settings")
async def update_settings(data: Settings):
    # Anyone can call this endpoint!
    pass

# GOOD - With CSRF protection
@app.post("/api/settings")
async def update_settings(
    data: Settings,
    csrf_token: str = Header(...),
    user: User = Depends(get_current_user)
):
    verify_csrf_token(csrf_token, user.id)
    # ...
```

### 2. Validate All Inputs

```python
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    email: str

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v
```

### 3. Use HTTPS in Production

```javascript
// BAD - HTTP in production
const API_URL = 'http://api.example.com';

// GOOD - HTTPS in production
const API_URL = process.env.NODE_ENV === 'production'
    ? 'https://api.example.com'
    : 'http://localhost:3000';
```

---

## Pre-Commit Checklist

Before committing any code, verify:

### TypeScript/JavaScript
- [ ] `npm run lint` passes
- [ ] `npm run type-check` passes
- [ ] `npm run build` succeeds
- [ ] `npm run test` passes

### Python
- [ ] `flake8` passes
- [ ] `mypy` passes
- [ ] `pytest` passes

### Database
- [ ] Migrations are idempotent
- [ ] Migrations tested locally

### Docker
- [ ] Container builds successfully
- [ ] Container starts correctly

### Git
- [ ] Commit message follows conventions
- [ ] Commit is small and focused
- [ ] No broken code committed

---

## Quick Reference

### Common Commands

```bash
# TypeScript
npm run lint
npm run type-check
npm run build

# Python
flake8 .
mypy .
pytest

# Database
alembic downgrade -1
alembic upgrade head

# Docker
docker-compose up --build
docker ps
docker logs <container_id>

# Git
git add -p  # Stage changes interactively
git commit -m "type: description"
git push
```

---

*Based on analysis of 233 commits and recurring mistakes*

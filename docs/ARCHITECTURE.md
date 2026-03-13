# Architecture Overview

## System Design

The website playground follows a modular architecture with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                        Client (Browser)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Theory    │  │   Problem   │  │      Dashboard      │  │
│  │    Page     │  │    Page     │  │       (Home)        │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          └────────────────┼────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Next.js    │
                    │   (App      │
                    │  Router)    │
                    └──────┬──────┘
                           │ API Calls
                           │
                    ┌──────▼──────┐
                    │   FastAPI   │
                    │   Backend   │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐   ┌─────▼─────┐   ┌──────▼──────┐
    │ PostgreSQL│   │   Redis   │   │   Docker    │
    │   (Data)  │   │  (Cache)  │   │  (Sandbox)  │
    └───────────┘   └───────────┘   └─────────────┘
```

## Content Flow

```
python-oop-journey-v2/           website-playground/
        │                                │
        │  1. Ingest                     │
        └────────► curriculum.ingest ────┤
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │  curriculum.json    │
                              │  (normalized)       │
                              └──────────┬──────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
            ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
            │  Next.js     │    │  FastAPI     │    │  Search      │
            │  (render)    │    │  (API)       │    │  (index)     │
            └──────────────┘    └──────────────┘    └──────────────┘
```

## Key Components

### Frontend (apps/web)
- **Next.js 14** with App Router
- **React Server Components** for theory pages
- **Client Components** for editor/interactive elements
- **Monaco Editor** for code editing
- **Tailwind CSS** for styling
- **Zustand** for client state

### Backend (apps/api)
- **FastAPI** for REST API
- **Pydantic** for validation
- **SQLAlchemy** for ORM
- **PostgreSQL** for persistence
- **Redis** for caching and queues

### Content (packages/curriculum)
- **Ingestion script** parses repo
- **Normalization** creates consistent structure
- **Manifest** (JSON) drives the UI

### Execution (infrastructure/docker)
- **Sandbox containers** run learner code
- **Resource limits** (CPU, memory, time)
- **No network access** for security

## Data Models

### User
```typescript
interface User {
  id: string;
  email: string;
  createdAt: Date;
  progress: Progress[];
  drafts: Draft[];
  bookmarks: Bookmark[];
  notes: Note[];
}
```

### Progress
```typescript
interface Progress {
  id: string;
  userId: string;
  problemSlug: string;
  status: 'started' | 'completed';
  attempts: number;
  lastAttemptAt: Date;
  completedAt?: Date;
}
```

### Draft
```typescript
interface Draft {
  id: string;
  userId: string;
  problemSlug: string;
  code: string;
  savedAt: Date;
}
```

## API Design

### Content Endpoints
```
GET /api/curriculum              # Full curriculum
GET /api/weeks/:slug             # Single week
GET /api/weeks/:slug/days/:day   # Single day
GET /api/problems/:slug          # Single problem
```

### Execution Endpoints
```
POST /api/execute/run            # Run code
POST /api/execute/verify         # Run tests
```

### User Endpoints
```
GET  /api/user/progress          # Get progress
POST /api/user/progress          # Update progress
GET  /api/user/drafts            # Get drafts
POST /api/user/drafts            # Save draft
```

## Security Considerations

1. **Sandbox Isolation**
   - Each execution in fresh container
   - No network access
   - Resource limits enforced
   - Filesystem restricted

2. **Authentication**
   - Magic links (no passwords)
   - JWT tokens
   - Secure cookies

3. **Content Security**
   - User code never executed in main app
   - Input validation on all endpoints
   - Rate limiting

## Scalability

**Current Design:** Single server, suitable for launch

**Future Scaling:**
- Frontend: Static export + CDN
- API: Horizontal scaling with load balancer
- Sandbox: Kubernetes with auto-scaling
- Database: Read replicas

## Deployment

**Development:** Docker Compose
**Production:** VPS with Docker

See `infrastructure/deployment/` for detailed configs.

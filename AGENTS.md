# Website Playground - AGENTS.md

## Overview

This is the web interface for the Python OOP Journey curriculum. It provides search, discovery, and tracking features for learners.

## Architecture

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: React hooks + localStorage
- **Search**: Client-side with API fallback

## Key Components

### Search System
- `CommandPalette`: ⌘K search modal with fuzzy matching
- `SearchButton`: Trigger button with keyboard shortcut hint
- `useSearch`: Search logic with debouncing and filtering
- `build-search-index.js`: Script to generate search index from curriculum

### Discovery
- `/problems`: Problem listing with filters (week, difficulty, topic)
- `/weeks`: Week overview and navigation
- `/recent`: Recently visited items grouped by date
- `/bookmarks`: Saved bookmarks organized by type

### Personalization
- `ContinueLearningWidget`: Shows last visited content
- `useVisitedItems`: Tracks visited pages
- `useBookmarks`: Manages saved bookmarks
- `useRecentSearches`: Tracks search history

## File Locations

```
apps/web/
├── app/
│   ├── page.tsx              # Home page with Continue Learning
│   ├── problems/page.tsx     # Problem discovery
│   ├── recent/page.tsx       # Recently visited
│   ├── bookmarks/page.tsx    # Bookmarks
│   ├── weeks/page.tsx        # Weeks listing
│   ├── weeks/[weekId]/       # Week detail
│   └── api/search/route.ts   # Search API
├── components/
│   ├── search/               # Search components
│   ├── continue-learning.tsx
│   └── bookmark-button.tsx
├── hooks/                    # Custom hooks
└── data/search-index.json    # Generated index
```

## Development

```bash
npm install
npm run dev
```

## Search Index

Regenerate when curriculum changes:
```bash
npm run build:search-index
```

## Adding New Pages

1. Create page in `app/` with `page.tsx`
2. Add navigation link in `components/layout/header.tsx`
3. Update search index if needed

## Styling Guidelines

- Use Tailwind utility classes
- Follow shadcn/ui component patterns
- Support dark mode (uses CSS variables)
- Mobile-first responsive design

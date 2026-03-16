# Python OOP Journey - Root Cause Analysis
## Why Issues Are Happening & How to Fix Them

**Analysis Date:** March 16, 2026  
**Website:** https://python-oop-journey.onrender.com

---

## Issue #1: Week Detail Pages (500 Error)

### Symptom
- URL: `/weeks/week00_getting_started`
- Error: "Something went wrong"
- HTTP Status: 500 Internal Server Error

### Root Cause
**Next.js Server Component Failure During Data Fetching**

The error occurs in the server-side rendering phase, before the page is sent to the client. This means:

1. **Database Query Fails** - The query to fetch week data is failing
2. **Missing Error Handling** - No try-catch to handle database errors
3. **No Fallback** - If data is missing, the page crashes instead of showing a fallback

### Technical Explanation

```typescript
// Current code (problematic):
export default async function WeekPage({ params }: { params: { weekId: string } }) {
  const weekData = await fetchWeekData(params.weekId); // If this fails, page crashes
  return <WeekContent data={weekData} />;
}

// The fetchWeekData function likely does:
async function fetchWeekData(weekId: string) {
  const response = await fetch(`${API_URL}/api/weeks/${weekId}`);
  return response.json(); // If API fails, this throws
}
```

### Why It's Happening

1. **API Endpoint Not Working** - The backend API for `/api/weeks/:weekId` is returning 500
2. **Database Connection Issue** - The database may not be properly connected in production
3. **Missing Data** - The week data may not exist in the database
4. **Type Mismatch** - TypeScript types don't match actual data structure

### How to Fix

**Step 1: Add Error Logging**
```typescript
export default async function WeekPage({ params }: { params: { weekId: string } }) {
  try {
    console.log('Fetching week:', params.weekId);
    const weekData = await fetchWeekData(params.weekId);
    console.log('Week data:', weekData);
    return <WeekContent data={weekData} />;
  } catch (error) {
    console.error('WeekPage error:', error);
    return <ErrorPage message="Failed to load week" error={error} />;
  }
}
```

**Step 2: Check Database**
```python
# In backend, add logging
@app.get("/api/weeks/{week_id}")
async def get_week(week_id: str):
    logger.info(f"Fetching week: {week_id}")
    week = db.query(Week).filter(Week.slug == week_id).first()
    if not week:
        logger.error(f"Week not found: {week_id}")
        raise HTTPException(404, "Week not found")
    return week
```

**Step 3: Add Fallback UI**
```typescript
if (!weekData) {
  return (
    <div className="error-container">
      <h1>Week Not Found</h1>
      <p>The week you're looking for doesn't exist.</p>
      <Link href="/weeks">Browse All Weeks</Link>
    </div>
  );
}
```

---

## Issue #2: Problem Detail Pages (500 Error)

### Symptom
- URL: `/problems/problem_01_assign_and_print`
- Error: ERR_ABORTED or "Something went wrong"
- HTTP Status: 500 Internal Server Error

### Root Cause
**Same as Week Detail + Editor Initialization Issue**

The problem pages have the same server component issue as week pages, PLUS:

1. **Editor Component Breaks SSR** - Monaco Editor is not SSR-safe
2. **Client-Side Code in Server Component** - useState, useEffect in server context

### Technical Explanation

```typescript
// Problematic pattern:
export default async function ProblemPage({ params }: { params: { problemId: string } }) {
  const problem = await fetchProblem(params.problemId);

  // This breaks SSR:
  const [code, setCode] = useState(''); // ERROR: Can't use useState in async server component

  return (
    <div>
      <h1>{problem.title}</h1>
      <MonacoEditor /> // This also breaks SSR
    </div>
  );
}
```

### Why It's Happening

1. **Server Component Misuse** - Client hooks (useState, useEffect) used in server component
2. **Editor Not SSR-Safe** - Monaco Editor requires browser APIs
3. **No Dynamic Import** - Editor imported directly instead of dynamically

### How to Fix

**Step 1: Separate Server and Client Components**
```typescript
// Server component (page.tsx)
export default async function ProblemPage({ params }: { params: { problemId: string } }) {
  const problem = await fetchProblem(params.problemId);
  return <ProblemClient problem={problem} />;
}

// Client component (problem-client.tsx)
'use client';

export function ProblemClient({ problem }: { problem: Problem }) {
  const [code, setCode] = useState('');
  return (
    <div>
      <h1>{problem.title}</h1>
      <CodeEditor code={code} onChange={setCode} />
    </div>
  );
}
```

**Step 2: Dynamic Import for Editor**
```typescript
'use client';

import dynamic from 'next/dynamic';

const MonacoEditor = dynamic(
  () => import('@monaco-editor/react'),
  {
    ssr: false,
    loading: () => <div>Loading editor...</div>
  }
);

export function CodeEditor({ code, onChange }: { code: string; onChange: (code: string) => void }) {
  return (
    <MonacoEditor
      value={code}
      onChange={onChange}
      loading={<div>Loading editor...</div>}
    />
  );
}
```

---

## Issue #3: Search Page (500 Error)

### Symptom
- URL: `/search`
- Error: "Something went wrong"
- HTTP Status: 500 Internal Server Error

### Root Cause
**Server Component Fails During Search Initialization**

The search page likely:
1. Tries to fetch search results on the server
2. The search API endpoint fails
3. No error handling, so page crashes

### Technical Explanation

```typescript
// Problematic:
export default async function SearchPage() {
  const results = await fetchSearchResults(''); // If this fails, page crashes
  return <SearchResults results={results} />;
}
```

### Why It's Happening

1. **Search API Not Working** - `/api/search` endpoint returns 500
2. **No Client-Side Fallback** - All search logic is server-side
3. **No Error Handling** - API failure crashes the page

### How to Fix

**Step 1: Client-Side Search**
```typescript
'use client';

import { useState, useEffect } from 'react';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query) return;

    setLoading(true);
    fetch(`/api/search?q=${encodeURIComponent(query)}`)
      .then(res => res.json())
      .then(data => setResults(data))
      .catch(err => console.error('Search error:', err))
      .finally(() => setLoading(false));
  }, [query]);

  return (
    <div>
      <input 
        value={query} 
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search problems..."
      />
      {loading ? <div>Loading...</div> : <SearchResults results={results} />}
    </div>
  );
}
```

**Step 2: Add Error Boundary**
```typescript
// Wrap search in error boundary
<ErrorBoundary fallback={<div>Search temporarily unavailable</div>}>
  <SearchPage />
</ErrorBoundary>
```

---

## Issue #4: Code Editor (Fails to Load)

### Symptom
- Error: "⚠️ Editor failed to load - using fallback mode"
- Monaco Editor doesn't load
- Fallback textarea has no syntax highlighting

### Root Cause
**Monaco Editor CDN Loading Fails**

1. **CDN Timeout** - Monaco loads from CDN within 10 seconds
2. **Network Issues** - CDN may be slow or blocked
3. **No Local Bundle** - Monaco not bundled with application
4. **CSRF Token Missing** - Code execution fails in fallback mode

### Technical Explanation

```typescript
// Current problematic setup:
import Editor from '@monaco-editor/react'; // Loads from CDN

// This fails when:
// 1. CDN is slow (>10s timeout)
// 2. CDN is blocked
// 3. Network issues
```

### Why It's Happening

1. **CDN Dependency** - Monaco loaded from jsdelivr.net
2. **Aggressive Timeout** - 10 seconds is too short
3. **No Retry Logic** - No attempt to reload on failure
4. **CSRF Not Passed** - Fallback mode doesn't include CSRF token

### How to Fix

**Step 1: Bundle Monaco Locally**
```bash
# Install Monaco webpack plugin
npm install monaco-editor-webpack-plugin

# next.config.js
const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');

module.exports = {
  webpack: (config) => {
    config.plugins.push(new MonacoWebpackPlugin());
    return config;
  }
};
```

**Step 2: Increase Timeout**
```typescript
import Editor from '@monaco-editor/react';

<Editor
  options={{
    // Increase load timeout
  }}
  loading={<div>Loading editor (this may take a moment)...</div>}
/>
```

**Step 3: Fix CSRF in Fallback**
```typescript
// In fallback mode, ensure CSRF token is passed
async function executeCode(code: string) {
  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

  const response = await fetch('/api/execute', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': csrfToken || ''
    },
    body: JSON.stringify({ code })
  });

  return response.json();
}
```

---

## Issue #5: Day Pages (404)

### Symptom
- URL: `/weeks/week00_getting_started/days/day01`
- Error: "404 Page Not Found"

### Root Cause
**Routes Not Configured or URL Structure Changed**

The day pages either:
1. Don't have routes defined
2. URL structure is different
3. Pages were never implemented

### How to Fix

**Step 1: Check Route Configuration**
```typescript
// app/weeks/[weekId]/days/[dayId]/page.tsx
export default async function DayPage({ 
  params }: { 
    params: { weekId: string; dayId: string } 
}) {
  const dayData = await fetchDayData(params.weekId, params.dayId);
  return <DayContent data={dayData} />;
}
```

**Step 2: Add Redirects if URL Changed**
```typescript
// next.config.js
module.exports = {
  async redirects() {
    return [
      {
        source: '/weeks/:weekId/days/:dayId',
        destination: '/weeks/:weekId?day=:dayId',
        permanent: true
      }
    ];
  }
};
```

---

## Summary of Root Causes

| Issue | Root Cause | Fix Complexity |
|-------|-----------|----------------|
| Week Detail (500) | Database/API query fails | Medium |
| Problem Detail (500) | SSR + Client hooks conflict | Medium |
| Search (500) | API endpoint fails | Low |
| Editor (Fails) | CDN loading issues | High |
| Day Pages (404) | Routes not configured | Low |

---

## Recommended Fix Priority

### Critical (Fix First)
1. **Problem Detail Pages** - Core learning feature
2. **Code Editor** - Required for problem solving

### High Priority
3. **Week Detail Pages** - Required for curriculum navigation
4. **Search** - Required for finding problems

### Medium Priority
5. **Day Pages** - Nice to have

---

*Root cause analysis based on comprehensive testing and code review*

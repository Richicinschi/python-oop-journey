# Python OOP Journey - Website Playground

Interactive web interface for the Python OOP Journey curriculum with search, discovery, and tracking features.

## Features

### 🔍 Search & Discovery
- **Command Palette** (⌘K): Fast fuzzy search across weeks, days, problems, and topics
- **Problem Discovery Page**: Browse all 450+ problems with filters and sorting
- **Smart Results**: Results ranked by relevance with highlighted matches
- **Recent Searches**: Auto-saves recent searches for quick access

### 📚 Content Organization
- **Weeks Overview**: Visual curriculum navigation
- **Problem Cards**: Grid/list view with difficulty badges and topic tags
- **Topic Pages**: Browse by topic (classes, inheritance, lists, etc.)

### 👤 Personalization
- **Continue Learning**: Quick resume of last visited content
- **Recently Visited**: History grouped by time (Today, Yesterday, This Week)
- **Bookmarks**: Save favorite problems, days, or weeks

### ⌨️ Keyboard Shortcuts
| Key | Action |
|-----|--------|
| ⌘K | Open search |
| / | Open search |
| ↑↓ | Navigate results |
| ↵ | Select |
| Esc | Close |

## Project Structure

```
apps/web/
├── app/
│   ├── api/search/        # Search API endpoint
│   ├── bookmarks/         # Bookmarks page
│   ├── problems/          # Problem discovery page
│   ├── recent/            # Recently visited page
│   ├── weeks/             # Weeks listing and detail
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── template.tsx       # Client layout wrapper
├── components/
│   ├── search/            # Search components
│   ├── ui/                # shadcn/ui components
│   ├── bookmark-button.tsx
│   ├── continue-learning.tsx
│   └── layout/
├── data/
│   └── search-index.json  # Generated search index
├── hooks/
│   ├── use-bookmarks.ts
│   ├── use-local-storage.ts
│   ├── use-recent-searches.ts
│   ├── use-search.ts
│   └── use-visited-items.ts
└── lib/
    ├── search.ts          # Search utilities
    └── utils.ts           # Helper functions
```

## Technologies

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui, Radix UI
- **Search**: Fuse.js compatible (with custom implementation)
- **Icons**: Lucide React

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build search index
npm run build:search-index

# Build for production
npm run build
```

## Search Index Generation

The search index is generated from the curriculum data:

```bash
node scripts/build-search-index.js
```

This scans `python-oop-journey-v2/` and creates `apps/web/data/search-index.json` with:
- Week metadata
- Day metadata
- Problem metadata (with extracted topics, keywords, difficulty)
- Topic entries

## API Endpoints

### GET /api/search

Search the curriculum with filters.

**Query Parameters:**
- `q` - Search query
- `week` - Filter by week number
- `difficulty` - Filter by difficulty
- `topic` - Filter by topic
- `type` - Filter by type (week, day, problem, topic)
- `limit` - Max results (default: 20)

**Response:**
```json
{
  "results": [...],
  "total": 42,
  "query": "class",
  "filters": {},
  "searchTime": 15
}
```

## Local Storage Keys

- `recent-searches` - Recent search queries
- `visited-items` - Recently visited content
- `bookmarks` - User bookmarks

## Future Enhancements

- [ ] Progress tracking (completed problems)
- [ ] User authentication
- [ ] Server-side bookmarks
- [ ] Problem difficulty visualization
- [ ] Spaced repetition suggestions
- [ ] Achievement system

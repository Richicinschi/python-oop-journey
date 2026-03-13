# Curriculum Ingestion Package

Parses the `python-oop-journey-v2` repository and creates a normalized manifest for the web platform.

## Usage

```bash
# Ingest curriculum from repo
python -m curriculum.ingest --source ../python-oop-journey-v2 --output ./data/curriculum.json

# Watch for changes (development)
python -m curriculum.ingest --source ../python-oop-journey-v2 --output ./data/curriculum.json --watch
```

## Manifest Structure

The ingestion process creates a normalized JSON manifest:

```json
{
  "version": "2.0.0",
  "weeks": [
    {
      "slug": "week00_getting_started",
      "title": "Week 0: Getting Started with Python",
      "order": 0,
      "objective": "Learn Python basics...",
      "prerequisites": [],
      "days": [...],
      "project": {...}
    }
  ]
}
```

## Content Model

### Week
- `slug`: URL-friendly identifier
- `title`: Display title
- `order`: Sequence number
- `objective`: Learning objective
- `prerequisites`: List of required prior knowledge
- `days`: Array of Day objects
- `project`: Weekly project metadata

### Day
- `slug`: URL-friendly identifier
- `title`: Display title
- `order`: Day number (1-6, or 0-30 for Week 0)
- `theory`: Theory document metadata
- `problems`: Array of Problem objects
- `learning_objectives`: List of objectives

### Problem
- `slug`: URL-friendly identifier
- `title`: Display title
- `topic`: Topic tag
- `difficulty`: Easy | Medium | Hard
- `order`: Problem sequence
- `instructions`: Rendered markdown
- `starter_code`: Initial code
- `solution_code`: Reference solution
- `test_code`: Test harness
- `hints`: Array of hint strings

## Extension Points

To support new content types:

1. Add parser in `parsers/` directory
2. Register in `ingest.py`
3. Update TypeScript types in `packages/shared/types/`

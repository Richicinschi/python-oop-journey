# Project Page

The Project Page provides a three-pane IDE-like interface for working on weekly capstone projects.

## Features

### Three-Pane Layout (Desktop)

```
┌──────────────┬──────────────────────┬──────────────┐
│  File Tree   │  Editor (Monaco)     │ Instructions │
│  📁 src      │  ┌─────┬─────┐       │ - Overview   │
│   📄 main.py │  │file1│file2│       │ - Tasks      │
│   📄 utils.py│  └─────┴─────┘       │ - Hints      │
│  📁 tests    │  [Toolbar]           │ - Submit     │
│   📄 ...     │                      │              │
├──────────────┼──────────────────────┤              │
│  [+ New]     │  Output/Terminal     │              │
│              │  > python main.py    │              │
└──────────────┴──────────────────────┴──────────────┘
```

### Mobile Layout
- Collapsible file tree (left sheet)
- Full-screen editor
- Collapsible instructions (right sheet)
- Bottom navigation bar

### File Tree Panel
- Hierarchical file explorer
- Expand/collapse directories
- Create new files
- Delete files (with confirmation)
- Right-click context menu
- Entry point badge on main.py
- Read-only indicators

### Editor Panel
- Monaco Editor with Python syntax highlighting
- Multiple file support
- File tabs (when multiple files open)
- Toolbar with:
  - Save button (Ctrl+S)
  - Run button (Ctrl+Enter)
  - Test button
  - Reset button
- Unsaved changes indicator
- Entry point marker

### Instructions Panel
- Week badge and project title
- Overview/description
- Task checklist with:
  - Interactive checkboxes
  - Auto-check when tests pass
  - Progress bar
- Requirements list
- Progressive hints
- Submission guidelines
- Navigation buttons

### Terminal/Output Panel
- Resizable bottom panel
- Two tabs:
  - Terminal: Shows execution output
  - Tests: Shows test results with pass/fail status
- Clear button
- Execution time display

### Project Status Tracking
- Not Started
- In Progress (% complete)
- Submitted
- Completed

### Data Persistence
- Auto-save to localStorage
- File contents saved per project
- Task completion state saved
- Project status saved

## Project Data Format

Projects in `curriculum.json` support extended fields:

```json
{
  "slug": "week01_project",
  "title": "Week 1 Project: Shopping Cart",
  "description": "...",
  "overview": "Build a shopping cart system...",
  "entryPoint": "src/main.py",
  "files": [
    {
      "path": "src/main.py",
      "content": "...",
      "isEntryPoint": true
    },
    {
      "path": "src/cart.py",
      "content": "..."
    },
    {
      "path": "tests/test_cart.py",
      "content": "...",
      "readOnly": false
    }
  ],
  "tasks": [
    {
      "id": "task-1",
      "description": "Implement add_item method",
      "hint": "Use a list to store items"
    }
  ],
  "requirements": [
    "Use OOP principles",
    "Write tests for all methods"
  ],
  "hints": [
    "Consider using a dictionary for item lookup"
  ],
  "submissionGuidelines": "Submit when all tests pass"
}
```

## API Endpoints

### GET /api/projects/:slug
Load project data from curriculum.

### POST /api/projects/:slug/save
Save project state (currently client-side only).

### POST /api/projects/:slug/run
Execute project code (mock implementation).

### POST /api/projects/:slug/test
Run project tests (mock implementation).

### POST /api/projects/:slug/submit
Submit project for review.

## Testing Steps

1. Navigate to a week page with a project (e.g., Week 7)
2. Click "Start Project" on the project card
3. Verify:
   - File tree loads with correct structure
   - Entry point file (main.py) opens automatically
   - Instructions panel shows tasks
   - Can create new files
   - Can edit and save files
   - Can run code and see output
   - Can run tests and see results
   - Can check off tasks
   - Progress bar updates
   - Can submit when all tasks complete

## Keyboard Shortcuts

- `Ctrl+S`: Save current file
- `Ctrl+Enter`: Run code
- `Ctrl+Shift+Enter`: Run tests

## Future Enhancements

- Real code execution (Python runner service)
- Real-time collaboration
- Code review system
- Export to GitHub Gist
- Download as ZIP
- Share project URL (read-only)

# Day 30: Final Project - Todo List CLI Application

## Learning Objectives

By the end of this day, you will:
- Build a complete CLI application from scratch
- Apply functions, conditionals, and loops in a real project
- Implement file I/O for data persistence
- Practice error handling throughout the application
- Structure code into logical modules
- Write comprehensive tests for your application

---

## Project Overview

Build a **command-line Todo List application** that allows users to:
- Add, view, complete, and delete tasks
- Organize tasks with priorities (high, medium, low)
- Save tasks to a file for persistence
- Load tasks from a file on startup
- Search and filter tasks

---

## Requirements

### Core Features

1. **Add Tasks**
   - Task description (required)
   - Priority: high, medium, low (default: medium)
   - Due date (optional)

2. **View Tasks**
   - List all tasks
   - Filter by status (completed/pending)
   - Filter by priority
   - Sort by due date or priority

3. **Complete Tasks**
   - Mark tasks as completed
   - View completion date

4. **Delete Tasks**
   - Remove individual tasks
   - Clear all completed tasks

5. **Data Persistence**
   - Save to JSON file automatically
   - Load from JSON file on startup

### Error Handling

- Invalid input handling
- File I/O error handling
- Data validation
- Graceful error messages

---

## Project Structure

```
project/
├── README.md           # Project documentation
├── starter/            # Starter code for learners
│   ├── __init__.py
│   ├── task.py         # Task data model
│   ├── storage.py      # File I/O operations
│   ├── manager.py      # Task management logic
│   └── cli.py          # Command-line interface
├── reference_solution/ # Complete implementation
│   ├── __init__.py
│   ├── task.py
│   ├── storage.py
│   ├── manager.py
│   └── cli.py
└── tests/              # Test suite
    ├── __init__.py
    └── test_todo.py
```

---

## Data Model

### Task Structure

```python
{
    "id": int,           # Unique identifier
    "description": str,  # Task description
    "priority": str,     # "high", "medium", or "low"
    "due_date": str,     # ISO format date or None
    "completed": bool,   # Completion status
    "created_at": str,   # ISO format timestamp
    "completed_at": str  # ISO format timestamp or None
}
```

---

## CLI Commands

```
Usage: python cli.py [command] [options]

Commands:
    add "description" [--priority high|medium|low] [--due-date YYYY-MM-DD]
    list [--all|--completed|--pending] [--sort date|priority]
    complete <task_id>
    delete <task_id>
    clear-completed
    search <query>
    help
```

---

## Implementation Guide

### Step 1: Task Model (task.py)

Create the Task class/data structure with:
- Properties for all task fields
- Validation methods
- String representation
- JSON serialization/deserialization

### Step 2: Storage Module (storage.py)

Implement file operations:
- `load_tasks(filepath)`: Load tasks from JSON
- `save_tasks(tasks, filepath)`: Save tasks to JSON
- Error handling for file operations

### Step 3: Task Manager (manager.py)

Implement business logic:
- `add_task()`: Create and add new tasks
- `get_tasks()`: Retrieve tasks with filtering
- `complete_task()`: Mark task as done
- `delete_task()`: Remove task by ID
- `search_tasks()`: Find tasks by description

### Step 4: CLI Interface (cli.py)

Implement the user interface:
- Command parsing
- User interaction loops
- Display formatting
- Help text

---

## Testing Strategy

Write tests for:
1. Task creation and validation
2. File I/O operations
3. Task management operations
4. Search and filter functionality
5. Edge cases and error handling

Minimum 30 tests covering:
- Unit tests for each function
- Integration tests for workflows
- Error case tests

---

## Stretch Goals

If you finish early, add these features:
- Categories/tags for tasks
- Task statistics and reporting
- Export to CSV
- Recurring tasks
- Due date reminders

---

## Project Connection to Week 0 Lessons

This final project brings together everything you've learned:

| Week 0 Topic | How It Applies to the Project |
|--------------|-------------------------------|
| **Variables & Types** | Store task data (strings, ints, booleans) |
| **Collections** | Use lists to store tasks, dicts for task data |
| **Control Flow** | if/else for menu choices, loops for task iteration |
| **Functions** | Organize code into reusable functions |
| **File I/O** | Save/load tasks from JSON for persistence |
| **Error Handling** | Handle invalid input, missing files gracefully |
| **Modules** | Separate code into task.py, storage.py, manager.py, cli.py |
| **Debugging** | Use print statements and tracebacks to fix issues |

---

## Tips for Success

1. **Start small**: Get basic task creation working first
2. **Test frequently**: Run tests after each feature
3. **Handle errors**: Don't forget edge cases
4. **Keep it simple**: Clear code beats clever code
5. **Use type hints**: They help catch bugs early

---

## Evaluation Criteria

Your project should demonstrate:
- [ ] All core features working
- [ ] Proper error handling
- [ ] Type hints throughout
- [ ] Clear docstrings
- [ ] At least 30 passing tests
- [ ] Clean, readable code

Good luck, and happy coding!

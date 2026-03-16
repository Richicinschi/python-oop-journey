# Week 00 Project: Todo List CLI Application

## What is the Goal?

Build a complete command-line todo list application that brings together everything you've learned in Week 00:

- **Variables and data types** - Storing task information
- **Control flow** - Filtering, searching, and managing tasks
- **Data structures** - Lists and dictionaries for task storage
- **Functions** - Modular code organization
- **File I/O** - Persistent storage with JSON
- **Error handling** - Graceful handling of invalid input
- **Modules** - Separating concerns across multiple files

By the end of this project, you will have a fully functional CLI tool you can actually use to manage your tasks.

---

## Which Files Matter Most?

### For Learners (Start Here)

```
project/
├── starter/                    # Your starting point
│   ├── task.py                 # Step 1: Task data model
│   ├── storage.py              # Step 2: File I/O operations
│   ├── manager.py              # Step 3: Business logic
│   └── cli.py                  # Step 4: Command-line interface
```

### For Reference

```
project/
├── reference_solution/         # Complete working implementation
│   ├── task.py                 # Task class with validation
│   ├── storage.py              # JSON load/save functions
│   ├── manager.py              # TaskManager class
│   └── cli.py                  # CLI with argparse
```

### For Testing

```
project/
└── tests/
    └── test_todo.py            # 44 tests covering all functionality
```

---

## What is the Public Contract?

### Task Data Model (`task.py`)

Each task has these properties:
- `id` (int): Unique identifier
- `description` (str): Task description text
- `priority` (str): "high", "medium", or "low"
- `due_date` (str|None): ISO format date (YYYY-MM-DD)
- `completed` (bool): Completion status
- `created_at` (str): ISO timestamp
- `completed_at` (str|None): ISO timestamp when completed

**Validation Rules:**
- Description cannot be empty or whitespace-only
- Priority must be "high", "medium", or "low" (case-insensitive)

### Storage Module (`storage.py`)

```python
def load_tasks(filepath: str) -> List[Task]:
    """Load tasks from JSON file. Returns empty list if file doesn't exist."""
    
def save_tasks(tasks: List[Task], filepath: str) -> bool:
    """Save tasks to JSON file. Returns True if successful."""
```

### Task Manager (`manager.py`)

```python
class TaskManager:
    def __init__(self, filepath: str = "tasks.json"): ...
    def add_task(self, description, priority="medium", due_date=None) -> Task: ...
    def get_tasks(self, completed=None, priority=None, sort_by="id") -> List[Task]: ...
    def get_task_by_id(self, task_id: int) -> Task | None: ...
    def complete_task(self, task_id: int) -> bool: ...
    def delete_task(self, task_id: int) -> bool: ...
    def clear_completed(self) -> int: ...  # Returns count removed
    def search_tasks(self, query: str) -> List[Task]: ...
    def get_stats(self) -> dict: ...
```

### CLI Commands

```bash
# Add a task
python -m starter.cli add "Buy groceries" --priority high --due-date 2026-03-15

# List tasks
python -m starter.cli list                    # All tasks
python -m starter.cli list --pending          # Only pending
python -m starter.cli list --completed        # Only completed
python -m starter.cli list --sort priority    # Sort by priority

# Complete a task
python -m starter.cli complete 1

# Delete a task
python -m starter.cli delete 1

# Clear all completed
python -m starter.cli clear-completed

# Search tasks
python -m starter.cli search "groceries"
```

---

## How Should the Learner Approach the Starter?

### Recommended Implementation Order

Follow this order. Each file builds on the previous one:

#### Step 1: Task Model (`starter/task.py`)

**Start here.** The Task class is the foundation.

1. Implement `__init__` with validation:
   - Strip whitespace from description
   - Validate priority is one of VALID_PRIORITIES
   - Auto-generate `created_at` timestamp if not provided

2. Implement `to_dict()` for JSON serialization

3. Implement `from_dict()` class method for deserialization

4. Implement `mark_completed()` to set completion status and timestamp

5. Implement `__str__()` and `__repr__()` for display

**Validation Requirements:**
```python
# Should raise ValueError
task = Task(1, "")           # Empty description
task = Task(1, "   ")        # Whitespace-only
task = Task(1, "Test", priority="invalid")  # Invalid priority

# Should work (case-insensitive priority)
task = Task(1, "Test", priority="HIGH")
assert task.priority == "high"
```

#### Step 2: Storage Module (`starter/storage.py`)

**Next**, implement file persistence.

1. Implement `ensure_directory_exists()`:
   - Create parent directories if they don't exist
   - Use `os.path.dirname()` and `os.makedirs()`

2. Implement `load_tasks()`:
   - Return empty list if file doesn't exist
   - Parse JSON and convert dictionaries to Task objects using `Task.from_dict()`
   - Handle invalid JSON by raising `json.JSONDecodeError`

3. Implement `save_tasks()`:
   - Convert Task objects to dictionaries using `task.to_dict()`
   - Write pretty-printed JSON (use `indent=2`)
   - Return True on success, False on failure

#### Step 3: Task Manager (`starter/manager.py`)

**Then**, implement business logic.

1. Implement `__init__`:
   - Load existing tasks from file
   - Calculate next available ID

2. Implement `_calculate_next_id()`:
   - Return 1 if no tasks
   - Otherwise return max ID + 1

3. Implement `add_task()`:
   - Create Task with next_id
   - Append to tasks list
   - Call `save()`
   - Increment next_id

4. Implement `get_tasks()` with filtering and sorting:
   - Filter by completed status (True/False/None for all)
   - Filter by priority
   - Sort by: "id", "priority", "due_date", "created_at"

5. Implement `complete_task()` and `delete_task()`:
   - Find task by ID
   - Return True if found and modified, False otherwise
   - Call `save()` after modification

6. Implement `search_tasks()`:
   - Case-insensitive search in description

7. Implement `get_stats()`:
   - Return dict with total, completed, pending, by_priority

#### Step 4: CLI (`starter/cli.py`)

**Finally**, wire everything together.

1. Implement `format_task()`:
   - Show status indicator ([✓] or [ ])
   - Show task ID
   - Show description
   - Show priority indicator
   - Show due date if present

2. Implement `print_tasks()`:
   - Print title
   - Handle empty list gracefully
   - Print each formatted task

3. Implement command handlers (`cmd_add`, `cmd_list`, etc.):
   - Convert argparse args to manager calls
   - Print appropriate messages
   - Return exit codes (0 for success, 1 for error)

4. Implement `create_parser()`:
   - Use `argparse.ArgumentParser`
   - Add subparsers for each command
   - Configure arguments for each command

5. Implement `main()`:
   - Parse arguments
   - Create TaskManager
   - Dispatch to appropriate command handler

---

## What Should the Final Behavior Look Like?

### Example Session

```bash
# Add some tasks
$ python -m starter.cli add "Buy groceries" --priority high --due-date 2026-03-15
Added task: [ ] #1: Buy groceries [HIGH] (Due: 2026-03-15)

$ python -m starter.cli add "Call mom"
Added task: [ ] #2: Call mom

$ python -m starter.cli add "Finish project" --priority high
Added task: [ ] #3: Finish project [HIGH]

# List all tasks
$ python -m starter.cli list

=== Tasks ===
[ ] #1: Buy groceries [HIGH] (Due: 2026-03-15)
[ ] #2: Call mom
[ ] #3: Finish project [HIGH]

Total: 3 | Completed: 0 | Pending: 3

# Complete a task
$ python -m starter.cli complete 2
Task #2 marked as completed.

# List pending only
$ python -m starter.cli list --pending

=== Tasks (Pending) ===
[ ] #1: Buy groceries [HIGH] (Due: 2026-03-15)
[ ] #3: Finish project [HIGH]

Total: 3 | Completed: 1 | Pending: 2

# Search tasks
$ python -m starter.cli search "project"

=== Search results for "project" ===
[ ] #3: Finish project [HIGH]

# Clear completed
$ python -m starter.cli clear-completed
Cleared 1 completed task(s).
```

### Data Persistence

Tasks are automatically saved to `tasks.json`:

```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "priority": "high",
    "due_date": "2026-03-15",
    "completed": false,
    "created_at": "2026-03-12T10:30:00.000000",
    "completed_at": null
  }
]
```

---

## How Does This Project Connect to the Daily Lessons?

### Day 28: Modules and Imports

The project structure directly applies Day 28 concepts:

- **Separate modules for separate concerns**: 
  - `task.py` - Data model (what a task IS)
  - `storage.py` - File operations (how tasks are saved)
  - `manager.py` - Business logic (what you can DO with tasks)
  - `cli.py` - User interface (how users INTERACT)

- **Import patterns in use**:
  ```python
  from .task import Task              # Import class
  from .storage import load_tasks     # Import function
  from .manager import TaskManager    # Import for CLI
  ```

- **`__main__` guard pattern**:
  ```python
  if __name__ == "__main__":
      sys.exit(main())
  ```
  This lets you run `python -m starter.cli` while also importing the module.

### Week 00 Review: All Concepts Combined

| Week 00 Concept | Where It Appears in Project |
|-----------------|------------------------------|
| Variables | Task attributes, function parameters |
| Data types | `int` (id), `str` (description), `bool` (completed) |
| Lists | `tasks` list in manager, filtering results |
| Dictionaries | JSON serialization, `get_stats()` return |
| Functions | Every module has focused functions |
| Conditionals | Validation logic, filtering |
| Loops | Iterating tasks for search/filter |
| File I/O | `storage.py` read/write JSON |
| Error handling | Try/except in storage, validation in Task |
| Modules | Four separate module files |

---

## Running Commands

### Running the Reference Solution

```bash
cd week00_getting_started/project

# Add a task
python -m reference_solution.cli add "Test task" --priority high

# List tasks
python -m reference_solution.cli list
```

### Running Your Implementation

```bash
cd week00_getting_started/project

# Add a task
python -m starter.cli add "Test task" --priority high

# List tasks
python -m starter.cli list
```

### Running the Tests

```bash
# From repository root
pytest week00_getting_started/project/tests/ -v

# Run specific test categories
pytest week00_getting_started/project/tests/test_todo.py::test_task_creation_basic -v
pytest week00_getting_started/project/tests/test_todo.py -k "task_" -v
pytest week00_getting_started/project/tests/test_todo.py -k "manager_" -v
pytest week00_getting_started/project/tests/test_todo.py -k "cli_" -v
```

---

## Verification Checklist

Before calling the project complete, verify:

- [ ] `python -m pytest week00_getting_started/project/tests/ -v` passes all 44 tests
- [ ] `python -m starter.cli add "Test"` works and creates `tasks.json`
- [ ] `python -m starter.cli list` displays tasks
- [ ] `python -m starter.cli complete 1` marks task complete
- [ ] `python -m starter.cli search "test"` finds matching tasks
- [ ] `python -m starter.cli clear-completed` removes completed tasks
- [ ] Empty description raises ValueError
- [ ] Invalid priority raises ValueError
- [ ] Data persists after restarting the CLI
- [ ] All type hints are present
- [ ] All functions have docstrings

---

## Common Pitfalls

### Task ID Management

**Pitfall**: Resetting IDs to 1 when loading from file.
```python
# WRONG - loses track of existing IDs
self.next_id = 1  # Don't do this!

# CORRECT - calculate from existing tasks
self.next_id = self._calculate_next_id()
```

### File Path Handling

**Pitfall**: Not creating directories before saving.
```python
# WRONG - fails if directory doesn't exist
with open(filepath, "w") as f:  # May fail!

# CORRECT - ensure directory exists first
ensure_directory_exists(filepath)
with open(filepath, "w") as f:
```

### Case Sensitivity

**Pitfall**: Priority comparison failing due to case.
```python
# WRONG - "HIGH" != "high"
if task.priority == priority:  # Case-sensitive!

# CORRECT - normalize to lowercase
task = Task(1, "Test", priority="HIGH")  # Stored as "high"
```

### Mutable Default Arguments

**Pitfall**: Using lists or dicts as default arguments.
```python
# WRONG - shared mutable default
def func(items=[]):  # Don't do this!

# CORRECT - use None as default
def func(items: list | None = None):
    if items is None:
        items = []
```

---

## Tips for Success

1. **Implement one module at a time** - Get `task.py` working before moving to `storage.py`
2. **Test incrementally** - Run tests after each function you implement
3. **Read the reference solution** - Look at it when stuck, but try to understand rather than copy
4. **Use the Python REPL** - Test small pieces of code interactively
5. **Check JSON output** - Open `tasks.json` to verify data is saved correctly

---

## Project Files Summary

| File | Purpose | Lines in Reference |
|------|---------|-------------------|
| `task.py` | Data model with validation | ~124 |
| `storage.py` | JSON file I/O | ~75 |
| `manager.py` | Business logic | ~213 |
| `cli.py` | Command-line interface | ~275 |
| `test_todo.py` | 44 comprehensive tests | ~502 |

---

**Good luck with your Todo List CLI application!**

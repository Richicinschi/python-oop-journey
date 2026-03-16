# Week 5 Project: Task Management System

## Goal

Build a professional task management system that demonstrates mastery of advanced Python OOP features. This is the **capstone project** for Week 5, bringing together descriptors, decorators, context managers, and clean domain architecture.

By completing this project, you will:
- Use **descriptors** to create self-validating model attributes
- Apply **decorators** for cross-cutting concerns (logging, validation, timing)
- Implement **context managers** for atomic, transactional operations
- Design clean domain models with proper encapsulation
- Create extensible role-based access control
- Build status workflows with enforced state transitions

---

## Files That Matter Most

```
project/
├── README.md                      # This file (start here)
├── starter/                       # Your working area - start here
│   ├── decorators.py             # TODO: Implement 7 decorators
│   ├── user.py                   # TODO: Implement User with descriptors
│   ├── task.py                   # TODO: Implement Task with descriptors
│   ├── project.py                # TODO: Implement Project container
│   └── storage.py                # TODO: Implement persistence layer
├── reference_solution/            # Complete working implementation
│   ├── decorators.py             # Reference: all decorators
│   ├── user.py                   # Reference: descriptors, permissions
│   ├── task.py                   # Reference: descriptors, workflows
│   ├── project.py                # Reference: project management
│   └── storage.py                # Reference: transactions
└── tests/
    └── test_task_system.py       # 84 tests - your verification
```

**Where to start:** Open `starter/decorators.py` first - it has the clearest TODOs and warms you up for the descriptor work in `user.py` and `task.py`.

---

## Public Contract

Your implementation must satisfy this public API contract:

### Decorators (`decorators.py`)
```python
@log_operation              # Prints: [LOG] func_name(args) -> result
@timing_decorator           # Prints: [TIMING] func_name took X.XXX seconds
@require_permission("CREATE_TASK")  # Raises PermissionError if denied
@validate_types(name=str, age=int)  # Raises TypeError on mismatch
@singleton                  # Class becomes singleton
@retry_on_error(max_attempts=3)     # Retries on failure
@deprecated("Use new_func")  # Emits DeprecationWarning
@count_calls                # Adds .call_count attribute
```

### User Model (`user.py`)
```python
user = User("alice", "alice@example.com", Role.MANAGER)
user.username              # Validated: 3-30 chars, alphanumeric+underscore
user.email                 # Validated: must contain @ and domain
user.has_permission(Permission.CREATE_TASK)  # True/False by role
user.to_dict()             # {"username": "...", "email": "...", "role": "..."}
User.from_dict(data)       # Deserialize user
```

### Task Model (`task.py`)
```python
task = Task("Title", priority=Priority.HIGH, deadline="2024-12-31")
task.title                 # Validated: 3-100 chars, required
task.description           # Validated: max 1000 chars, optional
task.priority              # Validated: Priority enum
task.status                # Validated: Status enum, workflow enforced
task.deadline              # Validated: datetime or ISO string
task.assign_to(user)       # Set assignee
task.transition_to(Status.IN_PROGRESS)  # Raises ValueError if invalid
task.start_progress()      # Shortcut: BACKLOG/TODO -> IN_PROGRESS
task.complete()            # Shortcut to DONE (via REVIEW if CRITICAL)
task.cancel()              # To CANCELLED (not from terminal states)
task.is_overdue()          # True if past deadline and not done
```

### Project Model (`project.py`)
```python
project = Project("Name", "Description", owner=admin)
project.project_id         # Unique identifier
project.add_member(user, Role.MANAGER)
project.remove_member(user)  # Unassigns their tasks too
project.add_task(task)
project.get_task(task_id)  # Get by ID or None
project.get_tasks_by_status(Status.TODO)
project.get_overdue_tasks()
project.get_statistics()   # {"total_tasks": N, "by_status": {...}, ...}
project.activate()         # Status -> ACTIVE
project.to_dict()          # Serialize for storage
Project.from_dict(data, users)  # Deserialize
```

### Storage (`storage.py`)
```python
storage = Storage("data/tasks.json")
storage.save(projects, users)    # Atomic write
storage.load()                   # Returns (projects, users)
storage.load_or_init()           # Returns empty if no file

with storage.transaction() as txn:
    txn.save_project(project)    # Queued for save
    txn.save_user(user)
    txn.delete_project(id)
    # Auto-committed on success
    # Auto-rolled-back on exception
```

---

## How to Approach the Starter

### Recommended Order

1. **Start with `decorators.py`** (Warm-up, 30-45 min)
   - Implement `log_operation` first - it's the simplest
   - Then `timing_decorator` - similar structure
   - Save `require_permission` for last - needs the User model
   - Run tests after each: `pytest tests/test_task_system.py::TestLogOperationDecorator -v`

2. **Build `user.py`** (Descriptors practice, 45-60 min)
   - Implement `ValidatedEmail` descriptor first
   - Then `ValidatedUsername` descriptor
   - Finish with `User` class using your descriptors
   - Key insight: descriptors validate on `__set__`, store in private attribute

3. **Implement `task.py`** (Complex descriptors, 60-90 min)
   - Reuse `ValidatedString` pattern from user.py
   - Implement `ValidatedChoice` for Priority/Status
   - Implement `ValidatedDatetime` (accepts string or datetime)
   - Status workflow: check `VALID_TRANSITIONS` dict before allowing changes

4. **Create `project.py`** (Integration, 45-60 min)
   - Straightforward collection management
   - Track members in dict: `{user: role}`
   - Track tasks in dict: `{task_id: task}`
   - Handle edge case: removing member unassigns their tasks

5. **Finish with `storage.py`** (Context managers, 45-60 min)
   - Implement atomic save: write to temp, then rename
   - Transaction uses `@contextmanager` decorator
   - On success: save changes; on exception: don't save (rollback)

### Testing as You Go

```bash
# Test just the decorators
pytest week05_oop_advanced/project/tests/test_task_system.py -k "Decorator" -v

# Test just user functionality
pytest week05_oop_advanced/project/tests/test_task_system.py -k "User" -v

# Test just task functionality
pytest week05_oop_advanced/project/tests/test_task_system.py -k "Task" -v

# Test everything
pytest week05_oop_advanced/project/tests/ -v
```

### When You're Stuck

1. **Look at the reference solution** for the file you're working on
2. **Read the tests** - they show expected behavior
3. **Check the week README** - days 1-3 cover the concepts used here

---

## What Final Behavior Looks Like

### Complete Example

```python
from starter.user import User, Role, Permission
from starter.task import Task, Priority, Status
from starter.project import Project
from starter.storage import Storage

# Create users with validated emails
admin = User("admin", "admin@example.com", Role.ADMIN)
manager = User("mgr", "manager@example.com", Role.MANAGER)
member = User("alice", "alice@example.com", Role.MEMBER)

# Verify permissions work
assert admin.has_permission(Permission.DELETE_PROJECT)
assert manager.has_permission(Permission.ASSIGN_TASK)
assert not member.has_permission(Permission.ASSIGN_TASK)

# Create a project
project = Project("Website Redesign", "Q4 website overhaul", owner=admin)
project.add_member(manager, Role.MANAGER)
project.add_member(member, Role.MEMBER)

# Create tasks with descriptor validation
task1 = Task(
    title="Update homepage",
    description="Redesign landing page with new branding",
    priority=Priority.HIGH,
    deadline="2024-12-31"
)
task1.add_tag("urgent")
task1.add_tag("design")

# Status workflow enforcement
task1.start_progress()        # BACKLOG -> TODO -> IN_PROGRESS
assert task1.status == Status.IN_PROGRESS

task1.transition_to(Status.REVIEW)
task1.complete()              # REVIEW -> DONE
assert task1.status == Status.DONE

# Critical tasks must go through REVIEW
critical = Task("Security audit", priority=Priority.CRITICAL)
critical.start_progress()     # IN_PROGRESS
critical.complete()           # Goes to REVIEW first
assert critical.status == Status.REVIEW
critical.complete()           # Now to DONE
assert critical.status == Status.DONE

# Assign and track
task1.assign_to(member)
project.add_task(task1)
assert task1 in project.get_tasks_for_user(member)

# Persist with transaction safety
storage = Storage("data/tasks.json")
with storage.transaction() as txn:
    txn.save_project(project)
    txn.save_user(admin)
    txn.save_user(manager)
    txn.save_user(member)
# Data saved atomically only if no exception raised

# Load back
projects, users = storage.load()
print(f"Loaded {len(projects)} projects with {len(users)} users")
```

### Expected Test Results

When complete, all 84 tests pass:
```
pytest week05_oop_advanced/project/tests/ -v
# =========================== 84 passed in ~0.5s ===========================
```

---

## Connection to Daily Lessons

This project reinforces concepts from **all 6 days** of Week 5:

### Day 1: Descriptors
- **`ValidatedString`** in `task.py` - Custom descriptor with `__get__`, `__set__`, `__set_name__`
- **`ValidatedEmail`** in `user.py` - Descriptor with validation logic
- **`ValidatedChoice`** - Enum validation via descriptor protocol
- **Learning focus:** Descriptors intercept attribute access for validation

### Day 2: Metaclasses (Optional Enhancement)
- The reference solution uses standard classes, but you could:
  - Add a metaclass to auto-register Task subclasses
  - Use `__init_subclass__` for plugin-style task types
- **Learning focus:** Metaclasses control class creation (advanced)

### Day 3: Decorators
- **`log_operation`** - Function decorator with `@functools.wraps`
- **`require_permission`** - Decorator factory with arguments
- **`singleton`** - Class decorator modifying instance creation
- **`validate_types`** - Runtime type checking via decorator
- **Learning focus:** Decorators wrap functions to add behavior

### Day 4: Dataclasses and `__slots__`
- Could convert Task/User to `@dataclass` for simpler code
- Consider `__slots__` for memory optimization in large task lists
- **Learning focus:** Dataclasses reduce boilerplate

### Day 5: Iterators and Collections
- **`Project.get_tasks()`** returns iterator-friendly list
- Could implement `__iter__` on Project to iterate over tasks
- **`Storage`** could yield records lazily for large datasets
- **Learning focus:** Iterators for memory-efficient data processing

### Day 6: Context Managers
- **`Storage.transaction()`** - `@contextmanager` for atomic operations
- **Transaction rollback** on exception
- **Resource cleanup** with try/finally patterns
- **Learning focus:** Context managers ensure cleanup (rollback/commit)

### Concept Map

```
┌─────────────────────────────────────────────────────────────┐
│                    TASK MANAGEMENT SYSTEM                    │
├─────────────────────────────────────────────────────────────┤
│  Day 1: Descriptors    │  ValidatedString, ValidatedEmail   │
│                        │  ValidatedChoice, ValidatedDatetime│
├─────────────────────────────────────────────────────────────┤
│  Day 3: Decorators     │  @log_operation, @timing_decorator │
│                        │  @require_permission, @singleton   │
├─────────────────────────────────────────────────────────────┤
│  Day 6: Context Mgrs   │  with storage.transaction()        │
│                        │  Atomic save/rollback              │
├─────────────────────────────────────────────────────────────┤
│  All Days Integration  │  Clean domain model architecture   │
└─────────────────────────────────────────────────────────────┘
```

---

## Running Tests

```bash
# From repo root - all project tests
pytest week05_oop_advanced/project/tests/ -v

# Specific test category
pytest week05_oop_advanced/project/tests/test_task_system.py -k "Descriptor" -v
pytest week05_oop_advanced/project/tests/test_task_system.py -k "Decorator" -v
pytest week05_oop_advanced/project/tests/test_task_system.py -k "Transaction" -v

# Run specific test class
pytest week05_oop_advanced/project/tests/test_task_system.py::TestTaskDescriptors -v
```

---

## Stretch Features

After completing the core requirements, try these enhancements:

- [ ] **Task dependencies** - Block completion until prerequisites done
- [ ] **Time tracking** - Record time spent on each task
- [ ] **Comments/activity log** - Track all changes to a task
- [ ] **Email notifications** - Decorator to send email on assignment
- [ ] **Search and filtering** - Query tasks by multiple criteria
- [ ] **Project templates** - Create projects from predefined templates

---

## Success Criteria

Your project is complete when:

1. ✅ All 84 tests pass
2. ✅ Descriptors validate on assignment (raise `ValueError` for bad data)
3. ✅ Decorators apply cleanly without breaking functionality
4. ✅ Context manager properly handles rollback on errors
5. ✅ Status workflows enforce valid transitions
6. ✅ Role-based access control works as expected
7. ✅ You can run the "Complete Example" code above without errors

---

## Quick Reference: Key Implementation Patterns

### Descriptor Template
```python
class ValidatedAttribute:
    def __init__(self, ...):
        # Store configuration
    
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self  # Class access
        return getattr(instance, self.private_name, default)
    
    def __set__(self, instance, value):
        # Validate value
        # Raise ValueError if invalid
        setattr(instance, self.private_name, value)
```

### Decorator Template
```python
def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Before function
        result = func(*args, **kwargs)
        # After function
        return result
    return wrapper
```

### Context Manager Template
```python
from contextlib import contextmanager

@contextmanager
def my_context():
    # Setup
    try:
        yield resource
        # Success cleanup (commit)
    except Exception:
        # Error cleanup (rollback)
        raise
```

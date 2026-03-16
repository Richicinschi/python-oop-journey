# Day 6: Reflection, Introspection, and Context Managers

## Learning Objectives

By the end of this day, you will:

- Understand Python's introspection capabilities and how to inspect objects at runtime
- Master `__getattr__`, `__getattribute__`, `__setattr__`, and `__delattr__` for dynamic attribute handling
- Create context managers using both class-based (`__enter__`, `__exit__`) and generator (`@contextmanager`) approaches
- Build powerful debugging and monitoring tools using reflection
- Implement resource management patterns that ensure cleanup

---

## Key Concepts

### 1. Introspection and Reflection

**Introspection** is the ability to examine the type and properties of objects at runtime. **Reflection** goes further, allowing you to modify structure and behavior dynamically.

```python
from __future__ import annotations

class Person:
    """A simple person class."""
    
    species = "Homo sapiens"  # Class attribute
    
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self._age = age
    
    def greet(self) -> str:
        return f"Hello, I'm {self.name}"
    
    def _private_method(self) -> str:
        return "private"

# Introspection examples
p = Person("Alice", 30)

# Type introspection
type(p)  # <class 'Person'>
isinstance(p, Person)  # True
hasattr(p, 'name')  # True

# Attribute introspection
dir(p)  # List all attributes
getattr(p, 'name')  # 'Alice'
getattr(p, 'nonexistent', 'default')  # 'default' (with fallback)
setattr(p, 'city', 'New York')  # Dynamic attribute creation

# Callable introspection
callable(p.greet)  # True

# Module introspection
import inspect
inspect.getmembers(p)  # All attributes as (name, value) pairs
inspect.getsource(Person)  # Get source code
inspect.signature(Person.__init__)  # Get function signature
```

### 2. Dynamic Attribute Access

Python provides hooks for customizing attribute access:

| Method | Purpose |
|--------|---------|
| `__getattr__` | Called when attribute lookup fails |
| `__getattribute__` | Called for ALL attribute access (use with caution) |
| `__setattr__` | Called when setting any attribute |
| `__delattr__` | Called when deleting an attribute |

```python
from __future__ import annotations


class DynamicConfig:
    """Configuration with dynamic attribute access."""
    
    def __init__(self) -> None:
        self._data: dict[str, any] = {}
    
    def __getattr__(self, name: str) -> any:
        """Called when attribute is not found normally."""
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")
    
    def __setattr__(self, name: str, value: any) -> None:
        """Intercept all attribute setting."""
        if name.startswith('_'):
            # Allow private attributes to be set normally
            super().__setattr__(name, value)
        else:
            # Store public attributes in _data
            self._data[name] = value
    
    def __delattr__(self, name: str) -> None:
        """Handle attribute deletion."""
        if name in self._data:
            del self._data[name]
        else:
            super().__delattr__(name)


class MethodRouter:
    """Routes method calls based on name patterns."""
    
    def __getattr__(self, name: str) -> callable:
        """Dynamically create methods based on name."""
        if name.startswith('handle_'):
            event_type = name[7:]  # Extract event type from handle_EVENT
            
            def handler(*args, **kwargs) -> str:
                return f"Handling {event_type} event"
            
            return handler
        
        raise AttributeError(f"No method named '{name}'")

# Usage
router = MethodRouter()
router.handle_click()  # "Handling click event"
router.handle_submit()  # "Handling submit event"
```

### 3. Context Managers

Context managers ensure proper resource setup and cleanup using the `with` statement.

#### Class-Based Context Managers

```python
from __future__ import annotations
from types import TracebackType
from typing import Self


class DatabaseConnection:
    """Context manager for database connections."""
    
    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
        self.connection: any = None
        self.is_connected = False
    
    def __enter__(self) -> Self:
        """Setup - called when entering 'with' block."""
        print(f"Connecting to {self.connection_string}")
        self.connection = f"Connection({self.connection_string})"
        self.is_connected = True
        return self
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Cleanup - called when exiting 'with' block.
        
        Args:
            exc_type: Exception type if an exception occurred, else None
            exc_val: Exception value if an exception occurred, else None
            exc_tb: Exception traceback if an exception occurred, else None
        
        Returns:
            True to suppress the exception, None/False to propagate it
        """
        print("Closing connection")
        self.is_connected = False
        self.connection = None
        
        # Return False to let exceptions propagate
        return False
    
    def query(self, sql: str) -> list[dict]:
        """Execute a query."""
        if not self.is_connected:
            raise RuntimeError("Not connected")
        return [{"result": f"Data from {sql}"}]


# Usage
with DatabaseConnection("postgres://localhost/db") as db:
    results = db.query("SELECT * FROM users")
# Connection automatically closed here
```

#### Generator-Based Context Managers

```python
from __future__ import annotations
from contextlib import contextmanager
from typing import Generator
import time


@contextmanager
def timed_execution(operation_name: str) -> Generator[None, None, None]:
    """Context manager that times code execution."""
    start = time.time()
    print(f"Starting: {operation_name}")
    
    try:
        yield  # Control passes to the 'with' block
    finally:
        elapsed = time.time() - start
        print(f"Completed: {operation_name} in {elapsed:.3f}s")


# Usage
with timed_execution("data processing"):
    # Your code here
    process_large_dataset()


@contextmanager
def temporary_attribute(obj: object, attr: str, value: any) -> Generator[None, None, None]:
    """Temporarily change an attribute, then restore it."""
    original = getattr(obj, attr, None)
    has_original = hasattr(obj, attr)
    
    setattr(obj, attr, value)
    
    try:
        yield
    finally:
        if has_original:
            setattr(obj, attr, original)
        else:
            delattr(obj, attr)
```

### 4. Advanced Context Manager Patterns

```python
from __future__ import annotations
from types import TracebackType
from typing import Self


class Transaction:
    """Transaction context manager with rollback capability."""
    
    def __init__(self) -> None:
        self.operations: list[callable] = []
        self.committed = False
    
    def __enter__(self) -> Self:
        return self
    
    def add_operation(self, operation: callable, rollback: callable) -> None:
        """Add an operation with its rollback."""
        self.operations.append((operation, rollback))
        operation()  # Execute immediately
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """Commit or rollback based on success."""
        if exc_type is None:
            # No exception - commit
            self.committed = True
            return True
        else:
            # Exception occurred - rollback
            for operation, rollback in reversed(self.operations):
                rollback()
            return False  # Re-raise the exception


class Suppress:
    """Context manager to suppress specific exceptions."""
    
    def __init__(self, *exceptions: type[BaseException]) -> None:
        self.exceptions = exceptions
    
    def __enter__(self) -> Suppress:
        return self
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """Suppress specified exceptions."""
        if exc_type is not None and issubclass(exc_type, self.exceptions):
            return True  # Suppress this exception
        return False


# Usage
with Suppress(ZeroDivisionError, FileNotFoundError):
    result = 1 / 0  # Silently suppressed
```

---

## Common Mistakes

### 1. Infinite Recursion in `__getattribute__`

```python
# WRONG - infinite recursion!
class Broken:
    def __getattribute__(self, name: str) -> any:
        return self.__dict__[name]  # Calls __getattribute__ again!

# CORRECT - use super()
class Fixed:
    def __getattribute__(self, name: str) -> any:
        # Use super() to avoid recursion
        d = super().__getattribute__('__dict__')
        return d.get(name)
```

### 2. Not Handling `__exit__` Exceptions Properly

```python
# WRONG - always suppresses exceptions
class BadContext:
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        return True  # Always suppresses!

# CORRECT - only suppress when intended
class GoodContext:
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        # Return False (or None) to propagate exceptions
        return False
```

### 3. Forgetting `__setattr__` Needs Special Handling for Private Attributes

```python
# WRONG - recursion when trying to set _data
class BrokenConfig:
    def __setattr__(self, name, value):
        self._data[name] = value  # But _data doesn't exist yet!

# CORRECT - handle initialization properly
class FixedConfig:
    def __init__(self):
        # Set _data directly via object.__setattr__
        object.__setattr__(self, '_data', {})
    
    def __setattr__(self, name, value):
        if name == '_data':
            object.__setattr__(self, name, value)
        else:
            self._data[name] = value
```

---

## Connection to Exercises

| Exercise | Concept | What You'll Build |
|----------|---------|-------------------|
| Problem 1 | Introspection | Object inspector using `getattr`, `hasattr`, `dir` |
| Problem 2 | `__getattr__` | Dynamic method router |
| Problem 3 | Attribute tracking | Diff tool for object state changes |
| Problem 4 | Context managers | Timing context manager with `__enter__`/`__exit__` |
| Problem 5 | Context managers | Transaction manager with rollback |
| Problem 6 | Context managers | Temporary configuration override |

---

## Weekly Project Connection

The Week 5 project (Task Management System) uses:

- **Introspection** for debugging and logging task states
- **Dynamic attributes** for flexible task metadata
- **Context managers** for database transactions and timed operations
- **Reflection** for plugin discovery and dynamic task handlers

---

## Further Reading

- Python Data Model: https://docs.python.org/3/reference/datamodel.html
- `inspect` module: https://docs.python.org/3/library/inspect.html
- `contextlib` module: https://docs.python.org/3/library/contextlib.html
- `types` module: https://docs.python.org/3/library/types.html

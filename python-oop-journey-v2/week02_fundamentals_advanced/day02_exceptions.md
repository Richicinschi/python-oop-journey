# Day 2: Exceptions and Defensive Programming

## Overview

Today we explore Python's exception handling mechanisms and defensive programming techniques. Writing robust code means anticipating failures and handling them gracefully. Understanding when to catch exceptions, when to let them propagate, and how to create meaningful custom exceptions is essential for production-quality Python code.

## Learning Objectives

By the end of today, you will be able to:

- Use `try/except/else/finally` blocks effectively for error handling
- Understand Python's built-in exception hierarchy and when to use each type
- Create custom exception classes for domain-specific errors
- Apply the EAFP (Easier to Ask Forgiveness than Permission) vs LBYL (Look Before You Leap) philosophies
- Implement context managers for resource management
- Design defensive code that fails safely and provides meaningful error messages

## Key Concepts

### 1. Exception Basics

Exceptions in Python are objects that represent errors. When an error occurs, Python raises an exception which can be caught and handled.

```python
# Basic try/except structure
try:
    result = 10 / 0  # Raises ZeroDivisionError
except ZeroDivisionError:
    print("Cannot divide by zero")
```

**Common built-in exceptions:**
- `ValueError` - Invalid value for operation
- `TypeError` - Wrong type provided
- `KeyError` - Dictionary key not found
- `IndexError` - Sequence index out of range
- `FileNotFoundError` - File doesn't exist
- `ZeroDivisionError` - Division by zero

### 2. The Full try/except/else/finally Structure

```python
try:
    # Code that might raise an exception
    result = risky_operation()
except ValueError as e:
    # Handle specific exception type
    print(f"Invalid value: {e}")
except (TypeError, AttributeError) as e:
    # Handle multiple exception types
    print(f"Type or attribute error: {e}")
except Exception as e:
    # Catch-all (use sparingly)
    print(f"Unexpected error: {e}")
    raise  # Re-raise to preserve stack trace
else:
    # Executes only if no exception occurred
    print(f"Success: {result}")
finally:
    # Always executes (cleanup code)
    print("Cleanup complete")
```

**Best practices:**
- Catch specific exceptions, not generic `Exception`
- Use `else` for code that should only run on success
- Use `finally` for cleanup (closing files, releasing locks)
- Re-raise with `raise` (not `raise e`) to preserve traceback

### 3. Exception Hierarchy

Python exceptions form a class hierarchy. Catching a parent class catches all its children.

```
BaseException
├── SystemExit              # sys.exit()
├── KeyboardInterrupt       # Ctrl+C
└── Exception               # All other exceptions
    ├── ArithmeticError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── TypeError
    ├── ValueError
    │   └── ValidationError (custom)
    └── OSError
        ├── FileNotFoundError
        └── PermissionError
```

```python
# Catching parent catches children
try:
    some_dict[key]
except LookupError:  # Catches both KeyError and IndexError
    handle_missing()
```

### 4. Custom Exceptions

Create custom exceptions by inheriting from `Exception` or its subclasses.

```python
class ValidationError(ValueError):
    """Raised when input validation fails."""
    pass

class InsufficientFundsError(Exception):
    """Raised when account balance is too low."""
    
    def __init__(self, balance: float, amount: float) -> None:
        self.balance = balance
        self.amount = amount
        super().__init__(f"Balance {balance} insufficient for withdrawal {amount}")

# Usage
def withdraw(account_balance: float, amount: float) -> None:
    if amount > account_balance:
        raise InsufficientFundsError(account_balance, amount)
```

**Guidelines for custom exceptions:**
- Inherit from `Exception` or appropriate subclass
- Provide meaningful error messages
- Add attributes that help callers handle the error
- Document when the exception is raised

### 5. EAFP vs LBYL

Two approaches to handling potential errors:

**EAFP (Easier to Ask Forgiveness than Permission):**
```python
# Pythonic - try first, handle if it fails
try:
    value = my_dict[key]
except KeyError:
    value = default_value
```

**LBYL (Look Before You Leap):**
```python
# Check first, then act (more common in other languages)
if key in my_dict:
    value = my_dict[key]
else:
    value = default_value
```

**When to use each:**
- **EAFP**: When the exception is truly exceptional (rare), or when checking is expensive
- **LBYL**: When the condition is common, or when side effects of trying would be harmful
- **Python prefers EAFP** - it's often more readable and race-condition safe

### 6. Context Managers (with Statement)

Context managers ensure resources are properly managed, even if exceptions occur.

```python
# Built-in context managers
with open('file.txt', 'r') as f:
    content = f.read()  # File automatically closed

# Creating custom context managers
from contextlib import contextmanager

@contextmanager
def managed_resource():
    resource = acquire_resource()
    try:
        yield resource
    finally:
        release_resource(resource)

# Class-based context manager
class Transaction:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def __enter__(self):
        self.db.begin()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.db.commit()
        else:
            self.db.rollback()
        return False  # Don't suppress exceptions
```

### 7. Defensive Programming Techniques

**Input validation:**
```python
def process_data(data: list[int]) -> None:
    if not isinstance(data, list):
        raise TypeError(f"Expected list, got {type(data).__name__}")
    if not data:
        raise ValueError("Data cannot be empty")
    if not all(isinstance(x, int) for x in data):
        raise ValueError("All elements must be integers")
```

**Fail-fast with assertions (for internal invariants):**
```python
def calculate_average(numbers: list[float]) -> float:
    assert len(numbers) > 0, "Internal error: empty list passed to calculate_average"
    return sum(numbers) / len(numbers)
```

**Graceful degradation:**
```python
def load_config(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Config not found at {path}, using defaults")
        return DEFAULT_CONFIG
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {path}: {e}")
        return DEFAULT_CONFIG
```

### 8. Exception Chaining

Preserve original exception context when raising a new one:

```python
def parse_port(config: dict) -> int:
    try:
        return int(config['port'])
    except KeyError as e:
        raise ConfigError("Missing 'port' in config") from e
    except ValueError as e:
        raise ConfigError(f"Invalid port value: {config['port']}") from e

# Without 'from', the original exception is lost (suppressed)
# With 'from None', explicitly suppress the context
```

## Common Mistakes

### 1. Bare Except Clauses

```python
# WRONG - catches SystemExit, KeyboardInterrupt, etc.
try:
    do_something()
except:  # Never do this!
    pass

# CORRECT - catch specific exceptions
try:
    do_something()
except (ValueError, TypeError) as e:
    handle_error(e)
```

### 2. Catching and Ignoring

```python
# WRONG - swallowing exceptions silently
try:
    result = process_data()
except Exception:
    pass  # Where did my error go?

# CORRECT - at minimum, log the error
try:
    result = process_data()
except Exception as e:
    logger.error(f"Processing failed: {e}")
    raise  # Re-raise if you can't handle it
```

### 3. Losing Exception Information

```python
# WRONG - loses original traceback
try:
    risky_operation()
except ValueError as e:
    raise MyError(str(e))  # Loses original context

# CORRECT - preserve with 'from'
try:
    risky_operation()
except ValueError as e:
    raise MyError("Operation failed") from e
```

### 4. Overly Broad Exception Handling

```python
# WRONG - masks bugs
try:
    result = calculate(a, b)
except Exception:  # Too broad!
    result = 0

# CORRECT - handle specific expected errors
try:
    result = calculate(a, b)
except ZeroDivisionError:
    result = float('inf')
```

### 5. Using Exceptions for Control Flow

```python
# WRONG - using exceptions for normal flow
for i in range(100):
    try:
        value = my_list[i]
    except IndexError:
        break

# CORRECT - use proper iteration
for value in my_list:
    process(value)
```

### 6. Not Cleaning Up Resources

```python
# WRONG - resource leak on exception
f = open('file.txt')
data = f.read()  # Exception here leaks file handle
f.close()

# CORRECT - use context manager
with open('file.txt') as f:
    data = f.read()
```

## Connection to Exercises

Today's exercises build exception handling skills progressively:

| Exercise | Concepts Practiced |
|----------|-------------------|
| 01. Safe Divide | Basic try/except, ZeroDivisionError |
| 02. Parse Positive Int | ValueError, custom validation messages |
| 03. Validate Age | Custom exception classes |
| 04. Bounded Withdrawal | Multiple validation checks, specific exceptions |
| 05. Retry Operation | Exception handling in loops, exponential backoff |
| 06. Safe JSON Loader | File handling, JSON errors, graceful fallback |
| 07. Config Validator | Nested validation, comprehensive error collection |
| 08. Custom Exception Hierarchy | Exception inheritance, domain-specific errors |
| 09. Transaction Guard | Context managers, cleanup guarantees |
| 10. Fallback Value Resolver | Multiple exception types, priority handling |

## Weekly Project Connection

The Week 2 project (Procedural Library System) relies heavily on Day 2's exception handling concepts:

- **Custom Exceptions**: `LibraryError`, `BookNotFoundError`, `BookAlreadyExistsError` define domain-specific errors
- **Validation**: `add_book()` raises exceptions for invalid ISBNs or duplicate books
- **State Checking**: `checkout_book()` verifies availability before proceeding
- **Graceful Degradation**: File operations handle `StorageError` with meaningful messages
- **Context Managers**: File I/O uses `with` statements for safe resource handling

Example from the project:
```python
# From exceptions.py - Custom exception hierarchy
class LibraryError(Exception):
    """Base exception for library errors."""
    pass

class BookNotFoundError(LibraryError):
    """Raised when ISBN doesn't exist."""
    def __init__(self, isbn: str) -> None:
        self.isbn = isbn
        super().__init__(f"Book with ISBN '{isbn}' not found")

# From library.py - Defensive programming
def checkout_book(library: dict, isbn: str) -> dict:
    if isbn not in library:
        raise BookNotFoundError(isbn)
    if not library[isbn]["available"]:
        raise BookNotAvailableError(isbn)
    # ... proceed with checkout
```

---

## Key Takeaways

1. **Be specific** - Catch specific exception types, not generic `Exception`
2. **Don't swallow** - Never catch and ignore exceptions without logging
3. **Preserve context** - Use `raise ... from` to maintain exception chains
4. **Use context managers** - They ensure cleanup even when exceptions occur
5. **Prefer EAFP** - It's often cleaner and more Pythonic than LBYL
6. **Create meaningful errors** - Custom exceptions should help callers understand and fix problems
7. **Fail safely** - Design code that fails in predictable, non-destructive ways

## Further Reading

- [Python Exception Hierarchy](https://docs.python.org/3/library/exceptions.html)
- [PEP 8 - Exception Names](https://peps.python.org/pep-0008/#exception-names)
- [Context Managers Documentation](https://docs.python.org/3/reference/datamodel.html#context-managers)
- [Errors and Exceptions Tutorial](https://docs.python.org/3/tutorial/errors.html)

## Time Estimate

- Reading: 25-35 minutes
- Exercises: 2-3 hours
- Review: 20 minutes

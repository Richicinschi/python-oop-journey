# Day 25: Try and Except

## Learning Objectives

By the end of this day, you will be able to:

1. Use `try` and `except` to handle errors gracefully
2. Catch specific exception types
3. Understand the difference between bare `except` and specific exception handling
4. Write code that continues running even when errors occur

---

## Key Concepts

### 1. Why Handle Errors?

Without error handling, a single error crashes your entire program:

```python
# Without error handling - program crashes!
number = int(input("Enter a number: "))  # User types "abc"
# ValueError! Program crashes.
```

With error handling, your program can recover:

```python
# With error handling - program continues!
try:
    number = int(input("Enter a number: "))
except ValueError:
    print("That's not a valid number!")
    number = 0  # Use a default value
# Program continues running...
```

---

### 2. Basic Try/Except Structure

The `try` block contains code that might cause an error. The `except` block contains code that runs if an error occurs.

```python
try:
    # Code that might raise an exception
    result = 10 / 0
except ZeroDivisionError:
    # Code that runs if ZeroDivisionError occurs
    print("Cannot divide by zero!")
    result = 0
```

**How it works:**
1. Python executes the `try` block
2. If no error occurs, the `except` block is skipped
3. If an error occurs, Python jumps to the matching `except` block
4. After the `except` block, execution continues normally

---

### 3. Catching Specific Exceptions

Always catch specific exceptions, not everything. This helps you handle different errors differently:

```python
try:
    number = int(user_input)
    result = 100 / number
    data = my_list[number]
except ValueError:
    # Handle invalid conversion
    print("Please enter a valid number")
except ZeroDivisionError:
    # Handle division by zero
    print("Cannot divide by zero")
except IndexError:
    # Handle out-of-range index
    print("Index is out of range")
```

**Benefits of specific exceptions:**
- Different errors can have different solutions
- You don't accidentally catch unexpected errors
- Your code is more readable and maintainable

---

### 4. The Bare Except Problem

Avoid bare `except:` clauses—they catch everything including system interrupts!

```python
# BAD - catches KeyboardInterrupt, SystemExit, everything!
try:
    do_something()
except:  # Don't do this!
    pass

# GOOD - catches only what you expect
try:
    do_something()
except ValueError:
    pass
```

**Why bare except is dangerous:**
- Makes debugging harder
- Can mask real bugs
- Catches system signals you might want to propagate

---

### 5. Common Pattern: Try/Except with Defaults

A common pattern is providing default values when operations fail:

```python
def safe_divide(a: float, b: float) -> float:
    """Divide two numbers, returning 0 if division by zero."""
    try:
        return a / b
    except ZeroDivisionError:
        return 0.0

def safe_int_convert(value: str, default: int = 0) -> int:
    """Convert to int, returning default on failure."""
    try:
        return int(value)
    except ValueError:
        return default
```

---

### 6. The Else Clause (Optional)

The `else` clause runs only if no exception occurred:

```python
try:
    number = int(user_input)
except ValueError:
    print("Invalid number")
else:
    # This runs only if conversion succeeded
    print(f"Success! Number is {number}")
    result = number * 2
```

**Use case:** Keep the `try` block focused on the operation that might fail.

---

### 7. Best Practices

1. **Be specific**: Catch only the exceptions you expect
2. **Keep try blocks small**: Only wrap the line(s) that might fail
3. **Don't silently pass**: Do something meaningful in except blocks
4. **Document your handling**: Explain why certain errors are expected
5. **Don't use exceptions for flow control**: They're for exceptional cases

```python
# Good example
def get_user_age(input_str: str) -> int | None:
    """Parse age from string, returning None if invalid."""
    try:
        age = int(input_str)
    except ValueError:
        return None  # Invalid format
    
    if age < 0:
        return None  # Invalid value
    
    return age
```

---

## Common Mistakes to Avoid

1. **Catching everything**: `except:` catches system errors too
2. **Empty except blocks**: Hiding errors makes debugging hard
3. **Overly broad try blocks**: Wrap only what needs protection
4. **Catching and ignoring**: Always do something with caught exceptions

## Connection to Project

Error handling makes your Todo List app robust and user-friendly:

```python
def safe_load_tasks(filepath: str = "tasks.json") -> list[dict]:
    """Load tasks, returning empty list if file doesn't exist."""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # First run - no tasks file yet
        return []
    except json.JSONDecodeError:
        # File exists but is corrupted
        print(f"Warning: {filepath} is corrupted. Starting fresh.")
        return []

def safe_get_task(tasks: list[dict], task_id: int) -> dict | None:
    """Get task by ID, returning None if not found."""
    try:
        return next(t for t in tasks if t["id"] == task_id)
    except StopIteration:
        return None
```

---

## Next Steps

Tomorrow we'll explore the most common exception types in detail and learn when each one occurs.

**Next**: [Day 26: Common Exceptions](./day26_common_exceptions.md)

# Day 26: Common Exceptions

## Learning Objectives

By the end of this day, you will be able to:

1. Understand the most common Python exception types
2. Recognize when each exception occurs
3. Write appropriate error handlers for different scenarios
4. Choose the right exception type for different error situations

---

## Key Concepts

### 1. ValueError

Occurs when an operation receives an argument of the correct type but inappropriate value.

```python
# Converting invalid string to int
int("hello")  # ValueError: invalid literal for int()

# Unpacking wrong number of values
a, b = [1, 2, 3]  # ValueError: too many values to unpack

# List remove() item not found
[1, 2, 3].remove(5)  # ValueError: list.remove(x): x not in list
```

**Common causes:**
- String-to-number conversion failures
- Function arguments outside valid range
- Trying to remove non-existent items from lists

---

### 2. TypeError

Occurs when an operation is applied to an object of inappropriate type.

```python
# Wrong type for operation
len(42)  # TypeError: object of type 'int' has no len()

# Adding incompatible types
"2" + 2  # TypeError: can only concatenate str to str

# Calling non-callable object
x = 5
x()  # TypeError: 'int' object is not callable
```

**Common causes:**
- Passing wrong types to functions
- Operations between incompatible types
- Calling something that isn't a function

---

### 3. KeyError

Occurs when trying to access a dictionary key that doesn't exist.

```python
data = {"name": "Alice", "age": 30}

# Accessing non-existent key
data["email"]  # KeyError: 'email'

# Using pop() on missing key
data.pop("phone")  # KeyError: 'phone'
```

**Common causes:**
- Typos in dictionary keys
- Accessing optional fields that might not exist
- Assuming a key exists without checking

**How to avoid:**
```python
# Use get() with default
email = data.get("email", "unknown")

# Check first
if "email" in data:
    print(data["email"])
```

---

### 4. IndexError

Occurs when trying to access a sequence index that doesn't exist.

```python
items = [10, 20, 30]

# Index too large
items[5]  # IndexError: list index out of range

# Empty sequence
empty = []
empty[0]  # IndexError: list index out of range
```

**Common causes:**
- Off-by-one errors
- Not checking list length before indexing
- Assuming a list isn't empty

**How to avoid:**
```python
# Check length first
if len(items) > 5:
    print(items[5])

# Use try/except
from week00_getting_started.solutions.day25.problem_03_safe_list_access import safe_get
value = safe_get(items, 5)  # Returns None if out of range
```

---

### 5. ZeroDivisionError

Occurs when dividing by zero.

```python
10 / 0   # ZeroDivisionError: division by zero
10 % 0   # ZeroDivisionError: integer modulo by zero
```

**Common causes:**
- User input being zero unexpectedly
- Calculated values becoming zero
- Missing validation before division

---

### 6. AttributeError

Occurs when trying to access an attribute that doesn't exist.

```python
text = "hello"
text.nonexistent()  # AttributeError: 'str' has no attribute 'nonexistent'

# Common mistake with None
value = None
value.upper()  # AttributeError: 'NoneType' has no attribute 'upper'
```

**Common causes:**
- Typos in method/attribute names
- Calling methods on None
- Assuming an object has certain methods

---

## Exception Hierarchy

Python exceptions are organized in a hierarchy:

```
BaseException
├── SystemExit
├── KeyboardInterrupt
└── Exception
    ├── ArithmeticError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── TypeError
    ├── ValueError
    └── AttributeError
```

**Why this matters:**
- Catching a parent catches all its children
- `except LookupError:` catches both IndexError and KeyError
- Be specific to avoid catching unexpected errors

---

## Quick Reference Table

| Exception | When It Occurs | Example |
|-----------|----------------|---------|
| `ValueError` | Right type, wrong value | `int("abc")` |
| `TypeError` | Wrong type for operation | `len(5)` |
| `KeyError` | Missing dict key | `{"a":1}["b"]` |
| `IndexError` | Index out of range | `[1][5]` |
| `ZeroDivisionError` | Division by zero | `1/0` |
| `AttributeError` | Missing attribute | `"hi".unknown()` |

---

## Best Practices for Exception Handling

1. **Catch specific exceptions**, not general ones
2. **Handle different errors differently**
3. **Provide helpful error messages**
4. **Don't suppress errors silently**

```python
def process_user_data(data: dict) -> dict:
    """Process user data with proper error handling."""
    result = {}
    
    try:
        result["age"] = int(data["age"])
    except KeyError:
        result["error"] = "Age field is required"
    except ValueError:
        result["error"] = "Age must be a number"
    
    return result
```

## Connection to Project

Here's how specific exceptions apply to your Todo List app:

```python
def process_task_input(user_input: str, tasks: list[dict]) -> None:
    """Handle user input with specific exception handling."""
    try:
        # ValueError: user enters "abc" instead of a number
        task_id = int(user_input)
        
        # IndexError: user enters task number that doesn't exist
        task = tasks[task_id - 1]
        
        # KeyError: task dict missing expected field
        description = task["description"]
        
    except ValueError:
        print("Please enter a valid number")
    except IndexError:
        print(f"Task {task_id} doesn't exist")
    except KeyError as e:
        print(f"Task data corrupted: missing {e}")

# Handle multiple exceptions together
except (ValueError, IndexError):
    print("Invalid task selection")
```

---

## Next Steps

Tomorrow we'll learn practical debugging techniques to find and fix errors in your code.

**Next**: [Day 27: Debugging Basics](./day27_debugging_basics.md)

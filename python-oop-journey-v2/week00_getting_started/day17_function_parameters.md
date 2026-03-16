# Day 17: Function Parameters

## Learning Objectives

By the end of this day, you will:

- Understand positional arguments and how they work
- Use keyword arguments for clarity and flexibility
- Define functions with default parameter values
- Know when and how to use different argument types

---

## Key Concepts

### 1. Positional Arguments

Arguments matched by their position in the function call:

```python
def describe_pet(animal: str, name: str) -> str:
    """Return a description of a pet."""
    return f"I have a {animal} named {name}."

# Positional arguments - matched by position
result = describe_pet("dog", "Buddy")
# "I have a dog named Buddy."
```

**Important:** The order matters!

```python
describe_pet("Buddy", "dog")
# "I have a Buddy named dog."  # Wrong meaning!
```

### 2. Keyword Arguments

Arguments matched by parameter name, can be in any order:

```python
def describe_pet(animal: str, name: str) -> str:
    """Return a description of a pet."""
    return f"I have a {animal} named {name}."

# Keyword arguments - matched by name
result = describe_pet(name="Buddy", animal="dog")
# "I have a dog named Buddy."
```

You can mix positional and keyword arguments:

```python
# Positional first, then keyword
describe_pet("dog", name="Buddy")  # Valid

# All positional after keyword is NOT allowed
describe_pet(animal="dog", "Buddy")  # SyntaxError!
```

### 3. Default Parameter Values

Provide default values that are used when no argument is passed:

```python
def greet(name: str, greeting: str = "Hello") -> str:
    """Return a greeting message."""
    return f"{greeting}, {name}!"

# Using default
greet("Alice")           # "Hello, Alice!"

# Overriding default
greet("Alice", "Hi")     # "Hi, Alice!"
greet("Bob", greeting="Hey")  # "Hey, Bob!"
```

### 4. Mutable Default Values - A Dangerous Trap!

Never use mutable default values (like lists or dictionaries):

```python
# WRONG - Mutable default!
def add_item_wrong(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items

# The list persists between calls!
add_item_wrong("a")  # Returns ["a"]
add_item_wrong("b")  # Returns ["a", "b"] - Surprise!
```

Correct approach:

```python
# CORRECT - Use None as default
def add_item_correct(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items

add_item_correct("a")  # Returns ["a"]
add_item_correct("b")  # Returns ["b"] - Correct!
```

### 5. Best Practices for Parameters

```python
def create_profile(
    name: str,           # Required positional
    age: int,            # Required positional
    city: str = "Unknown",   # Optional with default
    active: bool = True      # Optional with default
) -> dict[str, str | int | bool]:
    """Create a user profile.
    
    Args:
        name: The user's full name (required)
        age: The user's age in years (required)
        city: The user's city (optional, default "Unknown")
        active: Whether the account is active (optional, default True)
    """
    return {
        "name": name,
        "age": age,
        "city": city,
        "active": active
    }

# Various ways to call
create_profile("Alice", 30)
create_profile("Bob", 25, city="NYC")
create_profile("Carol", 35, active=False)
create_profile("Dave", 40, city="LA", active=True)
```

---

## Common Mistakes

### 1. Mutable Default Arguments

```python
def bad_append(item: int, lst: list = []) -> list:  # Danger!
    lst.append(item)
    return lst

# Fix: Use None
def good_append(item: int, lst: list | None = None) -> list:
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### 2. Keyword Before Positional

```python
def func(a: int, b: int, c: int) -> int:
    return a + b + c

func(1, b=2, 3)      # SyntaxError!
func(1, 2, c=3)      # OK - positional then keyword
```

### 3. Forgetting Required Arguments

```python
def greet(name: str, greeting: str) -> str:
    return f"{greeting}, {name}!"

greet("Alice")       # TypeError - missing 'greeting'
```

---

## Connection to Exercises

### Problem 01: Create User
Practice positional and optional parameters with defaults.

### Problem 02: Calculate Total Price
Work with multiple parameters and default values.

### Problem 03: Format Name
Combine positional and keyword arguments.

### Problem 04: Create Shopping List
Avoid the mutable default trap.

### Problem 05: Configure Settings
Multiple optional parameters with defaults.

---

## Connection to Project

Default parameters make your CLI more user-friendly:

```python
def add_task(
    description: str,
    priority: str = "medium",  # Default priority
    due_date: str | None = None  # Optional due date
) -> dict:
    """Add a task with optional parameters."""
    return {
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }

# User can call in different ways:
add_task("Buy milk")  # Uses defaults
add_task("Buy milk", "high")  # Overrides priority
add_task("Buy milk", due_date="2024-12-25")  # Uses keyword
```

---

## Tips for Success

1. **Put required parameters first**, optional ones last
2. **Use keyword arguments** for clarity with many parameters
3. **Never use mutable defaults** - use `None` instead
4. **Be consistent** in your argument passing style
5. **Document parameters** in your docstrings

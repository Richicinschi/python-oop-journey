# Day 16: Defining Functions

## Learning Objectives

By the end of this day, you will:

- Understand how to define functions using the `def` keyword
- Learn how to use the `return` statement to send values back
- Know how to call functions and use their results
- Write functions with proper type hints and docstrings

---

## Key Concepts

### 1. Defining Functions with `def`

Functions are reusable blocks of code that perform a specific task:

```python
def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"
```

**Key elements:**
- `def` keyword to start the function definition
- Function name (lowercase with underscores)
- Parameters in parentheses (with type hints)
- Colon `:` to start the function body
- Docstring (triple-quoted string) describing the function
- Function body (indented code)
- `return` statement to output a value

### 2. The `return` Statement

The `return` statement sends a value back to the caller:

```python
def add(a: int, b: int) -> int:
    """Return the sum of two numbers."""
    result = a + b
    return result

# Using the return value
sum_result = add(3, 5)  # sum_result is 8
```

Functions without `return` return `None`:

```python
def print_greeting(name: str) -> None:
    """Print a greeting (no return value)."""
    print(f"Hello, {name}!")

result = print_greeting("Alice")  # result is None
```

### 3. Calling Functions

Call a function by using its name followed by parentheses with arguments:

```python
def multiply(x: int, y: int) -> int:
    """Return the product of x and y."""
    return x * y

# Calling the function
product = multiply(4, 5)  # Returns 20
```

### 4. Multiple Return Values

Functions can return multiple values as a tuple:

```python
def divide_and_remainder(dividend: int, divisor: int) -> tuple[int, int]:
    """Return quotient and remainder."""
    quotient = dividend // divisor
    remainder = dividend % divisor
    return quotient, remainder

q, r = divide_and_remainder(17, 5)  # q=3, r=2
```

### 5. Type Hints and Docstrings

Always use type hints and write clear docstrings:

```python
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle.
    
    Args:
        length: The length of the rectangle.
        width: The width of the rectangle.
        
    Returns:
        The area of the rectangle (length * width).
    """
    return length * width
```

---

## Common Mistakes

### 1. Forgetting `return`

```python
def add_wrong(a: int, b: int) -> int:
    result = a + b  # Missing return!

def add_correct(a: int, b: int) -> int:
    result = a + b
    return result
```

### 2. Indentation Errors

```python
def bad_function():  # Missing colon or wrong indentation
return "Hello"        # This will cause an error

def good_function() -> str:
    return "Hello"    # Proper indentation
```

### 3. Calling Without Parentheses

```python
def say_hello() -> str:
    return "Hello"

message = say_hello    # Wrong - assigns the function object
message = say_hello()  # Correct - calls the function
```

---

## Connection to Exercises

### Problem 01: Simple Greeting
Practice basic function definition and return.

### Problem 02: Calculate Rectangle Area
Apply type hints and docstrings to a simple calculation.

### Problem 03: Is Even
Return a boolean from a function.

### Problem 04: Get Sign
Practice multiple return paths with if/else.

### Problem 05: Max of Three
Combine multiple return statements with comparison logic.

---

## Connection to Project

Functions are the building blocks of your final project:

- Each menu option (add, complete, delete) will be a function
- File operations (save/load) will be separate functions
- Helper functions for validation and formatting

Example from the project:
```python
def add_task(description: str, priority: str = "medium") -> dict:
    """Create and return a new task dictionary."""
    return {
        "id": generate_id(),
        "description": description,
        "priority": priority,
        "completed": False
    }
```

---

## Tips for Success

1. **Always include type hints** - They make your code clearer
2. **Write descriptive docstrings** - Explain what the function does
3. **Use verb names** for functions (get_, calculate_, is_, has_)
4. **Keep functions focused** - One function should do one thing
5. **Test your functions** - Call them with different inputs to verify

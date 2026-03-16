# Day 28: Modules and Imports

## Learning Objectives

By the end of this day, you will:

- Understand what Python modules are and why they matter
- Know how to create your own modules
- Master different import styles and their use cases
- Learn about module execution and the `__name__ == "__main__"` pattern
- Understand Python's module search path

---

## What is a Module?

A **module** is simply a Python file containing definitions and statements. Any Python file (`.py`) can be imported as a module.

### Why Use Modules?

1. **Organization**: Keep related code together
2. **Reusability**: Use the same code across multiple programs
3. **Namespace**: Avoid naming conflicts
4. **Maintainability**: Smaller, focused files are easier to manage

---

## Creating a Module

Create a file named `math_utils.py`:

```python
"""Utility functions for mathematical operations."""

PI = 3.14159


def add(a: int, b: int) -> int:
    """Return the sum of two numbers."""
    return a + b


def multiply(a: int, b: int) -> int:
    """Return the product of two numbers."""
    return a * b


def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"
```

---

## Import Styles

### 1. Import the Entire Module

```python
import math_utils

result = math_utils.add(5, 3)
print(math_utils.PI)
```

**Pros**: Clear namespace, always know where functions come from  
**Cons**: More typing

### 2. Import Specific Items

```python
from math_utils import add, PI

result = add(5, 3)  # No module prefix needed
print(PI)
```

**Pros**: Less typing, direct access  
**Cons**: Can cause naming conflicts

### 3. Import with Alias

```python
import math_utils as mu
from math_utils import add as addition

result = mu.multiply(4, 5)
sum_result = addition(2, 3)
```

**Pros**: Shortens long module names, resolves conflicts  
**Cons**: Can reduce readability if overused

### 4. Import Everything (NOT Recommended)

```python
from math_utils import *  # Avoid this!
```

**Why avoid?**: Pollutes namespace, unclear where names come from, hard to debug

---

## The `__name__ == "__main__"` Pattern

When a Python file is run directly, `__name__` is set to `"__main__"`. When imported, it's set to the module name.

```python
# calculator.py

def calculate(x: int, y: int) -> int:
    return x + y


if __name__ == "__main__":
    # This code only runs when the file is executed directly
    print("Running calculator directly!")
    result = calculate(10, 20)
    print(f"Result: {result}")
```

```python
# main.py
import calculator  # The __main__ block doesn't run!

result = calculator.calculate(5, 3)  # Just uses the function
```

---

## Module Search Path

Python looks for modules in this order:

1. Current directory
2. `PYTHONPATH` environment variable directories
3. Standard library directories
4. Site-packages (third-party packages)

```python
import sys

print(sys.path)  # See where Python looks for modules
```

---

## Best Practices

1. **Use explicit imports**: Prefer `import module` or `from module import name`
2. **Avoid `import *`**: It makes code hard to read and debug
3. **Place imports at the top**: Keep all imports at the beginning of the file
4. **Group imports**: Standard library, third-party, then local modules
5. **Use meaningful aliases**: Only when it improves readability

---

## Common Mistakes

### Circular Imports

```python
# a.py
from b import func_b  # Importing from b

def func_a():
    return "A"
```

```python
# b.py
from a import func_a  # Importing from a - CIRCULAR!

def func_b():
    return "B"
```

**Solution**: Restructure code or use imports inside functions.

### Shadowing Built-ins

```python
from math_utils import sum  # Shadows built-in sum()!
```

**Solution**: Use aliases or import the module instead.

---

## Today's Exercises

1. **Problem 01**: Create a greeting module
2. **Problem 02**: Build a calculator module with constants
3. **Problem 03**: String utilities module
4. **Problem 04**: Temperature conversion module
5. **Problem 05**: Module with main guard pattern

---

## Project Connection

Today's concepts are essential for the final project:
- You'll organize your code into logical modules
- The `__main__` guard will let you run your CLI app
- Imports will help separate concerns (data, logic, UI)

Keep modules small and focused - one module per responsibility!

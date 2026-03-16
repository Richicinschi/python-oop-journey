# Day 03: Your First Python Program

## Learning Objectives

By the end of this day, you will be able to:

1. Write a complete Python program with proper structure
2. Use the `print()` function with various options (sep, end)
3. Create f-strings for formatted output
4. Write single-line and multi-line comments
5. Structure a Python file with docstrings and imports
6. Understand and use the `if __name__ == "__main__":` pattern

---

## What You Will Learn
- How to write a complete Python program
- The `print()` function in detail
- Different types of comments and when to use them
- Basic program structure
- Best practices for beginner code

---

## Hello, World!

The traditional first program in any language prints "Hello, World!" Let's understand why.

### The Classic Example

```python
print("Hello, World!")
```

**Output:**
```
Hello, World!
```

This simple program teaches us:
1. How to call a function (`print`)
2. How to use strings (text in quotes)
3. How to run Python code
4. How to see output

---

## Understanding the `print()` Function

`print()` is a **built-in function**—it comes with Python and is always available.

### Basic Usage

```python
print("This is a message")
```

### Printing Multiple Items

```python
print("Hello", "World")        # Output: Hello World
print("The answer is", 42)     # Output: The answer is 42
```

`print()` automatically adds a space between items.

### Customizing the Separator

```python
print("a", "b", "c", sep="-")  # Output: a-b-c
print("1", "2", "3", sep="")   # Output: 123
```

### Changing the End Character

By default, `print()` adds a newline (moves to next line):

```python
print("Hello")
print("World")
# Output:
# Hello
# World
```

You can change this:

```python
print("Hello", end=" ")
print("World")
# Output: Hello World
```

```python
print("Loading", end="")
print("...", end="")
print("Done!")
# Output: Loading...Done!
```

### Using F-Strings (Formatted Strings)

F-strings let you insert variables into text:

```python
name = "Alice"
age = 25

print(f"My name is {name} and I am {age} years old.")
# Output: My name is Alice and I am 25 years old.
```

The `f` before the string tells Python to evaluate expressions inside `{}`.

### F-String Expressions

You can do simple math inside f-strings:

```python
a = 10
b = 5

print(f"{a} + {b} = {a + b}")  # Output: 10 + 5 = 15
print(f"{a} * {b} = {a * b}")  # Output: 10 * 5 = 50
```

---

## Comments: Explaining Your Code

**Comments** are notes in your code that Python ignores. They're for humans, not computers.

### Why Use Comments?

1. **Explain complex code**: Help yourself and others understand
2. **Mark TODOs**: Remind yourself what needs work
3. **Temporarily disable code**: Testing without deleting

### Single-Line Comments

Use `#` for comments that fit on one line:

```python
# This is a single-line comment
name = "Alice"  # This comment is at the end of a line

# Calculate the area of a rectangle
width = 10
height = 5
area = width * height  # Formula: width times height
```

### Multi-Line Comments

For longer explanations, use triple quotes:

```python
"""
This is a multi-line comment.
It can span multiple lines.
Use it for file descriptions or function explanations.
"""

name = "Alice"
```

Or use multiple single-line comments:

```python
# This program calculates the total cost of items
# including tax and shipping
# Written by: Your Name
# Date: 2024
```

### Comment Best Practices

✅ **Good Comments:**
```python
# Convert temperature from Celsius to Fahrenheit
celsius = 25
fahrenheit = (celsius * 9/5) + 32

# Check if user is eligible for discount
if age < 18 or age > 65:
    apply_discount()
```

❌ **Bad Comments:**
```python
# Set x to 5
x = 5  # This is obvious from the code

# This function does stuff
def calculate():  # Vague, doesn't explain what "stuff" is
    pass
```

**Rule**: Comments should explain *why*, not *what*. The code shows what; comments explain why decisions were made.

---

## Program Structure

A well-structured Python file looks like this:

```python
"""Module docstring - explains what this file does.

This module provides functions for calculating areas
of different geometric shapes.
"""

from __future__ import annotations


# Constants (usually at the top, in UPPER_CASE)
PI = 3.14159
DEFAULT_RADIUS = 1.0


def calculate_circle_area(radius: float) -> float:
    """Calculate the area of a circle.
    
    Args:
        radius: The radius of the circle.
        
    Returns:
        The area of the circle.
    """
    return PI * radius * radius


def main() -> None:
    """Main function - program entry point."""
    radius = 5.0
    area = calculate_circle_area(radius)
    print(f"A circle with radius {radius} has area {area:.2f}")


if __name__ == "__main__":
    main()
```

### The Parts Explained

| Part | Purpose |
|------|---------|
| **Module docstring** | Explains what the file does |
| **`from __future__ import annotations`** | Enables modern type hint features |
| **Constants** | Values that don't change |
| **Functions** | Reusable blocks of code |
| **`main()` function** | Where the program starts running |
| **`if __name__ == "__main__":`** | Standard Python entry point pattern |

### Why `if __name__ == "__main__":`?

This is a Python idiom that means:
> "Only run this code if the file is being run directly, not if it's being imported."

It allows the same file to be:
1. Run as a standalone program
2. Imported as a module by other code

---

## Your First Complete Program

Let's put it all together:

```python
"""My First Python Program.

This program greets the user and shows the current date.
It's designed for absolute beginners learning Python.
"""

from __future__ import annotations

# Import the datetime module to work with dates
from datetime import date


def get_greeting(name: str) -> str:
    """Create a personalized greeting message.
    
    Args:
        name: The name of the person to greet.
        
    Returns:
        A friendly greeting string.
    """
    return f"Hello, {name}! Welcome to Python!"


def show_date_info() -> None:
    """Display information about today's date."""
    today = date.today()
    
    # Print date in different formats
    print(f"Today's date: {today}")
    print(f"Formatted: {today.strftime('%B %d, %Y')}")
    print(f"Day of week: {today.strftime('%A')}")


def main() -> None:
    """Main program entry point."""
    # Get user's name
    user_name = "Learner"  # In the future, we'll get this from user input
    
    # Print greeting
    greeting = get_greeting(user_name)
    print(greeting)
    print()  # Empty line for spacing
    
    # Show date information
    print("Here is some information about today:")
    show_date_info()
    
    # Farewell message
    print()  # Empty line
    print("Keep learning and have fun with Python!")


# Standard entry point check
if __name__ == "__main__":
    main()
```

**Output:**
```
Hello, Learner! Welcome to Python!

Here is some information about today:
Today's date: 2024-01-15
Formatted: January 15, 2024
Day of week: Monday

Keep learning and have fun with Python!
```

---

## Today's Exercise

Create your own "Hello, World" program with improvements!

See the exercise file: [day03_exercises/hello_world.py](./day03_exercises/hello_world.py)

And the solution: [day03_solutions/hello_world.py](./day03_solutions/hello_world.py)

Run the tests: [day03_tests/test_hello_world.py](./day03_tests/test_hello_world.py)

---

## Connection to Exercises

| Exercise | Skills Practiced |
|----------|------------------|
| hello_world.py | Program structure, print(), f-strings, comments |

Exercise files: [day03_exercises/hello_world.py](./day03_exercises/hello_world.py)  
Solution: [day03_solutions/hello_world.py](./day03_solutions/hello_world.py)  
Tests: [day03_tests/test_hello_world.py](./day03_tests/test_hello_world.py)

## Connection to Weekly Project

The program structure you learn today (module docstring, imports, functions, main()) will be used throughout the Todo CLI project. Every file in your project should follow this pattern.

---

## Summary

### What You Learned

1. **`print()` function**: Display output to the screen
2. **F-strings**: Insert variables into strings with `f"...{variable}..."`
3. **Comments**: Explain code with `#` for single-line or `"""` for multi-line
4. **Program structure**: Docstrings, imports, constants, functions, and `main()`
5. **Entry point**: `if __name__ == "__main__":` pattern

### Key Takeaways

- Always use comments to explain why, not what
- Structure your programs with a `main()` function
- Use f-strings for readable string formatting
- Start every file with a module docstring

---

## What's Next?

Congratulations! You've completed Week 0: Getting Started!

You're now ready for **Week 1: Python Fundamentals**, where you'll learn:
- Variables and data types
- Strings and string manipulation
- Lists and tuples
- Dictionaries and sets
- Control flow (if/else, loops)
- Functions and recursion

**Next**: Start [Week 1: Python Fundamentals](../week01_fundamentals/README.md)

---

## Quick Reference

### Print Function

```python
print("Hello")                    # Basic print
print("a", "b", "c")              # Multiple items (space-separated)
print("a", "b", sep="-")          # Custom separator
print("Hello", end=" ")           # Custom ending (no newline)
print(f"Value: {x}")              # F-string with variable
```

### Comments

```python
# Single-line comment

"""
Multi-line comment
or docstring
"""
```

### Basic Program Template

```python
"""Module description."""

from __future__ import annotations


def main() -> None:
    """Main entry point."""
    print("Program running...")


if __name__ == "__main__":
    main()
```

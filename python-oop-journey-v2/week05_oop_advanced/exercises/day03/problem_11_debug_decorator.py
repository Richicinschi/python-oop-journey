"""Problem 11: Debug Decorator

Topic: Debug Function Calls
Difficulty: Easy

Create a decorator that prints debug information about function calls.

This demonstrates inspecting function arguments and return values at runtime,
a technique useful for debugging and logging in development environments.

Example:
    >>> @debug
    ... def add(a: int, b: int) -> int:
    ...     return a + b
    
    >>> add(2, 3)
    DEBUG: Calling add(2, 3)
    DEBUG: add returned 5
    5

    >>> @debug
    ... def greet(name: str, greeting: str = "Hello") -> str:
    ...     return f"{greeting}, {name}!"
    
    >>> greet("World", greeting="Hi")
    DEBUG: Calling greet('World', greeting='Hi')
    DEBUG: greet returned 'Hi, World!'
    'Hi, World!'

    >>> @debug
    ... def compute(x: float, y: float, op: str = "add") -> float:
    ...     return x + y if op == "add" else x - y
    
    >>> compute(10.5, 3.5, op="sub")
    DEBUG: Calling compute(10.5, 3.5, op='sub')
    DEBUG: compute returned 7.0
    7.0

Behavior Notes:
    - Prints "DEBUG: Calling <func_name>(<args_repr>)" before execution
    - Prints "DEBUG: <func_name> returned <result_repr>" after execution
    - Uses repr() for argument and result representation
    - Prints to stdout (use print() function)
    - Returns the original function's result unchanged

Edge Cases:
    - Works with functions that return None (shows "returned None")
    - Works with functions that raise exceptions (no "returned" line printed)
    - Handles both positional and keyword arguments
    - Empty argument list shows as "func_name()"
"""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any


def debug(func: Callable) -> Callable:
    """A decorator that prints debug information about function calls.
    
    Prints:
    - Function name and signature
    - Arguments (args and kwargs)
    - Return value
    
    Format:
    "DEBUG: Calling <func_name>(<args_repr>)"
    "DEBUG: <func_name> returned <result_repr>"
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function with debug output
    """
    raise NotImplementedError("Implement the debug decorator")


# Hints for Debug Decorator (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to print function entry (with args) and exit (with result). Use repr()
# to format arguments and results.
#
# Hint 2 - Structural plan:
# - Create a wrapper function
# - Before calling func, print the entry message with function name and args
# - Call the function and store the result
# - Print the exit message with the result
# - Return the result
#
# Hint 3 - Edge-case warning:
# What if the function raises an exception? You might want to catch it, print an
# error message, then re-raise. Also, be careful with large objects in repr().

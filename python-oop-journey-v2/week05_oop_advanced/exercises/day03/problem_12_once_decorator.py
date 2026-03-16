"""Problem 12: Once Decorator

Topic: Run Only Once
Difficulty: Easy

Create a decorator that ensures a function runs only once.

This demonstrates caching results and preventing re-execution, useful for
initialization code, expensive setup operations, or ensuring side effects
happen exactly one time.

Example:
    >>> @once
    ... def initialize():
    ...     print("Initializing...")
    ...     return "Setup complete"
    
    >>> initialize()
    Initializing...
    'Setup complete'
    >>> initialize()  # Returns cached result, doesn't print
    'Setup complete'
    >>> initialize()  # Same result every time
    'Setup complete'

    >>> call_count = 0
    >>> @once
    ... def expensive_computation(x):
    ...     global call_count
    ...     call_count += 1
    ...     return x * x
    
    >>> expensive_computation(5)
    25
    >>> expensive_computation(10)  # Still returns 25 (first call cached)
    25
    >>> call_count
    1

Behavior Notes:
    - Executes the function on first call and caches the result
    - Returns cached result on all subsequent calls
    - Ignores arguments on subsequent calls (always returns first result)
    - The original function is called exactly once

Edge Cases:
    - Works with functions that return None (caches None)
    - Works with functions that raise exceptions (exception is raised, not cached)
    - Each decorated function has its own separate cache
    - Thread safety is NOT required for this exercise
"""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any


def once(func: Callable) -> Callable:
    """A decorator that ensures a function runs only once.
    
    Subsequent calls return the result from the first call without
    re-executing the function.
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function that runs only once
    """
    raise NotImplementedError("Implement the once decorator")


# Hints for Once Decorator (Medium):
# 
# Hint 1 - Conceptual nudge:
# Similar to cache but simpler - you only need to remember if the function has
# been called and what the result was.
#
# Hint 2 - Structural plan:
# - Create a wrapper function
# - Store a "called" flag and "result" variable in the closure
# - On first call, execute function, store result, set flag
# - On subsequent calls, return stored result without calling function
# - functools.wraps preserves metadata
#
# Hint 3 - Edge-case warning:
# What about exceptions on the first call? Should subsequent calls retry or
# keep raising the same exception?

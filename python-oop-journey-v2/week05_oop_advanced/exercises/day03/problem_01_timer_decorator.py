"""Problem 01: Timer Decorator

Topic: Function Decorators
Difficulty: Easy

Create a decorator that times function execution and prints the elapsed time.

This demonstrates basic decorator creation with the @wraps decorator and
using time.perf_counter() for precise timing measurements.

Example:
    >>> @timer
    ... def slow_add(a: int, b: int) -> int:
    ...     import time
    ...     time.sleep(0.01)
    ...     return a + b
    
    >>> result = slow_add(2, 3)  # Prints: "slow_add took 0.0123 seconds"
    5

    >>> @timer
    ... def quick_greet(name: str) -> str:
    ...     return f"Hello, {name}!"
    
    >>> quick_greet("World")  # Prints: "quick_greet took 0.0001 seconds"
    'Hello, World!'

Behavior Notes:
    - Uses time.perf_counter() for high-precision timing
    - Prints time with exactly 4 decimal places
    - The printed format is: "<function_name> took <elapsed:.4f} seconds"
    - Preserves function metadata using @wraps
    - Returns the original function's result unchanged

Edge Cases:
    - Very fast functions may show 0.0000 seconds
    - Works with functions that return None
    - Works with functions that raise exceptions (timer still prints)
"""

from __future__ import annotations

from functools import wraps
from time import perf_counter
from typing import Callable, Any


def timer(func: Callable) -> Callable:
    """A decorator that times function execution.
    
    Prints the elapsed time with 4 decimal places in the format:
    "<function_name> took <elapsed_time:.4f} seconds"
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function that times execution
    """
    raise NotImplementedError("Implement the timer decorator")

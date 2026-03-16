"""Problem 05: Logged Class Decorator

Topic: Log All Method Calls
Difficulty: Medium

Create a class decorator that logs all method calls.

This demonstrates metaprogramming at the class level - inspecting and
modifying class attributes to add cross-cutting concerns like logging
to all methods without modifying each one individually.

Example:
    >>> @logged
    ... class Calculator:
    ...     def add(self, a: float, b: float) -> float:
    ...         return a + b
    ...     def multiply(self, a: float, b: float) -> float:
    ...         return a * b
    
    >>> calc = Calculator()
    >>> calc.add(2, 3)  # Prints: "Calling add with args=(2, 3), kwargs={}"
    Calling add with args=(2, 3), kwargs={}
    5
    >>> calc.multiply(4, 5)  # Prints: "Calling multiply with args=(4, 5), kwargs={}"
    Calling multiply with args=(4, 5), kwargs={}
    20

    >>> @logged
    ... class Greeter:
    ...     def greet(self, name: str, greeting: str = "Hello") -> str:
    ...         return f"{greeting}, {name}!"
    
    >>> Greeter().greet("World", greeting="Hi")
    Calling greet with args=('World',), kwargs={'greeting': 'Hi'}
    'Hi, World!'

Behavior Notes:
    - Wraps all callable attributes that don't start with '_'
    - Preserves original method behavior and return values
    - Uses functools.wraps to preserve method metadata
    - The message format is exactly: "Calling <method_name> with args=<args>, kwargs=<kwargs>"

Edge Cases:
    - Magic methods (starting with __) should NOT be wrapped
    - Private methods (starting with _ but not __) SHOULD be wrapped
    - Properties should NOT be wrapped (use callable() check)
    - The class itself is modified in place (no wrapper class needed)
"""

from __future__ import annotations

from functools import wraps
from typing import Type, Any, Callable


def logged(cls: Type) -> Type:
    """A class decorator that logs all method calls.
    
    Wraps all callable attributes (except magic methods) to log their calls.
    Prints: "Calling <method_name> with args=<args>, kwargs=<kwargs>"
    
    Args:
        cls: The class to decorate
        
    Returns:
        The decorated class with logging
    """
    raise NotImplementedError("Implement the logged decorator")


# Hints for Logged Class Decorator (Hard):
# 
# Hint 1 - Conceptual nudge:
# You need to iterate through the class's methods and wrap each one with logging.
# Use getattr and setattr to replace methods.
#
# Hint 2 - Structural plan:
# - Iterate through cls.__dict__ to find methods
# - Skip dunder methods (names starting and ending with __)
# - For each method, create a wrapper that logs and calls original
# - Use setattr(cls, name, wrapper) to replace the method
# - Return the modified class
#
# Hint 3 - Edge-case warning:
# Be careful with classmethods and staticmethods - they need special handling.
# You might need to detect them using isinstance(attr, (classmethod, staticmethod)).

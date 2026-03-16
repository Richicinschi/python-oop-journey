"""Problem 07: Immutable Decorator

Topic: Make Class Immutable
Difficulty: Hard

Create a class decorator that makes instances immutable after creation.

This demonstrates intercepting attribute access and modification to enforce
immutability - a pattern used by Python's built-in tuple, frozenset, and
frozen dataclasses. Prevents accidental state mutations.

Example:
    >>> @immutable
    ... class Point:
    ...     def __init__(self, x: float, y: float):
    ...         self.x = x
    ...         self.y = y
    
    >>> p = Point(1.0, 2.0)
    >>> p.x
    1.0
    >>> p.x = 3.0  # Raises AttributeError
    Traceback (most recent call last):
        ...
    AttributeError: Cannot modify immutable attribute 'x'
    
    >>> p.z = 5.0  # Also raises AttributeError for new attributes
    Traceback (most recent call last):
        ...
    AttributeError: Cannot set attribute on immutable instance

    >>> @immutable
    ... class Config:
    ...     def __init__(self, debug: bool = False):
    ...         self.debug = debug
    
    >>> cfg = Config(debug=True)
    >>> cfg.debug
    True
    >>> cfg.debug = False  # Cannot change after creation
    Traceback (most recent call last):
        ...
    AttributeError: Cannot modify immutable attribute 'debug'

Behavior Notes:
    - Allows attribute setting during __init__
    - Prevents attribute modification after __init__ completes
    - Prevents adding new attributes after creation
    - Raises AttributeError with descriptive message on violation
    - Error messages: "Cannot modify immutable attribute '{name}'" or
      "Cannot set attribute on immutable instance"

Edge Cases:
    - __init__ must be able to set initial values
    - Special methods (__str__, __repr__, etc.) should work normally
    - Deletion (del obj.attr) should also be prevented
    - The check should be instance-specific, not class-level
    - Private attributes (starting with _) follow same rules
"""

from __future__ import annotations

from typing import Type, Any


def immutable(cls: Type) -> Type:
    """A class decorator that makes instances immutable.
    
    Prevents setting new attributes or modifying existing ones after __init__.
    Raises AttributeError on any attempt to modify the instance.
    
    Args:
        cls: The class to decorate
        
    Returns:
        The decorated class with immutability enforcement
    """
    raise NotImplementedError("Implement the immutable decorator")


# Hints for Immutable Decorator (Hard):
# 
# Hint 1 - Conceptual nudge:
# You need to override __setattr__ on the class to prevent modifications after
# __init__ completes. The class decorator can modify the class's behavior.
#
# Hint 2 - Structural plan:
# - Define a custom __setattr__ that checks if _initialized flag is set
# - Store this as the class's __setattr__ method
# - Modify __init__ to set _initialized = True at the end
# - Also override __delattr__ to prevent deletion
#
# Hint 3 - Edge-case warning:
# Be careful - during __init__, you NEED to allow attribute setting! Use the
# _initialized flag to distinguish between initialization time and after.
# What about slots? The implementation becomes more complex.

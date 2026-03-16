"""Problem 06: Singleton Decorator

Topic: Class Decorator for Singleton
Difficulty: Medium

Create a class decorator that ensures only one instance of a class exists.

This demonstrates the Singleton pattern using a class decorator instead of
a metaclass. The singleton pattern is useful for managing shared resources
like database connections, configuration managers, or logging services.

Example:
    >>> @singleton
    ... class Database:
    ...     def __init__(self, connection_string: str = "default"):
    ...         self.connection_string = connection_string
    ...     def connect(self):
    ...         return f"Connected to {self.connection_string}"
    
    >>> db1 = Database("postgresql://localhost")
    >>> db2 = Database("mysql://remote")  # Returns same instance!
    >>> db1 is db2
    True
    >>> db1.connection_string  # First initialization wins
    'postgresql://localhost'

    >>> @singleton
    ... class Config:
    ...     def __init__(self):
    ...         self.debug = False
    ...         self.version = "1.0.0"
    
    >>> cfg1 = Config()
    >>> cfg2 = Config()
    >>> cfg1 is cfg2
    True

Behavior Notes:
    - The first call to the class creates and stores the instance
    - Subsequent calls return the same instance (ignoring new arguments)
    - The decorator maintains a dictionary mapping classes to instances
    - Works with __init__ arguments on first call only

Edge Cases:
    - Multiple classes decorated with @singleton each get their own instance
    - Calling the class after first creation ignores all constructor arguments
    - The instance persists for the lifetime of the program
    - Thread safety is NOT required for this exercise
"""

from __future__ import annotations

from typing import Type, Any, Dict


def singleton(cls: Type) -> Type:
    """A class decorator that implements the Singleton pattern.
    
    Ensures only one instance of the decorated class exists.
    All subsequent instantiations return the same instance.
    
    Args:
        cls: The class to decorate
        
    Returns:
        A wrapper that manages the singleton instance
    """
    raise NotImplementedError("Implement the singleton decorator")


# Hints for Singleton Decorator (Medium):
# 
# Hint 1 - Conceptual nudge:
# A class decorator replaces the class with a wrapper function. When the wrapper
# is called (as if creating an instance), return the singleton instance.
#
# Hint 2 - Structural plan:
# - Create a wrapper function that will replace the class
# - Store the original class and a reference to the single instance
# - On first call, create instance using cls(*args, **kwargs)
# - On subsequent calls, return the stored instance
# - functools.wraps helps preserve class metadata
#
# Hint 3 - Edge-case warning:
# What if someone tries to create an instance with different arguments the second
# time? Should you warn them? Also, consider thread safety.

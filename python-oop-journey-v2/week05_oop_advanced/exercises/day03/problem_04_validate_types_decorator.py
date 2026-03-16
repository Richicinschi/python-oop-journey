"""Problem 04: Validate Types Decorator

Topic: Runtime Type Checking
Difficulty: Medium

Create a decorator that validates function arguments against type hints.

This demonstrates introspecting function signatures and type hints at runtime,
then validating arguments before function execution. Useful for debugging
and ensuring type safety in dynamically-typed Python.

Example:
    >>> @validate_types
    ... def greet(name: str, age: int) -> str:
    ...     return f"{name} is {age} years old"
    
    >>> greet("Alice", 30)  # Valid types
    'Alice is 30 years old'
    
    >>> greet("Alice", "thirty")  # Invalid: age should be int
    Traceback (most recent call last):
        ...
    TypeError: Argument 'age' must be <class 'int'>, got <class 'str'>

    >>> @validate_types
    ... def calculate(x: float, y: float, operation: str = "add") -> float:
    ...     if operation == "add":
    ...         return x + y
    ...     return x - y
    
    >>> calculate(1.5, 2.5)  # Valid
    4.0
    >>> calculate("1.5", 2.5)  # Invalid type for x
    Traceback (most recent call last):
        ...
    TypeError: Argument 'x' must be <class 'float'>, got <class 'str'>

Behavior Notes:
    - Uses typing.get_type_hints() to get parameter types
    - Checks each argument against its type hint before calling
    - Only validates arguments that have type hints (others are allowed)
    - Uses isinstance() for type checking
    - Error message format: "Argument '{name}' must be {expected}, got {actual}"

Edge Cases:
    - Functions without type hints are allowed (no validation performed)
    - Optional[X] should accept None or X
    - Union types (X | Y) should accept either X or Y
    - Return type is NOT validated (only inputs)
    - Default values are validated when explicitly passed
"""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any, get_type_hints


def validate_types(func: Callable) -> Callable:
    """A decorator that validates function arguments against type hints.
    
    Checks each argument against its type hint before calling the function.
    Raises TypeError if any argument doesn't match its expected type.
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function with type validation
    """
    raise NotImplementedError("Implement the validate_types decorator")


# Hints for Validate Types Decorator (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to inspect the function's type hints and validate arguments against them.
# Use inspect.signature and the typing module.
#
# Hint 2 - Structural plan:
# - Get function signature with inspect.signature(func)
# - For each parameter, get its annotation
# - In wrapper, check isinstance(arg, annotation) for each argument
# - Raise TypeError with descriptive message if validation fails
# - Handle missing annotations gracefully
#
# Hint 3 - Edge-case warning:
# Complex types like List[int] or Optional[str] need special handling.
# Use typing.get_origin() and typing.get_args() to decompose these types.

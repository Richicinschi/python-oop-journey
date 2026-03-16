"""Problem 08: Deprecated Decorator

Topic: Mark Deprecated Functions
Difficulty: Easy

Create a decorator that marks functions as deprecated and emits warnings.

This demonstrates emitting Python warnings and creating parameterized decorators
for code maintenance. Helps teams migrate away from old APIs by warning
developers at runtime.

Example:
    >>> @deprecated()
    ... def old_function():
    ...     return "I'm old"
    
    >>> old_function()  # Emits DeprecationWarning
    __main__:1: DeprecationWarning: old_function is deprecated
    "I'm old"

    >>> @deprecated("Use new_function() instead")
    ... def legacy_api():
    ...     return "legacy"
    
    >>> legacy_api()  # Emits warning with custom message
    __main__:1: DeprecationWarning: legacy_api is deprecated. Use new_function() instead
    'legacy'

    >>> @deprecated
    ... def bare_decorator():  # Works without parentheses too
    ...     pass

Behavior Notes:
    - Emits warnings.warn() with DeprecationWarning category
    - Default message: "{function_name} is deprecated"
    - Custom message appends to function name: "{name} is deprecated. {message}"
    - Uses stacklevel=2 so warning points to caller's code
    - Function continues to work normally (just warns)

Edge Cases:
    - Works both as @deprecated and @deprecated()
    - Works with @deprecated("custom message")
    - Multiple calls emit multiple warnings (expected behavior)
    - Preserves function metadata using @wraps
    - Warning should be visible in normal execution
"""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any, Optional
import warnings


def deprecated(message: Optional[str] = None) -> Callable:
    """A decorator that marks functions as deprecated.
    
    Emits a DeprecationWarning when the decorated function is called.
    Optionally includes a custom message.
    
    Args:
        message: Optional custom deprecation message
        
    Returns:
        A decorator function
    """
    raise NotImplementedError("Implement the deprecated decorator")


# Hints for Deprecated Decorator (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to emit a DeprecationWarning when the decorated function is called.
# Use warnings.warn() for this.
#
# Hint 2 - Structural plan:
# - Create a decorator factory that accepts an optional message
# - The decorator returns a wrapper function
# - In the wrapper, call warnings.warn() with DeprecationWarning category
# - Include the function name and custom message in the warning
# - Call the original function and return its result
#
# Hint 3 - Edge-case warning:
# Warnings might be suppressed by default. Use stacklevel parameter to ensure
# the warning points to the caller's code, not the decorator.

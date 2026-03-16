"""Problem 02: Scope Chain - Solution."""

from __future__ import annotations

# Global variable
level = "global"


def outer_function() -> str:
    """Return a value from the outer (enclosing) scope.

    Create a local variable 'level' with value "enclosing",
    then call inner_function() and return its result.

    Returns:
        The result from inner_function.
    """
    level = "enclosing"

    def inner_function() -> str:
        """Return the value of level from enclosing scope."""
        # This should access 'level' from outer_function's scope
        return level

    return inner_function()


def read_global() -> str:
    """Read and return the global 'level' variable.

    Returns:
        The value of the global level variable.
    """
    return level

"""Problem 01: Local vs Global - Solution."""

from __future__ import annotations

# Global variable
global_message = "Hello from global"


def get_local_message() -> str:
    """Return a local message.

    Create a local variable named 'message' with value "Hello from local"
    and return it. This should NOT use or modify the global_message.

    Returns:
        The local message string.
    """
    message = "Hello from local"
    return message


def get_global_message() -> str:
    """Return the global message.

    Read and return the value of global_message.
    Do NOT modify the global variable.

    Returns:
        The value of global_message.
    """
    return global_message

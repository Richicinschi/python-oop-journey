"""Problem 02: Safe Convert

Topic: Try and Except
Difficulty: Easy

Write a function that safely converts a string to an integer.

If the conversion fails, return a default value instead.

Examples:
    >>> safe_convert("42", default=0)
    42
    >>> safe_convert("abc", default=-1)
    -1
    >>> safe_convert("", default=0)
    0

Requirements:
    - Return the integer value when conversion succeeds
    - Return the default value when conversion fails
    - The default parameter should have a default value of 0
"""

from __future__ import annotations


def safe_convert(value: str, default: int = 0) -> int:
    """Safely convert a string to an integer.

    Args:
        value: The string to convert
        default: The value to return if conversion fails

    Returns:
        The integer value or the default
    """
    raise NotImplementedError("Implement safe_convert")

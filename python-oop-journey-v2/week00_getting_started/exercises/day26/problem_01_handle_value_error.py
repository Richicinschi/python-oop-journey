"""Problem 01: Handle ValueError

Topic: Common Exceptions
Difficulty: Easy

Write a function that converts a string to a number, handling ValueError.

The function should try to convert to int first, then float.
If both fail, return None.

Examples:
    >>> convert_number("42")
    42
    >>> convert_number("3.14")
    3.14
    >>> convert_number("abc")
    None

Requirements:
    - Try int conversion first, then float
    - Return None if both conversions fail
    - Return the numeric value on success
"""

from __future__ import annotations


def convert_number(value: str) -> int | float | None:
    """Convert a string to a number, handling ValueError.

    Args:
        value: The string to convert

    Returns:
        int if whole number, float if decimal, None if invalid
    """
    raise NotImplementedError("Implement convert_number")

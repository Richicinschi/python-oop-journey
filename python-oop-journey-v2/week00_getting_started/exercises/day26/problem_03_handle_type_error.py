"""Problem 03: Handle TypeError

Topic: Common Exceptions
Difficulty: Medium

Write a function that safely concatenates two strings.

If inputs are not strings, convert them to strings first.
Handle any type of input gracefully.

Examples:
    >>> safe_concat("Hello, ", "World")
    'Hello, World'
    >>> safe_concat("Age: ", 25)
    'Age: 25'
    >>> safe_concat(100, " items")
    '100 items'

Requirements:
    - Concatenate two values as strings
    - Convert non-string inputs to strings
    - Never raise TypeError
"""

from __future__ import annotations


def safe_concat(a: any, b: any) -> str:
    """Safely concatenate two values as strings.

    Args:
        a: First value
        b: Second value

    Returns:
        Concatenated string representation
    """
    raise NotImplementedError("Implement safe_concat")

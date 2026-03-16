"""Problem 01: Check Equality

Topic: Boolean Logic, Comparison Operators
Difficulty: Easy

Write a function that checks if two values are equal.

Examples:
    >>> check_equality(5, 5)
    True
    >>> check_equality(5, 3)
    False
    >>> check_equality("hello", "hello")
    True
    >>> check_equality("hello", "world")
    False

Requirements:
    - Use the equality operator (==)
    - Return a boolean value
"""

from __future__ import annotations


def check_equality(a: int | str | float, b: int | str | float) -> bool:
    """Check if two values are equal.

    Args:
        a: First value to compare
        b: Second value to compare

    Returns:
        True if a equals b, False otherwise
    """
    raise NotImplementedError("Implement check_equality")

"""Problem 02: Is In Range

Topic: Boolean Logic, Comparison Operators
Difficulty: Easy

Write a function that checks if a number is within a specified range [min, max].
The range is inclusive (includes both min and max).

Examples:
    >>> is_in_range(5, 1, 10)
    True
    >>> is_in_range(1, 1, 10)
    True
    >>> is_in_range(10, 1, 10)
    True
    >>> is_in_range(0, 1, 10)
    False
    >>> is_in_range(11, 1, 10)
    False

Requirements:
    - Use comparison operators
    - Return a boolean value
    - The range is inclusive: min <= value <= max
"""

from __future__ import annotations


def is_in_range(value: int, min_val: int, max_val: int) -> bool:
    """Check if value is within the inclusive range [min_val, max_val].

    Args:
        value: The number to check
        min_val: The minimum value of the range (inclusive)
        max_val: The maximum value of the range (inclusive)

    Returns:
        True if value is within range, False otherwise
    """
    raise NotImplementedError("Implement is_in_range")

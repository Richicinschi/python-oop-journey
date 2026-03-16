"""Problem 02: Print Pattern

Topic: For Loops, Nested loops
Difficulty: Easy

Write a function that generates a triangle pattern of asterisks.
Returns a list of strings, each string representing one row.

Examples:
    >>> print_pattern(3)
    ['*', '**', '***']
    >>> print_pattern(1)
    ['*']
    >>> print_pattern(5)
    ['*', '**', '***', '****', '*****']

Requirements:
    - Use nested for loops
    - Return list of strings
    - Row i has i asterisks (1-indexed)
"""

from __future__ import annotations


def print_pattern(n: int) -> list[str]:
    """Generate a triangle pattern of asterisks.

    Args:
        n: Number of rows

    Returns:
        List of strings, each containing asterisks for that row
    """
    raise NotImplementedError("Implement print_pattern")

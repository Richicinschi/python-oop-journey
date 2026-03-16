"""Problem 03: Find Maximum

Topic: If Statements, Nested conditionals
Difficulty: Easy

Write a function that finds the maximum of three numbers without using max().

Examples:
    >>> find_maximum(1, 2, 3)
    3
    >>> find_maximum(5, 2, 3)
    5
    >>> find_maximum(1, 5, 3)
    5
    >>> find_maximum(1, 1, 1)
    1
    >>> find_maximum(-1, -5, -3)
    -1

Requirements:
    - Use if statements (no max() function)
    - Handle all cases including ties
"""

from __future__ import annotations


def find_maximum(a: int | float, b: int | float, c: int | float) -> int | float:
    """Find the maximum of three numbers.

    Args:
        a: First number
        b: Second number
        c: Third number

    Returns:
        The maximum value among a, b, and c
    """
    raise NotImplementedError("Implement find_maximum")

"""Problem 01: Get Number Sign

Topic: If Statements, Conditionals
Difficulty: Easy

Write a function that returns the sign of a number as a string.

Examples:
    >>> get_number_sign(5)
    'positive'
    >>> get_number_sign(-3)
    'negative'
    >>> get_number_sign(0)
    'zero'

Requirements:
    - Use if-elif-else structure
    - Return 'positive', 'negative', or 'zero'
"""

from __future__ import annotations


def get_number_sign(n: int | float) -> str:
    """Return the sign of a number.

    Args:
        n: The number to check

    Returns:
        'positive' if n > 0, 'negative' if n < 0, 'zero' if n == 0
    """
    raise NotImplementedError("Implement get_number_sign")

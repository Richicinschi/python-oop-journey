"""Problem 01: Safe Divide

Topic: Exception Handling
Difficulty: Easy

Write a function that safely divides two numbers, handling division by zero.

Examples:
    >>> safe_divide(10, 2)
    5.0
    >>> safe_divide(10, 0)
    'Error: Division by zero'
    >>> safe_divide(7, 2)
    3.5
    >>> safe_divide(0, 5)
    0.0

Requirements:
    - Return the float result of a / b if b is not zero
    - Return the string 'Error: Division by zero' if b is zero
    - Handle both integer and float inputs
"""

from __future__ import annotations


def safe_divide(a: float, b: float) -> float | str:
    """Safely divide a by b, handling division by zero.

    Args:
        a: The dividend (numerator)
        b: The divisor (denominator)

    Returns:
        The result of a / b as a float, or an error message string
    """
    raise NotImplementedError("Implement safe_divide")

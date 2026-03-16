"""Problem 01: Safe Divide

Topic: Try and Except
Difficulty: Easy

Write a function that safely divides two numbers.

If division by zero occurs, return 0 instead of crashing.
If the inputs are not numbers, return None.

Examples:
    >>> safe_divide(10, 2)
    5.0
    >>> safe_divide(10, 0)
    0
    >>> safe_divide("hello", 2)
    None

Requirements:
    - Return the division result as a float when successful
    - Return 0 when dividing by zero
    - Return None for invalid input types
"""

from __future__ import annotations


def safe_divide(a: float, b: float) -> float | None:
    """Safely divide two numbers, handling errors gracefully.

    Args:
        a: The dividend
        b: The divisor

    Returns:
        The quotient as float, 0 if division by zero, None if invalid input
    """
    raise NotImplementedError("Implement safe_divide")

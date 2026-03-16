"""Reference solution for Problem 03: Factorial."""

from __future__ import annotations


def factorial(n: int) -> int:
    """Calculate n! using recursion.
    
    Args:
        n: A non-negative integer
        
    Returns:
        The factorial of n
        
    Raises:
        ValueError: If n is negative
        
    Examples:
        >>> factorial(0)
        1
        >>> factorial(3)
        6
        >>> factorial(5)
        120
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

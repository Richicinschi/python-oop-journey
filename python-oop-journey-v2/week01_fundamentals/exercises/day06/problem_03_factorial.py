"""Problem 03: Factorial

Topic: Recursion
Difficulty: Easy

Calculate the factorial of a number using recursion.

The factorial of n (written as n!) is:
- 0! = 1 (by definition)
- n! = n × (n-1) × (n-2) × ... × 1 for n > 0

Example:
    factorial(0) → 1
    factorial(3) → 6   (3 × 2 × 1)
    factorial(5) → 120 (5 × 4 × 3 × 2 × 1)

Requirements:
    - Use recursion (function calling itself)
    - Handle negative inputs by raising ValueError
    - factorial(0) should return 1
"""

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
    raise NotImplementedError("Implement factorial")

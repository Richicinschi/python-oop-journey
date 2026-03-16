"""Problem 04: Power Recursive

Topic: Recursion
Difficulty: Easy

Calculate x raised to the power n (x^n) using recursion.

Implement efficient recursive exponentiation using the property:
- x^n = x^(n/2) × x^(n/2) when n is even
- x^n = x × x^((n-1)/2) × x^((n-1)/2) when n is odd

Example:
    power(2, 0) → 1      (any number^0 = 1)
    power(2, 3) → 8      (2 × 2 × 2)
    power(3, 4) → 81     (3 × 3 × 3 × 3)
    power(2, -3) → 0.125 (1/8)

Requirements:
    - Use recursion with divide-and-conquer approach
    - Handle negative exponents (return float result)
    - x^0 should return 1 for any x (including 0)
    - Optimize using the even/odd property to reduce recursive calls

Note: This approach has O(log n) time complexity.
"""

from __future__ import annotations


def power(x: float, n: int) -> float:
    """Calculate x^n using recursive divide-and-conquer.
    
    Args:
        x: The base number
        n: The exponent (can be negative)
        
    Returns:
        x raised to the power n
        
    Examples:
        >>> power(2, 3)
        8.0
        >>> power(2, -2)
        0.25
        >>> power(5, 0)
        1.0
    """
    raise NotImplementedError("Implement power")

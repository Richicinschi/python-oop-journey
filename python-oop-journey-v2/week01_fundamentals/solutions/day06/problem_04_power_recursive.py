"""Reference solution for Problem 04: Power Recursive."""

from __future__ import annotations


def power(x: float, n: int) -> float:
    """Calculate x^n using recursive divide-and-conquer.
    
    Uses the property that x^n = (x^(n/2))^2 for even n,
    reducing time complexity from O(n) to O(log n).
    
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
    # Base case: anything^0 = 1
    if n == 0:
        return 1.0
    
    # Handle negative exponent: x^(-n) = 1/(x^n)
    if n < 0:
        return 1.0 / power(x, -n)
    
    # Recursive case: use divide and conquer
    half = power(x, n // 2)
    
    if n % 2 == 0:
        # Even: x^n = (x^(n/2))^2
        return half * half
    else:
        # Odd: x^n = x * (x^((n-1)/2))^2
        return x * half * half

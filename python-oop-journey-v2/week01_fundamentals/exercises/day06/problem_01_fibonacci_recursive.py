"""Problem 01: Fibonacci Recursive

Topic: Recursion
Difficulty: Easy

Calculate the nth Fibonacci number using a naive recursive approach.

The Fibonacci sequence is defined as:
- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) for n > 1

Example:
    fibonacci(0) → 0
    fibonacci(1) → 1
    fibonacci(6) → 8  (0, 1, 1, 2, 3, 5, 8)
    fibonacci(10) → 55

Requirements:
    - Use recursion (function calling itself)
    - Handle negative inputs by raising ValueError
    - This is the naive version - do NOT use memoization here

Note: This naive approach has exponential time complexity O(2^n).
Compare with the memoized version in the next problem.
"""

from __future__ import annotations


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number using naive recursion.
    
    Args:
        n: The position in the Fibonacci sequence (0-indexed)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
        
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(6)
        8
    """
    raise NotImplementedError("Implement fibonacci")

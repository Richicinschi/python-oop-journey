"""Problem 02: Fibonacci Memoized

Topic: Recursion with Memoization
Difficulty: Easy

Calculate the nth Fibonacci number efficiently using memoization.

The Fibonacci sequence is defined as:
- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) for n > 1

Example:
    fibonacci_memoized(0) → 0
    fibonacci_memoized(6) → 8
    fibonacci_memoized(50) → 12586269025

Requirements:
    - Use recursion with memoization to avoid redundant calculations
    - Store computed values in a dictionary
    - Handle negative inputs by raising ValueError
    - The memo parameter should be optional with default None

Note: This approach has O(n) time and space complexity.
Compare performance with the naive recursive version.
"""

from __future__ import annotations


def fibonacci_memoized(n: int, memo: dict[int, int] | None = None) -> int:
    """Calculate the nth Fibonacci number using memoized recursion.
    
    Args:
        n: The position in the Fibonacci sequence (0-indexed)
        memo: Dictionary to store computed values (optional)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
        
    Examples:
        >>> fibonacci_memoized(0)
        0
        >>> fibonacci_memoized(6)
        8
        >>> fibonacci_memoized(50)
        12586269025
    """
    raise NotImplementedError("Implement fibonacci_memoized")

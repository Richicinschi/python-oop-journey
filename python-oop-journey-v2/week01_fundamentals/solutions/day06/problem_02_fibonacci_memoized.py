"""Reference solution for Problem 02: Fibonacci Memoized."""

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
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # Initialize memo dict if not provided
    if memo is None:
        memo = {}
    
    # Check if already computed
    if n in memo:
        return memo[n]
    
    # Base cases
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # Compute and store
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]

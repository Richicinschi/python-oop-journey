"""Problem 05: Maximum of Three Numbers

Topic: Functions - Multiple Parameters
Difficulty: Easy

Write a function that finds the maximum of three numbers.

Function Signature:
    def max_of_three(a: int, b: int, c: int) -> int

Requirements:
    - Return the largest of the three numbers
    - Works with positive and negative integers

Behavior Notes:
    - Compare all three values
    - Can use nested max() calls: max(a, max(b, c))
    - Or use max(a, b, c)
    - All three equal: return that value

Examples:
    >>> max_of_three(1, 5, 3)
    5
    
    >>> max_of_three(10, 2, 8)
    10
    
    All equal:
    >>> max_of_three(7, 7, 7)
    7
    
    Negative numbers:
    >>> max_of_three(-5, -2, -10)
    -2

Input Validation:
    - You may assume a, b, c are integers

"""

from __future__ import annotations


def max_of_three(a: int, b: int, c: int) -> int:
    """Return the maximum of three numbers.

    Args:
        a: First number.
        b: Second number.
        c: Third number.

    Returns:
        The largest of the three numbers.
    """
    raise NotImplementedError("Implement max_of_three")

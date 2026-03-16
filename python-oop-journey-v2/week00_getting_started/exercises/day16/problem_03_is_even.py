"""Problem 03: Is Even

Topic: Functions - Boolean Return Values
Difficulty: Easy

Write a function that checks if a number is even.

Function Signature:
    def is_even(number: int) -> bool

Requirements:
    - Return True if the number is even
    - Return False if the number is odd
    - Zero is considered even

Behavior Notes:
    - Even numbers are divisible by 2 with no remainder
    - Use modulo operator: number % 2 == 0
    - Zero % 2 == 0, so zero is even

Examples:
    >>> is_even(4)
    True
    
    >>> is_even(7)
    False
    
    Zero:
    >>> is_even(0)
    True
    
    Negative numbers:
    >>> is_even(-4)
    True
    
    >>> is_even(-7)
    False

Input Validation:
    - You may assume number is an integer

"""

from __future__ import annotations


def is_even(number: int) -> bool:
    """Check if a number is even.

    Args:
        number: The number to check.

    Returns:
        True if even, False if odd.
    """
    raise NotImplementedError("Implement is_even")

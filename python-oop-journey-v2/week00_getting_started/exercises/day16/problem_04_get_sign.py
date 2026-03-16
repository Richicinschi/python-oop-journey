"""Problem 04: Get Number Sign

Topic: Functions - Multiple Return Paths
Difficulty: Easy

Write a function that returns the sign of a number.

Function Signature:
    def get_sign(number: int) -> str

Requirements:
    - Return "positive" for numbers > 0
    - Return "negative" for numbers < 0
    - Return "zero" for number == 0

Behavior Notes:
    - Three distinct cases with different return values
    - Zero is neither positive nor negative
    - Use if/elif/else structure

Examples:
    >>> get_sign(10)
    'positive'
    
    >>> get_sign(-5)
    'negative'
    
    Zero:
    >>> get_sign(0)
    'zero'
    
    Large numbers:
    >>> get_sign(1000000)
    'positive'

Input Validation:
    - You may assume number is an integer

"""

from __future__ import annotations


def get_sign(number: int) -> str:
    """Return the sign of a number.

    Args:
        number: The number to check.

    Returns:
        "positive", "negative", or "zero".
    """
    raise NotImplementedError("Implement get_sign")

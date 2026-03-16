"""Problem 02: Swap Variables Using Tuples

Topic: Tuples - Variable Swapping
Difficulty: Easy

Write a function that swaps two values using tuple unpacking.

Function Signature:
    def swap_values(a: int, b: int) -> tuple[int, int]

Requirements:
    - Return a tuple with values swapped (b, a)
    - Use tuple unpacking for the swap
    - Works with any integers

Behavior Notes:
    - Python allows simultaneous assignment: a, b = b, a
    - This uses tuple packing/unpacking
    - Return the swapped values as a tuple

Examples:
    >>> swap_values(5, 10)
    (10, 5)
    
    >>> swap_values(1, 2)
    (2, 1)
    
    Same values:
    >>> swap_values(5, 5)
    (5, 5)
    
    Negative numbers:
    >>> swap_values(-3, 7)
    (7, -3)

Input Validation:
    - You may assume a and b are integers

"""

from __future__ import annotations


def swap_values(a: int, b: int) -> tuple[int, int]:
    """Swap two values using tuple unpacking.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        A tuple with values swapped (b, a).
    """
    raise NotImplementedError("Implement swap_values")

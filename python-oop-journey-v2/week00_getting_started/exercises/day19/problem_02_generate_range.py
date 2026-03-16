"""Problem 02: Generate Range

Topic: Built-in Functions - range()
Difficulty: Easy

Write a function that generates a range of numbers with various options.

Function Signature:
    def generate_range(start: int, stop: int, step: int = 1) -> list[int]

Requirements:
    - Return a list of numbers from start to stop (exclusive)
    - Use the given step size
    - Match Python's range() behavior

Behavior Notes:
    - range(stop) goes from 0 to stop-1
    - range(start, stop) goes from start to stop-1
    - range(start, stop, step) uses step increment
    - Empty result if start >= stop (with positive step)

Examples:
    >>> generate_range(0, 5)
    [0, 1, 2, 3, 4]
    
    >>> generate_range(2, 10, 2)
    [2, 4, 6, 8]
    
    Empty range:
    >>> generate_range(5, 0)
    []
    
    Negative step:
    >>> generate_range(5, 0, -1)
    [5, 4, 3, 2, 1]

Input Validation:
    - You may assume all arguments are integers
    - step will not be zero

"""

from __future__ import annotations


def generate_range(start: int, stop: int, step: int = 1) -> list[int]:
    """Generate a range of numbers.

    Args:
        start: Starting value (inclusive).
        stop: Ending value (exclusive).
        step: Increment (default 1).

    Returns:
        A list of integers in the range.
    """
    raise NotImplementedError("Implement generate_range")

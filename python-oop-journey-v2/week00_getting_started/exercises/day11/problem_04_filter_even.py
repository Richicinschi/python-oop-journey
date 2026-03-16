"""Problem 04: Filter Even

Topic: For Loops, List building
Difficulty: Easy

Write a function that returns a new list containing only the even numbers
from the input list.

Examples:
    >>> filter_even([1, 2, 3, 4, 5])
    [2, 4]
    >>> filter_even([10, 20, 30])
    [10, 20, 30]
    >>> filter_even([1, 3, 5])
    []
    >>> filter_even([])
    []

Requirements:
    - Use a for loop to iterate
    - Use modulo operator to check even
    - Return a new list
"""

from __future__ import annotations


def filter_even(numbers: list[int]) -> list[int]:
    """Filter list to keep only even numbers.

    Args:
        numbers: List of integers

    Returns:
        New list containing only even numbers from input
    """
    raise NotImplementedError("Implement filter_even")

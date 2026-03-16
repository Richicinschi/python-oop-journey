"""Problem 03: Tuple Statistics

Topic: Tuples - Aggregation
Difficulty: Easy

Write a function that calculates statistics for a tuple of numbers.

Function Signature:
    def tuple_stats(numbers: tuple[int, ...]) -> dict[str, float | int]

Requirements:
    - Calculate sum, count, average, min, and max
    - Return a dictionary with these statistics
    - Handle empty tuple (return zeros/empty values)

Behavior Notes:
    - Return count=0, sum=0, avg=0.0, min=None, max=None for empty tuple
    - Average is sum / count as float
    - Use built-in functions: sum(), len(), min(), max()

Examples:
    >>> tuple_stats((1, 2, 3, 4, 5))
    {'count': 5, 'sum': 15, 'average': 3.0, 'min': 1, 'max': 5}
    
    Single element:
    >>> tuple_stats((42,))
    {'count': 1, 'sum': 42, 'average': 42.0, 'min': 42, 'max': 42}
    
    Empty tuple:
    >>> tuple_stats(())
    {'count': 0, 'sum': 0, 'average': 0.0, 'min': None, 'max': None}

Input Validation:
    - You may assume numbers is a tuple of integers
    - Handle empty tuple gracefully

"""

from __future__ import annotations


def tuple_stats(numbers: tuple[int, ...]) -> dict[str, float | int]:
    """Calculate statistics for a tuple of numbers.

    Args:
        numbers: A tuple of integers.

    Returns:
        A dictionary with count, sum, average, min, and max.
    """
    raise NotImplementedError("Implement tuple_stats")

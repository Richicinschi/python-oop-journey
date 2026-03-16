"""Problem 04: Calculate Average

Topic: Try and Except
Difficulty: Medium

Write a function that calculates the average of a list of numbers.

Handle these cases gracefully:
- Empty list: return 0
- List contains non-numbers: skip them
- Division by zero: return 0

Examples:
    >>> calculate_average([1, 2, 3, 4])
    2.5
    >>> calculate_average([])
    0
    >>> calculate_average([1, "two", 3])
    2.0

Requirements:
    - Return the average as a float
    - Handle empty lists by returning 0
    - Skip non-numeric values
    - All numeric types (int, float) should be accepted
"""

from __future__ import annotations


def calculate_average(numbers: list) -> float:
    """Calculate the average of a list of numbers.

    Args:
        numbers: A list containing numbers (and possibly other types)

    Returns:
        The average as a float, or 0 if no valid numbers
    """
    raise NotImplementedError("Implement calculate_average")

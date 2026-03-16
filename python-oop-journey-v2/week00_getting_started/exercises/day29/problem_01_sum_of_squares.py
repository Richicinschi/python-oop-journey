"""Problem 01: Sum of Squares with Validation

Topic: Functions, loops, validation
Difficulty: Easy

Write a function that calculates the sum of squares of numbers in a list,
with proper input validation and error handling.

Required functions:
- sum_of_squares(numbers): Calculate sum of squares with validation
- sum_of_squares_safe(numbers): Return None for invalid inputs instead of raising

Validation rules:
- All elements must be numeric (int or float)
- Return 0 for empty list
- Raise ValueError for invalid inputs (in the main function)

Examples:
    >>> sum_of_squares([1, 2, 3])
    14  # 1 + 4 + 9
    >>> sum_of_squares([2.5, 3.0])
    15.25  # 6.25 + 9.0
    >>> sum_of_squares([])
    0
    >>> sum_of_squares([1, "two", 3])
    ValueError: All elements must be numeric
"""

from __future__ import annotations


def sum_of_squares(numbers: list) -> int | float:
    """Calculate the sum of squares of numbers with validation.

    Args:
        numbers: A list of numbers (int or float)

    Returns:
        The sum of squares of all numbers

    Raises:
        ValueError: If any element is not numeric
    """
    raise NotImplementedError("Implement sum_of_squares")


def sum_of_squares_safe(numbers: list) -> int | float | None:
    """Calculate sum of squares, returning None for invalid inputs.

    Args:
        numbers: A list of numbers (int or float)

    Returns:
        The sum of squares, or None if input is invalid
    """
    raise NotImplementedError("Implement sum_of_squares_safe")

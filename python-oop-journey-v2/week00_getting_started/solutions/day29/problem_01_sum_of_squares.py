"""Reference solution for Problem 01: Sum of Squares with Validation."""

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
    total = 0
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise ValueError("All elements must be numeric")
        total += num * num
    return total


def sum_of_squares_safe(numbers: list) -> int | float | None:
    """Calculate sum of squares, returning None for invalid inputs.

    Args:
        numbers: A list of numbers (int or float)

    Returns:
        The sum of squares, or None if input is invalid
    """
    try:
        return sum_of_squares(numbers)
    except ValueError:
        return None

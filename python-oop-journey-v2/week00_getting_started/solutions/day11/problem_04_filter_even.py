"""Reference solution for Problem 04: Filter Even."""

from __future__ import annotations


def filter_even(numbers: list[int]) -> list[int]:
    """Filter list to keep only even numbers.

    Args:
        numbers: List of integers

    Returns:
        New list containing only even numbers from input
    """
    result: list[int] = []
    for num in numbers:
        if num % 2 == 0:
            result.append(num)
    return result

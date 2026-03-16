"""Reference solution for Problem 04: Find Maximum."""

from __future__ import annotations


def find_max(numbers: list[int]) -> int | None:
    """Find the maximum value in a list.

    Args:
        numbers: A list of integers

    Returns:
        The maximum value, or None if the list is empty
    """
    if not numbers:
        return None
    
    maximum = numbers[0]
    for num in numbers[1:]:
        if num > maximum:
            maximum = num
    return maximum

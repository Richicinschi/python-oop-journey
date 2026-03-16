"""Reference solution for Problem 02: Find The Bug."""

from __future__ import annotations


def find_max(numbers: list) -> int | None:
    """Find the maximum value in a list.

    Args:
        numbers: A list of numbers

    Returns:
        The maximum value, or None if list is empty
    """
    if not numbers:
        return None
    
    # Fixed: Initialize with first element instead of 0
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

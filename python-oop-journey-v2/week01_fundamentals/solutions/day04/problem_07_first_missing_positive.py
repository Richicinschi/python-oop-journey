"""Reference solution for Problem 07: First Missing Positive."""

from __future__ import annotations


def first_missing_positive(nums: list[int]) -> int:
    """Find the smallest missing positive integer.

    Uses a hash set for O(1) existence checks. Starting from 1,
    find the first positive integer not in the set.

    Note: The optimal O(1) space solution uses array indices as hash.

    Time Complexity: O(n)
    Space Complexity: O(n)

    Args:
        nums: List of integers (may contain negative numbers and duplicates)

    Returns:
        Smallest positive integer (>= 1) not present in the array
    """
    num_set = set(nums)

    # Start from 1 and find first missing positive
    candidate = 1
    while candidate in num_set:
        candidate += 1

    return candidate

"""Problem 07: First Missing Positive

Topic: Hash Set, Array
Difficulty: Hard

Given an unsorted integer array, return the smallest missing positive integer.

The algorithm must run in O(n) time and use O(1) auxiliary space.

Note: For this exercise, O(n) space complexity using a hash set is acceptable.
The optimal O(1) space solution uses array indices as a hash.
"""

from __future__ import annotations


def first_missing_positive(nums: list[int]) -> int:
    """Find the smallest missing positive integer.

    Args:
        nums: List of integers (may contain negative numbers and duplicates)

    Returns:
        Smallest positive integer (>= 1) not present in the array

    Example:
        >>> first_missing_positive([1, 2, 0])
        3
        >>> first_missing_positive([3, 4, -1, 1])
        2
        >>> first_missing_positive([7, 8, 9, 11, 12])
        1
    """
    raise NotImplementedError("Implement first_missing_positive")

"""Problem 04: Longest Consecutive Sequence

Topic: Hash Set, Sequence
Difficulty: Medium

Given an unsorted array of integers, return the length of the longest
consecutive elements sequence.

The algorithm must run in O(n) time complexity.
"""

from __future__ import annotations


def longest_consecutive_sequence(nums: list[int]) -> int:
    """Find length of longest consecutive elements sequence.

    Args:
        nums: List of integers (unsorted, may contain duplicates)

    Returns:
        Length of longest consecutive sequence

    Example:
        >>> longest_consecutive_sequence([100, 4, 200, 1, 3, 2])
        4
        >>> longest_consecutive_sequence([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])
        9
    """
    raise NotImplementedError("Implement longest_consecutive_sequence")

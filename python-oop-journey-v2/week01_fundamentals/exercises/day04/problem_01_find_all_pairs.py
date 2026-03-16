"""Problem 01: Find All Pairs

Topic: Hash Map, Two Sum
Difficulty: Easy

Given a list of integers and a target value, find all unique pairs of numbers
that sum to the target value.

Each pair should be returned as a tuple with the smaller number first.
Each number can only be used in one pair.
"""

from __future__ import annotations


def find_all_pairs(nums: list[int], target: int) -> list[tuple[int, int]]:
    """Find all unique pairs that sum to target.

    Args:
        nums: List of integers to search
        target: Target sum value

    Returns:
        List of tuples, each containing a pair that sums to target.
        Each tuple has smaller number first. No duplicate pairs.

    Example:
        >>> find_all_pairs([1, 2, 3, 4, 5], 5)
        [(1, 4), (2, 3)]
        >>> find_all_pairs([1, 1, 1, 1], 2)
        [(1, 1)]
    """
    raise NotImplementedError("Implement find_all_pairs")

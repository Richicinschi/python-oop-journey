"""Problem 03: Top K Frequent Elements

Topic: Hash Map, Heap, Sorting
Difficulty: Medium

Given an integer array and an integer k, return the k most frequent elements.

You may return the answer in any order.
"""

from __future__ import annotations


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """Return the k most frequent elements.

    Args:
        nums: List of integers
        k: Number of most frequent elements to return

    Returns:
        List of k most frequent elements (order does not matter)

    Example:
        >>> sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2))
        [1, 2]
        >>> top_k_frequent([1], 1)
        [1]
    """
    raise NotImplementedError("Implement top_k_frequent")

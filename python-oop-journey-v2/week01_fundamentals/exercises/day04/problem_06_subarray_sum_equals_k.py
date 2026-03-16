"""Problem 06: Subarray Sum Equals K

Topic: Hash Map, Prefix Sum
Difficulty: Medium

Given an array of integers and an integer k, return the total number of
continuous subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.
"""

from __future__ import annotations


def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    """Count subarrays with sum equal to k.

    Args:
        nums: List of integers
        k: Target sum

    Returns:
        Number of subarrays with sum equal to k

    Example:
        >>> subarray_sum_equals_k([1, 1, 1], 2)
        2
        >>> subarray_sum_equals_k([1, 2, 3], 3)
        2
    """
    raise NotImplementedError("Implement subarray_sum_equals_k")

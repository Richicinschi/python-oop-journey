"""Reference solution for Problem 01: Two Sum List."""

from __future__ import annotations


def two_sum(nums: list[int], target: int) -> list[int]:
    """Return indices of two numbers that add up to target.

    Uses a hash map (dictionary) to achieve O(n) time complexity.
    For each number, we check if the complement (target - num) was seen before.

    Args:
        nums: List of integers.
        target: Target sum.

    Returns:
        List containing two indices whose values sum to target.

    Time Complexity: O(n) - single pass through the list
    Space Complexity: O(n) - hash map stores at most n elements
    """
    seen: dict[int, int] = {}  # value -> index mapping

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    # According to constraints, exactly one solution exists
    return []

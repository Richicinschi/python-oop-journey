"""Reference solution for Problem 03: Rotate Array."""

from __future__ import annotations


def rotate(nums: list[int], k: int) -> None:
    """Rotate array to the right by k steps using reversal algorithm.

    Algorithm:
    1. Reverse the entire array
    2. Reverse the first k elements
    3. Reverse the remaining n-k elements

    Example: [1, 2, 3, 4, 5, 6, 7], k = 3
    1. Reverse all: [7, 6, 5, 4, 3, 2, 1]
    2. Reverse first 3: [5, 6, 7, 4, 3, 2, 1]
    3. Reverse rest: [5, 6, 7, 1, 2, 3, 4]

    Args:
        nums: List of integers (modified in-place).
        k: Number of steps to rotate right.

    Time Complexity: O(n) - three reversals
    Space Complexity: O(1) - in-place
    """
    n = len(nums)
    if n == 0:
        return

    # Handle k > n
    k = k % n

    if k == 0:
        return

    def reverse(start: int, end: int) -> None:
        """Reverse elements from start to end (inclusive)."""
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1

    # Reverse entire array
    reverse(0, n - 1)
    # Reverse first k elements
    reverse(0, k - 1)
    # Reverse remaining n-k elements
    reverse(k, n - 1)

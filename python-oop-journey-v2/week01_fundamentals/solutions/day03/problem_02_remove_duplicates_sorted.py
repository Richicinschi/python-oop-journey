"""Reference solution for Problem 02: Remove Duplicates from Sorted Array."""

from __future__ import annotations


def remove_duplicates(nums: list[int]) -> int:
    """Remove duplicates from sorted array in-place using two-pointer technique.

    Uses a slow pointer to track the position for the next unique element,
    and a fast pointer to scan through the array.

    Args:
        nums: Sorted list of integers (modified in-place).

    Returns:
        The number of unique elements (k).

    Time Complexity: O(n) - single pass through the array
    Space Complexity: O(1) - only using two pointers
    """
    if not nums:
        return 0

    # slow pointer - position to place next unique element
    slow = 0

    # fast pointer - scans through the array
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]

    # Number of unique elements is slow + 1
    return slow + 1

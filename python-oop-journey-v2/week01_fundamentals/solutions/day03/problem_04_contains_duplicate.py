"""Reference solution for Problem 04: Contains Duplicate."""

from __future__ import annotations


def contains_duplicate(nums: list[int]) -> bool:
    """Check if list contains any duplicates using a set.

    Uses a set to track seen elements. If we encounter an element already
    in the set, we found a duplicate.

    Args:
        nums: List of integers.

    Returns:
        True if any value appears at least twice, False otherwise.

    Time Complexity: O(n) - single pass through list
    Space Complexity: O(n) - set stores up to n elements
    """
    seen: set[int] = set()

    for num in nums:
        if num in seen:
            return True
        seen.add(num)

    return False


def contains_duplicate_sort(nums: list[int]) -> bool:
    """Alternative solution using sorting (O(1) space but O(n log n) time).

    Sorts the array first, then checks adjacent elements for duplicates.

    Args:
        nums: List of integers.

    Returns:
        True if any value appears at least twice, False otherwise.

    Time Complexity: O(n log n) - due to sorting
    Space Complexity: O(1) or O(n) depending on sort implementation
    """
    nums_sorted = sorted(nums)

    for i in range(1, len(nums_sorted)):
        if nums_sorted[i] == nums_sorted[i - 1]:
            return True

    return False

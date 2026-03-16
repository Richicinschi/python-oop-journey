"""Reference solution for Problem 06: Merge Sorted Arrays."""

from __future__ import annotations


def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    """Merge nums2 into nums1 in-place using three-pointer technique.

    Strategy: Fill from the end to avoid overwriting elements in nums1.
    - Start from the end of both arrays
    - Compare elements and place the larger one at the end of nums1
    - Work backwards until all elements are merged

    Args:
        nums1: First sorted array with enough space at the end (modified in-place).
        m: Number of elements in nums1 (excluding trailing zeros).
        nums2: Second sorted array.
        n: Number of elements in nums2.

    Time Complexity: O(m + n) - single pass through both arrays
    Space Complexity: O(1) - in-place
    """
    # Pointers for the end of valid elements in each array
    i = m - 1  # Last element in nums1
    j = n - 1  # Last element in nums2
    k = m + n - 1  # Last position in merged array

    # Merge from the back
    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1

    # If there are remaining elements in nums2, copy them
    # (if nums1 has remaining elements, they're already in place)
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1


def merge_simple(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    """Alternative simple solution (not O(1) space due to slicing).

    Args:
        nums1: First sorted array (modified in-place).
        m: Number of elements in nums1.
        nums2: Second sorted array.
        n: Number of elements in nums2.
    """
    # Copy nums2 into the end of nums1
    nums1[m:m + n] = nums2
    # Sort the entire array
    nums1.sort()

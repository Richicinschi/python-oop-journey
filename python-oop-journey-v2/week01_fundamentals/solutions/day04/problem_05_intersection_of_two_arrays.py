"""Reference solution for Problem 05: Intersection of Two Arrays."""

from __future__ import annotations


def intersection_of_two_arrays(nums1: list[int], nums2: list[int]) -> list[int]:
    """Find intersection of two arrays.

    Converts both lists to sets and uses set intersection.

    Time Complexity: O(n + m) where n, m are lengths of the arrays
    Space Complexity: O(min(n, m)) for the result

    Args:
        nums1: First list of integers
        nums2: Second list of integers

    Returns:
        List of unique elements present in both arrays
    """
    set1 = set(nums1)
    set2 = set(nums2)
    return list(set1 & set2)

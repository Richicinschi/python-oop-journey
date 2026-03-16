"""Reference solution for Problem 08: Find Minimum in Rotated Sorted Array."""

from __future__ import annotations


def find_min(nums: list[int]) -> int:
    """Find minimum element in rotated sorted array using binary search.

    Key insight: In a rotated sorted array, the minimum element is the
    only element that is smaller than its previous element. We can use
    binary search to find it in O(log n) time.

    At any middle element:
    - If nums[mid] > nums[right]: Minimum must be in right half (including mid+1 to right)
    - If nums[mid] < nums[right]: Minimum must be in left half (including left to mid)
    - Since all elements are unique, nums[mid] == nums[right] never happens

    Args:
        nums: Rotated sorted array of unique elements.

    Returns:
        The minimum element.

    Time Complexity: O(log n) - binary search
    Space Complexity: O(1) - iterative approach
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        # Compare mid element with rightmost element
        if nums[mid] > nums[right]:
            # Minimum is in right half (after mid)
            left = mid + 1
        else:  # nums[mid] < nums[right]
            # nums[mid] is smaller than right, so minimum is at mid or to the left
            # Note: can't be mid+1 to right, so search left half including mid
            right = mid

    return nums[left]


def find_min_with_pivot(nums: list[int]) -> int:
    """Alternative: Find the pivot (rotation point) where array was rotated.

    The pivot is where nums[i] > nums[i+1], and nums[i+1] is the minimum.

    Args:
        nums: Rotated sorted array.

    Returns:
        The minimum element.
    """
    # If array is not rotated at all
    if nums[0] <= nums[-1]:
        return nums[0]

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        # Check if mid is the pivot
        if mid < len(nums) - 1 and nums[mid] > nums[mid + 1]:
            return nums[mid + 1]

        # Decide which half to search
        if nums[mid] >= nums[0]:
            # Still in left (larger) portion, go right
            left = mid + 1
        else:
            # In right (smaller) portion, go left
            right = mid - 1

    return nums[0]

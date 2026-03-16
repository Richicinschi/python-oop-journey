"""Reference solution for Problem 10: Container With Most Water."""

from __future__ import annotations


def max_area(height: list[int]) -> int:
    """Find maximum water container area using two-pointer technique.

    Algorithm:
    - Start with two pointers at both ends (widest container)
    - Calculate area: width * min(height[left], height[right])
    - Move the pointer with smaller height inward (since moving the taller
      one won't increase area - width decreases and height is limited by
      the shorter line)
    - Track maximum area seen

    Args:
        height: List where height[i] represents the height of line at position i.

    Returns:
        Maximum area of water that can be contained.

    Time Complexity: O(n) - single pass with two pointers
    Space Complexity: O(1) - only tracking pointers and max area
    """
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        # Calculate current area
        width = right - left
        current_height = min(height[left], height[right])
        current_area = width * current_height

        # Update maximum
        max_water = max(max_water, current_area)

        # Move the pointer with smaller height
        # (moving the taller one can't increase area)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water


def max_area_brute_force(height: list[int]) -> int:
    """Brute force solution for comparison (O(n^2)).

    Args:
        height: List of heights.

    Returns:
        Maximum area.
    """
    n = len(height)
    max_water = 0

    for i in range(n):
        for j in range(i + 1, n):
            area = (j - i) * min(height[i], height[j])
            max_water = max(max_water, area)

    return max_water

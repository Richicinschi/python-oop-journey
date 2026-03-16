"""Reference solution for Problem 05: Maximum Subarray."""

from __future__ import annotations


def max_subarray_sum(nums: list[int]) -> int:
    """Find the maximum sum of any contiguous subarray using Kadane's algorithm.

    Kadane's Algorithm:
    - Track the maximum sum ending at each position
    - At each element, decide whether to:
      a) Start a new subarray at current element, or
      b) Extend the existing subarray
    - Keep track of the overall maximum

    Args:
        nums: List of integers.

    Returns:
        Maximum sum of any contiguous subarray.

    Time Complexity: O(n) - single pass
    Space Complexity: O(1) - only tracking two values
    """
    if not nums:
        return 0

    # Initialize with first element
    current_sum = max_sum = nums[0]

    for num in nums[1:]:
        # Either start new subarray at current num or extend existing
        current_sum = max(num, current_sum + num)
        # Update global maximum
        max_sum = max(max_sum, current_sum)

    return max_sum


def max_subarray_with_indices(nums: list[int]) -> tuple[int, int, int]:
    """Extended version that also returns start and end indices.

    Args:
        nums: List of integers.

    Returns:
        Tuple of (max_sum, start_index, end_index).
    """
    if not nums:
        return 0, -1, -1

    current_sum = max_sum = nums[0]
    current_start = max_start = max_end = 0

    for i, num in enumerate(nums[1:], start=1):
        if num > current_sum + num:
            current_sum = num
            current_start = i
        else:
            current_sum += num

        if current_sum > max_sum:
            max_sum = current_sum
            max_start = current_start
            max_end = i

    return max_sum, max_start, max_end

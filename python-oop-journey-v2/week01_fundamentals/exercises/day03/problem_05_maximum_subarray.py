"""Problem 05: Maximum Subarray (Kadane's Algorithm)

Topic: Lists, Dynamic Programming
Difficulty: Medium

Given an integer array `nums`, find the contiguous subarray (containing at
least one number) which has the largest sum and return its sum.

A subarray is a contiguous part of an array.

Example 1:
    Input: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    Output: 6
    Explanation: [4, -1, 2, 1] has the largest sum = 6

Example 2:
    Input: nums = [1]
    Output: 1

Example 3:
    Input: nums = [5, 4, -1, 7, 8]
    Output: 23
    Explanation: [5, 4, -1, 7, 8] has the largest sum = 23

Constraints:
    - 1 <= len(nums) <= 10^5
    - -10^4 <= nums[i] <= 10^4

Follow up:
    - If you have figured out the O(n) solution, try coding another solution
      using the divide and conquer approach, which is more subtle.
"""

from __future__ import annotations


def max_subarray_sum(nums: list[int]) -> int:
    """Find the maximum sum of any contiguous subarray.

    Args:
        nums: List of integers.

    Returns:
        Maximum sum of any contiguous subarray.
    """
    raise NotImplementedError("Implement max_subarray_sum")

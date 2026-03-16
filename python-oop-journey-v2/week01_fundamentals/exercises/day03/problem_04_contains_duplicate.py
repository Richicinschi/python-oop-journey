"""Problem 04: Contains Duplicate

Topic: Lists, Sets
Difficulty: Easy

Given an integer array `nums`, return `True` if any value appears at least
twice in the array, and return `False` if every element is distinct.

Example 1:
    Input: nums = [1, 2, 3, 1]
    Output: True

Example 2:
    Input: nums = [1, 2, 3, 4]
    Output: False

Example 3:
    Input: nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
    Output: True

Constraints:
    - 1 <= len(nums) <= 10^5
    - -10^9 <= nums[i] <= 10^9

Follow up:
    - Can you solve this with O(n) time and O(1) space using sorting?
"""

from __future__ import annotations


def contains_duplicate(nums: list[int]) -> bool:
    """Check if list contains any duplicates.

    Args:
        nums: List of integers.

    Returns:
        True if any value appears at least twice, False otherwise.
    """
    raise NotImplementedError("Implement contains_duplicate")

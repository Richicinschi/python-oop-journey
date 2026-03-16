"""Problem 06: Merge Sorted Arrays

Topic: Lists, Two Pointers
Difficulty: Easy

You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing
order, and two integers `m` and `n`, representing the number of elements in
`nums1` and `nums2` respectively.

Merge `nums1` and `nums2` into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead be
stored inside the array `nums1`. To accommodate this, `nums1` has a length of
`m + n`, where the first `m` elements denote the elements that should be merged,
and the last `n` elements are set to 0 and should be ignored. `nums2` has a
length of `n`.

Example 1:
    Input: nums1 = [1, 2, 3, 0, 0, 0], m = 3, nums2 = [2, 5, 6], n = 3
    Output: [1, 2, 2, 3, 5, 6]

Example 2:
    Input: nums1 = [1], m = 1, nums2 = [], n = 0
    Output: [1]

Example 3:
    Input: nums1 = [0], m = 0, nums2 = [1], n = 1
    Output: [1]
    Explanation: The arrays we are merging are [] and [1].

Constraints:
    - nums1.length == m + n
    - nums2.length == n
    - 0 <= m, n <= 200
    - 1 <= m + n <= 200
    - -10^9 <= nums1[i], nums2[j] <= 10^9

Follow up:
    - Can you come up with an algorithm that runs in O(m + n) time?
"""

from __future__ import annotations


def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    """Merge nums2 into nums1 in-place.

    Args:
        nums1: First sorted array with enough space at the end (modified in-place).
        m: Number of elements in nums1 (excluding trailing zeros).
        nums2: Second sorted array.
        n: Number of elements in nums2.
    """
    raise NotImplementedError("Implement merge")

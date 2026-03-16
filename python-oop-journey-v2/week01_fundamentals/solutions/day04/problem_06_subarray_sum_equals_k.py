"""Reference solution for Problem 06: Subarray Sum Equals K."""

from __future__ import annotations


def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    """Count subarrays with sum equal to k.

    Uses prefix sum with hash map. If prefix_sum[i] - prefix_sum[j] = k,
    then the subarray from j to i-1 sums to k.

    Time Complexity: O(n)
    Space Complexity: O(n) for the hash map

    Args:
        nums: List of integers
        k: Target sum

    Returns:
        Number of subarrays with sum equal to k
    """
    from collections import defaultdict

    # prefix_count[sum] = how many times this prefix sum has occurred
    prefix_count = defaultdict(int)
    prefix_count[0] = 1  # Empty subarray has sum 0

    current_sum = 0
    count = 0

    for num in nums:
        current_sum += num

        # If (current_sum - k) exists, those prefix sums can form valid subarrays
        count += prefix_count[current_sum - k]

        # Record current prefix sum
        prefix_count[current_sum] += 1

    return count

"""Reference solution for Problem 04: Longest Consecutive Sequence."""

from __future__ import annotations


def longest_consecutive_sequence(nums: list[int]) -> int:
    """Find length of longest consecutive elements sequence.

    Uses a hash set for O(1) lookups. For each number that could
    start a sequence (no n-1 in set), count consecutive elements.

    Time Complexity: O(n) - each number is visited at most twice
    Space Complexity: O(n) for the hash set

    Args:
        nums: List of integers (unsorted, may contain duplicates)

    Returns:
        Length of longest consecutive sequence
    """
    if not nums:
        return 0

    num_set = set(nums)
    longest = 0

    for num in num_set:
        # Only start counting if this could be the beginning of a sequence
        if num - 1 not in num_set:
            current_num = num
            current_streak = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1

            longest = max(longest, current_streak)

    return longest

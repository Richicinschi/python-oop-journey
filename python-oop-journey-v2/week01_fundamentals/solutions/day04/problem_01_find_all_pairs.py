"""Reference solution for Problem 01: Find All Pairs."""

from __future__ import annotations


def find_all_pairs(nums: list[int], target: int) -> list[tuple[int, int]]:
    """Find all unique pairs that sum to target.

    Uses a hash map to track seen numbers and their remaining count,
    ensuring each number is only used in one pair.

    Args:
        nums: List of integers to search
        target: Target sum value

    Returns:
        List of tuples, each containing a pair that sums to target.
        Each tuple has smaller number first. No duplicate pairs.
    """
    from collections import Counter

    count = Counter(nums)
    result = []
    seen_pairs = set()

    for num in list(count.keys()):
        complement = target - num

        # Skip if we've already processed this pair
        pair_key = tuple(sorted([num, complement]))
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)

        if num == complement:
            # Need at least 2 occurrences for same-number pairs
            if count[num] >= 2:
                result.append(pair_key)
        elif complement in count:
            result.append(pair_key)

    return sorted(result)

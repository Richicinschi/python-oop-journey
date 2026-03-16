"""Reference solution for Problem 03: Top K Frequent Elements."""

from __future__ import annotations


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """Return the k most frequent elements.

    Uses Counter for frequency counting, then sorts by frequency.
    Alternative approaches: heap (O(n log k)) or bucket sort (O(n)).

    Args:
        nums: List of integers
        k: Number of most frequent elements to return

    Returns:
        List of k most frequent elements
    """
    from collections import Counter

    # Count frequencies
    freq = Counter(nums)

    # Sort by frequency (descending) and take top k
    most_common = freq.most_common(k)

    # Return just the elements
    return [num for num, _ in most_common]

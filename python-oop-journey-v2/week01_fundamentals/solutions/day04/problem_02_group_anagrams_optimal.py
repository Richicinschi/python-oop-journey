"""Reference solution for Problem 02: Group Anagrams Optimal."""

from __future__ import annotations


def group_anagrams_optimal(strs: list[str]) -> list[list[str]]:
    """Group anagrams together using character counting.

    Instead of sorting each string (O(n log n)), we use character
    counting to create a signature (O(n)) for each string.

    Args:
        strs: List of strings to group

    Returns:
        List of groups where each group contains anagrams
    """
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        # Create character count signature
        char_count = [0] * 26
        for char in s:
            char_count[ord(char) - ord("a")] += 1

        # Use tuple of counts as dictionary key
        key = tuple(char_count)
        groups[key].append(s)

    return list(groups.values())

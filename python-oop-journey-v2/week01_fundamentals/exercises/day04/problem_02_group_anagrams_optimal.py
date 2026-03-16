"""Problem 02: Group Anagrams Optimal

Topic: Hash Map, String Grouping
Difficulty: Medium

Given a list of strings, group the anagrams together.

An anagram is a word formed by rearranging the letters of a different word,
using all the original letters exactly once.

This is an optimized approach using character counting, different from
sorting-based solutions.
"""

from __future__ import annotations


def group_anagrams_optimal(strs: list[str]) -> list[list[str]]:
    """Group anagrams together using character counting.

    Args:
        strs: List of strings to group

    Returns:
        List of groups where each group contains anagrams

    Example:
        >>> result = group_anagrams_optimal(["eat", "tea", "tan", "ate", "nat", "bat"])
        >>> sorted([sorted(group) for group in result])
        [['bat'], ['eat', 'tea', 'ate'], ['tan', 'nat']]
    """
    raise NotImplementedError("Implement group_anagrams_optimal")

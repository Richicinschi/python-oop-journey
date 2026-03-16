"""Reference solution for Problem 09: Group Anagrams."""

from __future__ import annotations
from collections import defaultdict


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Group strings that are anagrams of each other.
    
    Uses a hash map where the key is the sorted string (canonical form of anagrams).
    All anagrams will have the same sorted representation.
    
    Args:
        strs: A list of strings.
        
    Returns:
        A list of groups, where each group contains strings that are anagrams.
    """
    anagram_groups: dict[str, list[str]] = defaultdict(list)
    
    for word in strs:
        # Sort the string to get its canonical form
        key = "".join(sorted(word))
        anagram_groups[key].append(word)
    
    return list(anagram_groups.values())

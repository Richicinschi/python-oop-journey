"""Reference solution for Problem 04: First Unique Character in a String."""

from __future__ import annotations
from collections import Counter


def first_unique_character(s: str) -> int:
    """Find the index of the first non-repeating character.
    
    Uses Counter to build a frequency map, then scans the string to find
    the first character with count of 1.
    
    Args:
        s: The input string.
        
    Returns:
        The index of the first unique character, or -1 if no unique character exists.
    """
    # Build frequency counter
    char_count = Counter(s)
    
    # Find first character with count 1
    for i, char in enumerate(s):
        if char_count[char] == 1:
            return i
    
    return -1

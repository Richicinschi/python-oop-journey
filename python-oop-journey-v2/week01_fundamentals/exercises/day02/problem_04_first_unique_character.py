"""Problem 04: First Unique Character in a String

Topic: Strings
Difficulty: Easy

Given a string s, find the first non-repeating character in it and return its index.
If it does not exist, return -1.
"""

from __future__ import annotations


def first_unique_character(s: str) -> int:
    """Find the index of the first non-repeating character.
    
    Args:
        s: The input string.
        
    Returns:
        The index of the first unique character, or -1 if no unique character exists.
        
    Examples:
        >>> first_unique_character("leetcode")
        0
        >>> first_unique_character("loveleetcode")
        2
        >>> first_unique_character("aabb")
        -1
        >>> first_unique_character("")
        -1
    """
    raise NotImplementedError("Implement first_unique_character")

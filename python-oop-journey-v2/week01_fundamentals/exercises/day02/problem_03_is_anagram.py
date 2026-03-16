"""Problem 03: Valid Anagram

Topic: Strings
Difficulty: Easy

Given two strings s and t, return True if t is an anagram of s, and False otherwise.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase,
typically using all the original letters exactly once.
"""

from __future__ import annotations


def is_anagram(s: str, t: str) -> bool:
    """Check if two strings are anagrams of each other.
    
    Args:
        s: The first string.
        t: The second string.
        
    Returns:
        True if t is an anagram of s, False otherwise.
        
    Examples:
        >>> is_anagram("anagram", "nagaram")
        True
        >>> is_anagram("rat", "car")
        False
        >>> is_anagram("", "")
        True
        >>> is_anagram("a", "ab")
        False
    """
    raise NotImplementedError("Implement is_anagram")

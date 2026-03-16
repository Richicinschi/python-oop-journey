"""Reference solution for Problem 03: Valid Anagram."""

from __future__ import annotations
from collections import Counter


def is_anagram(s: str, t: str) -> bool:
    """Check if two strings are anagrams of each other.
    
    Uses Counter to count character frequencies. Two strings are anagrams
    if they have the same character counts.
    
    Args:
        s: The first string.
        t: The second string.
        
    Returns:
        True if t is an anagram of s, False otherwise.
    """
    # Anagrams must have the same length
    if len(s) != len(t):
        return False
    
    return Counter(s) == Counter(t)

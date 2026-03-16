"""Problem 08: Isomorphic Strings

Topic: Hash Map, Bijection
Difficulty: Easy

Given two strings s and t, determine if they are isomorphic.

Two strings are isomorphic if the characters in s can be replaced to get t.
All occurrences of a character must be replaced with another character while
preserving the order of characters. No two characters may map to the same
character, but a character may map to itself.
"""

from __future__ import annotations


def isomorphic_strings(s: str, t: str) -> bool:
    """Check if two strings are isomorphic.

    Args:
        s: First string
        t: Second string

    Returns:
        True if strings are isomorphic, False otherwise

    Example:
        >>> isomorphic_strings("egg", "add")
        True
        >>> isomorphic_strings("foo", "bar")
        False
        >>> isomorphic_strings("paper", "title")
        True
    """
    raise NotImplementedError("Implement isomorphic_strings")

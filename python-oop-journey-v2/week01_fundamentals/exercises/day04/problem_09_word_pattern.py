"""Problem 09: Word Pattern

Topic: Hash Map, Pattern Matching
Difficulty: Easy

Given a pattern and a string s, find if s follows the same pattern.

A pattern is followed if there is a bijection between a letter in pattern
and a non-empty word in s.
"""

from __future__ import annotations


def word_pattern(pattern: str, s: str) -> bool:
    """Check if string follows pattern.

    Args:
        pattern: Pattern string containing letters
        s: String containing words separated by spaces

    Returns:
        True if s follows the pattern, False otherwise

    Example:
        >>> word_pattern("abba", "dog cat cat dog")
        True
        >>> word_pattern("abba", "dog cat cat fish")
        False
        >>> word_pattern("aaaa", "dog cat cat dog")
        False
    """
    raise NotImplementedError("Implement word_pattern")

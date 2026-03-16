"""Problem 07: Longest Substring Without Repeating Characters

Topic: Strings
Difficulty: Medium

Given a string s, find the length of the longest substring without repeating characters.

A substring is a contiguous sequence of characters within a string.
"""

from __future__ import annotations


def longest_substring_without_repeating(s: str) -> int:
    """Find the length of the longest substring without repeating characters.
    
    Args:
        s: The input string.
        
    Returns:
        The length of the longest substring with all unique characters.
        
    Examples:
        >>> longest_substring_without_repeating("abcabcbb")
        3
        >>> longest_substring_without_repeating("bbbbb")
        1
        >>> longest_substring_without_repeating("pwwkew")
        3
        >>> longest_substring_without_repeating("")
        0
        >>> longest_substring_without_repeating(" ")
        1
    """
    raise NotImplementedError("Implement longest_substring_without_repeating")

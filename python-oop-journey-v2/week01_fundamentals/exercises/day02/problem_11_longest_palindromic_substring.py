"""Problem 11: Longest Palindromic Substring

Topic: Strings
Difficulty: Medium

Given a string s, return the longest palindromic substring in s.

A palindrome is a string that reads the same backward as forward.

A substring is a contiguous sequence of characters within a string.
"""

from __future__ import annotations


def longest_palindromic_substring(s: str) -> str:
    """Find the longest palindromic substring.
    
    Args:
        s: The input string.
        
    Returns:
        The longest palindromic substring. If multiple exist, return any one.
        Returns empty string if input is empty.
        
    Examples:
        >>> longest_palindromic_substring("babad")
        'bab'  # or 'aba'
        >>> longest_palindromic_substring("cbbd")
        'bb'
        >>> longest_palindromic_substring("a")
        'a'
        >>> longest_palindromic_substring("")
        ''
        >>> longest_palindromic_substring("ac")
        'a'  # or 'c'
    """
    raise NotImplementedError("Implement longest_palindromic_substring")

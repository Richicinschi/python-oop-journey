"""Problem 02: Valid Palindrome

Topic: Strings
Difficulty: Easy

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters
and removing all non-alphanumeric characters, it reads the same forward and backward.

Alphanumeric characters include letters and numbers.
"""

from __future__ import annotations


def is_valid_palindrome(s: str) -> bool:
    """Check if a string is a valid palindrome.
    
    Only alphanumeric characters are considered, and case is ignored.
    
    Args:
        s: The input string to check.
        
    Returns:
        True if the string is a palindrome, False otherwise.
        
    Examples:
        >>> is_valid_palindrome("A man, a plan, a canal: Panama")
        True
        >>> is_valid_palindrome("race a car")
        False
        >>> is_valid_palindrome(" ")
        True
        >>> is_valid_palindrome("0P")
        False
    """
    raise NotImplementedError("Implement is_valid_palindrome")

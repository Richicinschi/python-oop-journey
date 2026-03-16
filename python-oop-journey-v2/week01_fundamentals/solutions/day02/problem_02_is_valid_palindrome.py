"""Reference solution for Problem 02: Valid Palindrome."""

from __future__ import annotations


def is_valid_palindrome(s: str) -> bool:
    """Check if a string is a valid palindrome.
    
    Uses two-pointer technique to compare characters from both ends,
    skipping non-alphanumeric characters and ignoring case.
    
    Args:
        s: The input string to check.
        
    Returns:
        True if the string is a palindrome, False otherwise.
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric from left
        while left < right and not s[left].isalnum():
            left += 1
        # Skip non-alphanumeric from right
        while left < right and not s[right].isalnum():
            right -= 1
            
        # Compare characters (case-insensitive)
        if s[left].lower() != s[right].lower():
            return False
            
        left += 1
        right -= 1
    
    return True

"""Reference solution for Problem 11: Longest Palindromic Substring."""

from __future__ import annotations


def longest_palindromic_substring(s: str) -> str:
    """Find the longest palindromic substring.
    
    Uses "expand around center" technique. For each position, expand outward
    to find palindromes centered at that position (odd length) and between
    positions (even length).
    
    Args:
        s: The input string.
        
    Returns:
        The longest palindromic substring.
    """
    if not s:
        return ""
    
    start, end = 0, 0
    
    for i in range(len(s)):
        # Check odd-length palindromes (centered at i)
        len1 = _expand_around_center(s, i, i)
        # Check even-length palindromes (centered between i and i+1)
        len2 = _expand_around_center(s, i, i + 1)
        
        max_len = max(len1, len2)
        
        # Update the longest palindrome boundaries
        if max_len > end - start:
            start = i - (max_len - 1) // 2
            end = i + max_len // 2
    
    return s[start:end + 1]


def _expand_around_center(s: str, left: int, right: int) -> int:
    """Expand around the center and return the length of palindrome.
    
    Args:
        s: The input string.
        left: The left pointer (starts at or left of center).
        right: The right pointer (starts at or right of center).
        
    Returns:
        The length of the palindrome found.
    """
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    
    # Return the length (right - left - 1 because we went one step too far)
    return right - left - 1

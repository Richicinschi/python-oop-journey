"""Reference solution for Problem 07: Longest Substring Without Repeating Characters."""

from __future__ import annotations


def longest_substring_without_repeating(s: str) -> int:
    """Find the length of the longest substring without repeating characters.
    
    Uses sliding window technique with a hash map to track character indices.
    When a duplicate is found, move the left pointer to skip the previous occurrence.
    
    Args:
        s: The input string.
        
    Returns:
        The length of the longest substring with all unique characters.
    """
    # char -> last seen index
    char_index: dict[str, int] = {}
    max_length = 0
    left = 0
    
    for right, char in enumerate(s):
        # If char is seen and is within current window
        if char in char_index and char_index[char] >= left:
            # Move left pointer to skip the duplicate
            left = char_index[char] + 1
        else:
            # Update max length for current valid window
            max_length = max(max_length, right - left + 1)
        
        # Update last seen index
        char_index[char] = right
    
    return max_length

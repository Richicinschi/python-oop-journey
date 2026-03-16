"""Reference solution for Problem 01: Reverse String."""

from __future__ import annotations


def reverse_string(s: str) -> str:
    """Return the reverse of the input string.
    
    Uses Python's slice notation [::-1] which is efficient and Pythonic.
    
    Args:
        s: The input string to reverse.
        
    Returns:
        The reversed string.
    """
    return s[::-1]

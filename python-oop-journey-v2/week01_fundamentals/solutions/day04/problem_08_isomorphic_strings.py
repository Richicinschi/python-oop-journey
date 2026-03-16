"""Reference solution for Problem 08: Isomorphic Strings."""

from __future__ import annotations


def isomorphic_strings(s: str, t: str) -> bool:
    """Check if two strings are isomorphic.

    Uses two dictionaries to maintain bidirectional mapping:
    - char_map: maps characters from s to t
    - reverse_map: maps characters from t to s

    Time Complexity: O(n)
    Space Complexity: O(k) where k is the character set size

    Args:
        s: First string
        t: Second string

    Returns:
        True if strings are isomorphic, False otherwise
    """
    if len(s) != len(t):
        return False

    char_map = {}  # s -> t mapping
    reverse_map = {}  # t -> s mapping

    for char_s, char_t in zip(s, t):
        # Check if char_s already has a mapping
        if char_s in char_map:
            if char_map[char_s] != char_t:
                return False
        else:
            char_map[char_s] = char_t

        # Check if char_t already has a reverse mapping
        if char_t in reverse_map:
            if reverse_map[char_t] != char_s:
                return False
        else:
            reverse_map[char_t] = char_s

    return True

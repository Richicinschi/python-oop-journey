"""Reference solution for Problem 05: Longest Common Prefix."""

from __future__ import annotations


def longest_common_prefix(strs: list[str]) -> str:
    """Find the longest common prefix among a list of strings.
    
    Uses horizontal scanning - compares prefix with each string and
    reduces the prefix until it matches.
    
    Args:
        strs: A list of strings.
        
    Returns:
        The longest common prefix string. Returns empty string if no common prefix
        or if the list is empty.
    """
    if not strs:
        return ""
    
    if len(strs) == 1:
        return strs[0]
    
    # Start with the first string as prefix
    prefix = strs[0]
    
    # Compare with remaining strings
    for string in strs[1:]:
        # Reduce prefix until it matches the start of current string
        while not string.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    
    return prefix

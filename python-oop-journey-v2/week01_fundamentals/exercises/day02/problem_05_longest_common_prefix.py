"""Problem 05: Longest Common Prefix

Topic: Strings
Difficulty: Easy

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".
"""

from __future__ import annotations


def longest_common_prefix(strs: list[str]) -> str:
    """Find the longest common prefix among a list of strings.
    
    Args:
        strs: A list of strings.
        
    Returns:
        The longest common prefix string. Returns empty string if no common prefix.
        
    Examples:
        >>> longest_common_prefix(["flower", "flow", "flight"])
        'fl'
        >>> longest_common_prefix(["dog", "racecar", "car"])
        ''
        >>> longest_common_prefix(["interspecies", "interstellar", "interstate"])
        'inters'
        >>> longest_common_prefix(["a"])
        'a'
        >>> longest_common_prefix([])
        ''
    """
    raise NotImplementedError("Implement longest_common_prefix")

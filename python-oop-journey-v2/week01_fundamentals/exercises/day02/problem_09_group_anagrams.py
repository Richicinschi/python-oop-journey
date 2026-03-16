"""Problem 09: Group Anagrams

Topic: Strings
Difficulty: Medium

Given an array of strings strs, group the anagrams together.

You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase,
typically using all the original letters exactly once.
"""

from __future__ import annotations


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Group strings that are anagrams of each other.
    
    Args:
        strs: A list of strings.
        
    Returns:
        A list of groups, where each group contains strings that are anagrams.
        
    Examples:
        >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
        >>> group_anagrams([""])
        [['']]
        >>> group_anagrams(["a"])
        [['a']]
        
    Note:
        The order of groups and the order within each group does not matter.
    """
    raise NotImplementedError("Implement group_anagrams")

"""Problem 08: String Compression

Topic: Strings
Difficulty: Easy

Given an array of characters chars, compress it using the following algorithm:

Begin with an empty string s. For each group of consecutive repeating characters in chars:
- If the group's length is 1, append the character to s.
- Otherwise, append the character followed by the group's length.

The compressed string s should not be returned separately, but instead, be stored in the
input character array chars. Note that group lengths that are 10 or longer will be split
into multiple characters in chars.

After you are done modifying the input array, return the new length of the array.

You must write an algorithm that uses only constant extra space.

Note: For this exercise, return the compressed string directly.
"""

from __future__ import annotations


def compress_string(chars: str) -> str:
    """Compress a string using run-length encoding.
    
    Consecutive repeating characters are replaced with the character followed
    by the count. Single characters are not followed by a count.
    
    Args:
        chars: The input string to compress.
        
    Returns:
        The compressed string.
        
    Examples:
        >>> compress_string("aabccccaaa")
        'a2bc4a3'
        >>> compress_string("abcd")
        'abcd'
        >>> compress_string("a")
        'a'
        >>> compress_string("aa")
        'a2'
        >>> compress_string("aabbaa")
        'a2b2a2'
    """
    raise NotImplementedError("Implement compress_string")

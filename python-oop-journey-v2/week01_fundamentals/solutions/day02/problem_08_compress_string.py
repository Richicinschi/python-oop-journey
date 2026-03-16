"""Reference solution for Problem 08: String Compression."""

from __future__ import annotations


def compress_string(chars: str) -> str:
    """Compress a string using run-length encoding.
    
    Iterates through the string, counting consecutive characters.
    When a different character is encountered, append the count and char to result.
    
    Args:
        chars: The input string to compress.
        
    Returns:
        The compressed string.
    """
    if not chars:
        return ""
    
    result = []
    count = 1
    
    for i in range(1, len(chars)):
        if chars[i] == chars[i - 1]:
            count += 1
        else:
            result.append(chars[i - 1])
            if count > 1:
                result.append(str(count))
            count = 1
    
    # Handle the last group
    result.append(chars[-1])
    if count > 1:
        result.append(str(count))
    
    return "".join(result)

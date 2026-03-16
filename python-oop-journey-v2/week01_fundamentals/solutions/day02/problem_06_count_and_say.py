"""Reference solution for Problem 06: Count and Say."""

from __future__ import annotations


def count_and_say(n: int) -> str:
    """Return the nth term of the count-and-say sequence.
    
    Uses iterative approach where each term is built by describing the previous term.
    
    Args:
        n: The term number (1-indexed).
        
    Returns:
        The nth term as a string.
    """
    if n <= 0:
        return ""
    
    # Base case
    result = "1"
    
    # Build each subsequent term
    for _ in range(n - 1):
        result = _say(result)
    
    return result


def _say(s: str) -> str:
    """Generate the 'say' description of a digit string.
    
    For each group of consecutive identical digits, output count followed by digit.
    
    Args:
        s: The digit string to describe.
        
    Returns:
        The description string.
    """
    result = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(str(count))
            result.append(s[i - 1])
            count = 1
    
    # Don't forget the last group
    result.append(str(count))
    result.append(s[-1])
    
    return "".join(result)

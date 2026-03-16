"""Reference solution for Problem 03: Count Frequencies.

This solution uses dict.get() for concise counting:
- frequencies.get(item, 0) returns the current count, or 0 if item not seen
- Add 1 to get the new count
- Assign back to frequencies[item]

This pattern is more Pythonic than checking 'if item in frequencies'.

Alternative: collections.Counter (most efficient for production)
    from collections import Counter
    return dict(Counter(items))
"""

from __future__ import annotations


def count_frequencies(items: list[str]) -> dict[str, int]:
    """Count the frequency of each item in a list.

    Args:
        items: A list of strings.

    Returns:
        A dictionary mapping each unique item to its count.
    """
    frequencies = {}
    
    for item in items:
        # dict.get(key, default) returns the value if key exists, else default
        # This elegantly handles both first occurrence (0 + 1 = 1)
        # and subsequent occurrences (n + 1 = n+1)
        frequencies[item] = frequencies.get(item, 0) + 1
    
    return frequencies

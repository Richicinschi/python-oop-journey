"""Problem 06: Unique Pairs

Topic: Set Comprehensions, itertools
Difficulty: Medium

Generate all unique unordered pairs from a list of items.
Pairs are considered the same regardless of order (a,b) == (b,a).
"""

from __future__ import annotations


def unique_pairs(items: list[str]) -> set[tuple[str, str]]:
    """Generate all unique unordered pairs from a list.

    Args:
        items: A list of strings.

    Returns:
        A set of tuples, where each tuple contains two different items
        from the input list. Each pair appears once, with the
        lexicographically smaller item first.

    Example:
        >>> unique_pairs(["a", "b", "c"])
        {('a', 'b'), ('a', 'c'), ('b', 'c')}
        >>> unique_pairs(["x", "y"])
        {('x', 'y')}
        >>> unique_pairs(["a"])
        set()
    """
    raise NotImplementedError("Implement unique_pairs")

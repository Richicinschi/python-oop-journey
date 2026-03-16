"""Reference solution for Problem 06: Unique Pairs."""

from __future__ import annotations
import itertools


def unique_pairs(items: list[str]) -> set[tuple[str, str]]:
    """Generate all unique unordered pairs from a list.

    Uses itertools.combinations to generate all unique pairs efficiently.
    Each pair is ordered with the lexicographically smaller item first.

    Args:
        items: A list of strings.

    Returns:
        A set of tuples containing all unique unordered pairs.
    """
    return set(itertools.combinations(sorted(items), 2))

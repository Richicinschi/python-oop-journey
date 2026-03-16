"""Reference solution for Problem 05: Word Length Histogram."""

from __future__ import annotations


def word_length_histogram(words: list[str]) -> dict[int, list[str]]:
    """Create a histogram of words grouped by their length.

    Uses a dictionary comprehension to group words by length.
    First collects all unique lengths, then groups words for each length.

    Args:
        words: A list of words (strings).

    Returns:
        A dictionary where keys are word lengths and values are
        lists of words with that length.
    """
    if not words:
        return {}

    # Get unique lengths to use as keys
    lengths = {len(word) for word in words}

    # Group words by their length
    return {length: [w for w in words if len(w) == length] for length in sorted(lengths)}

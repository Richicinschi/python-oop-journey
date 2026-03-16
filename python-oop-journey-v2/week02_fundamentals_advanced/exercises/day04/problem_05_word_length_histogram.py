"""Problem 05: Word Length Histogram

Topic: Dictionary Comprehensions, Aggregation
Difficulty: Easy

Create a histogram mapping each unique word length to a list of
words having that length.
"""

from __future__ import annotations


def word_length_histogram(words: list[str]) -> dict[int, list[str]]:
    """Create a histogram of words grouped by their length.

    Args:
        words: A list of words (strings).

    Returns:
        A dictionary where keys are word lengths and values are
        lists of words with that length. Words in each list
        appear in the same order as in the input.

    Example:
        >>> word_length_histogram(["cat", "dog", "elephant", "bird"])
        {3: ['cat', 'dog'], 8: ['elephant'], 4: ['bird']}
        >>> word_length_histogram([])
        {}
    """
    raise NotImplementedError("Implement word_length_histogram")

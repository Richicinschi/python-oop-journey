"""Problem 02: Word Frequency Analyzer

Topic: Dictionaries, strings, file I/O
Difficulty: Medium

Create a word frequency analyzer that processes text and returns statistics.

Required functions:
- count_words(text): Return dict of {word: count}
- get_top_words(text, n): Return the n most common words
- word_frequency_report(text): Return comprehensive stats dict

Processing rules:
- Convert to lowercase
- Remove punctuation (keep only alphanumeric and spaces)
- Words are separated by whitespace
- Empty text returns empty/zero results

Example:
    >>> count_words("Hello world hello")
    {'hello': 2, 'world': 1}
    >>> get_top_words("hello world hello", 1)
    [('hello', 2)]
    >>> word_frequency_report("Hello world!")
    {
        'total_words': 2,
        'unique_words': 2,
        'most_common': [('hello', 1), ('world', 1)],
        'average_word_length': 5.0
    }
"""

from __future__ import annotations
import re


def count_words(text: str) -> dict[str, int]:
    """Count frequency of each word in text.

    Args:
        text: Input text to analyze

    Returns:
        Dictionary mapping words to their occurrence counts
    """
    raise NotImplementedError("Implement count_words")


def get_top_words(text: str, n: int) -> list[tuple[str, int]]:
    """Get the n most common words in text.

    Args:
        text: Input text to analyze
        n: Number of top words to return

    Returns:
        List of (word, count) tuples, sorted by count (descending)
    """
    raise NotImplementedError("Implement get_top_words")


def word_frequency_report(text: str) -> dict:
    """Generate a comprehensive word frequency report.

    Args:
        text: Input text to analyze

    Returns:
        Dictionary containing:
            - total_words: Total word count
            - unique_words: Number of unique words
            - most_common: Top 5 words as (word, count) list
            - average_word_length: Average length of words
    """
    raise NotImplementedError("Implement word_frequency_report")

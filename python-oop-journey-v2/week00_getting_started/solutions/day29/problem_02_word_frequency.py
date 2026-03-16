"""Reference solution for Problem 02: Word Frequency Analyzer."""

from __future__ import annotations
import re
from collections import Counter


def count_words(text: str) -> dict[str, int]:
    """Count frequency of each word in text.

    Args:
        text: Input text to analyze

    Returns:
        Dictionary mapping words to their occurrence counts
    """
    if not text.strip():
        return {}

    # Remove punctuation, convert to lowercase, split into words
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())
    words = cleaned.split()

    return dict(Counter(words))


def get_top_words(text: str, n: int) -> list[tuple[str, int]]:
    """Get the n most common words in text.

    Args:
        text: Input text to analyze
        n: Number of top words to return

    Returns:
        List of (word, count) tuples, sorted by count (descending)
    """
    counts = count_words(text)
    return Counter(counts).most_common(n)


def word_frequency_report(text: str) -> dict:
    """Generate a comprehensive word frequency report.

    Args:
        text: Input text to analyze

    Returns:
        Dictionary containing word frequency statistics
    """
    counts = count_words(text)
    words = list(counts.keys())

    if not words:
        return {
            "total_words": 0,
            "unique_words": 0,
            "most_common": [],
            "average_word_length": 0.0,
        }

    total_chars = sum(len(word) for word in words)
    avg_length = total_chars / len(words) if words else 0.0

    return {
        "total_words": sum(counts.values()),
        "unique_words": len(counts),
        "most_common": get_top_words(text, 5),
        "average_word_length": round(avg_length, 2),
    }

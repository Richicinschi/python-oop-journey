"""Reference solution for Problem 05: Count Word Occurrences."""

from __future__ import annotations


def count_word_occurrences(filepath: str, word: str) -> int | None:
    """Count how many times a word appears in a file (case-insensitive, whole words only).

    Args:
        filepath: Path to the file to search.
        word: The word to count.

    Returns:
        The number of occurrences, or None if file doesn't exist.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            # Normalize whitespace and convert to lowercase
            words = content.lower().split()
            # Remove punctuation from each word
            cleaned_words = [
                w.strip(".,!?;:\"'()[]{}") for w in words
            ]
            target = word.lower()
            return cleaned_words.count(target)
    except FileNotFoundError:
        return None

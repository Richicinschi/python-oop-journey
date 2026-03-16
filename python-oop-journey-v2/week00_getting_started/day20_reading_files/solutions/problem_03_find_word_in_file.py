"""Reference solution for Problem 03: Find Word in File."""

from __future__ import annotations


def find_word_in_file(filepath: str, word: str) -> bool | None:
    """Check if a word exists in a file (case-insensitive).

    Args:
        filepath: Path to the file to search.
        word: The word to search for.

    Returns:
        True if the word is found, False if not found, or None if file doesn't exist.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read().lower()
            return word.lower() in content
    except FileNotFoundError:
        return None

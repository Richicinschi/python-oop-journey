"""Problem 03: Word Frequency

Topic: File I/O - Text analysis
Difficulty: Medium

Write a function that counts word frequencies in a text file.
Words are case-insensitive and punctuation should be stripped.

Examples:
    >>> word_frequency("hello.txt")  # contains "Hello world! Hello"
    {'hello': 2, 'world': 1}
    >>> word_frequency("empty.txt")
    {}

Requirements:
    - Convert all words to lowercase
    - Strip punctuation: .,!?:;"'()[]{}
    - Words are separated by whitespace
    - Return empty dict for empty or non-existent files
    - Return words sorted alphabetically in the dictionary
"""

from __future__ import annotations

from pathlib import Path


def word_frequency(filepath: str | Path) -> dict[str, int]:
    """Count word frequencies in a text file.

    Args:
        filepath: Path to the text file.

    Returns:
        Dictionary mapping lowercase words to their frequency count.
        Returns empty dict for empty or non-existent files.
    """
    raise NotImplementedError("Implement word_frequency")

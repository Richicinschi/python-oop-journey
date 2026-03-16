"""Problem 05: Count Word Occurrences

Topic: File I/O - Text Analysis
Difficulty: Easy

Write a function that counts how many times a word appears in a file (case-insensitive).

Function Signature:
    def count_word_occurrences(filepath: str, word: str) -> int | None

Requirements:
    - Return the count of word occurrences (case-insensitive)
    - Return None if the file does not exist
    - Return 0 if the word is not found
    - Count all occurrences (not just whole words)

Behavior Notes:
    - Case-insensitive: "Python", "python", "PYTHON" all count
    - Counts substrings: "py" counts in "python" and "pyramid"
    - Return 0 for empty word string
    - Each occurrence counts separately (even in same line)

Examples:
    File contains "Python is great. Python is easy.":
    >>> count_word_occurrences("example.txt", "python")
    2
    
    >>> count_word_occurrences("example.txt", "is")
    2
    
    Word not found:
    >>> count_word_occurrences("example.txt", "java")
    0
    
    File doesn't exist:
    >>> count_word_occurrences("missing.txt", "test")
    None

Input Validation:
    - You may assume filepath and word are valid strings
    - Empty word returns 0

"""

from __future__ import annotations


def count_word_occurrences(filepath: str, word: str) -> int | None:
    """Count occurrences of a word in a file (case-insensitive).

    Args:
        filepath: Path to the file to read.
        word: The word to count.

    Returns:
        Number of occurrences, or None if file doesn't exist.
    """
    raise NotImplementedError("Implement count_word_occurrences")

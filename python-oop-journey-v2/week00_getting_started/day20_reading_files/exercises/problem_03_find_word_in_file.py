"""Problem 03: Find Word in File

Topic: File I/O - Searching File Content
Difficulty: Easy

Write a function that searches for a word in a file (case-insensitive).

Function Signature:
    def find_word_in_file(filepath: str, word: str) -> bool | None

Requirements:
    - Return True if the word is found in the file (case-insensitive)
    - Return False if the word is not found
    - Return None if the file does not exist
    - Search is case-insensitive ("Hello" matches "hello")

Behavior Notes:
    - The search should match whole words only (not substrings)
    - Split lines by whitespace to get individual words
    - Remove punctuation before comparing (optional but recommended)
    - Case-insensitive means convert both file content and search word to same case

Examples:
    File contains "Hello World":
    >>> find_word_in_file("example.txt", "hello")
    True
    
    >>> find_word_in_file("example.txt", "goodbye")
    False
    
    File doesn't exist:
    >>> find_word_in_file("missing.txt", "test")
    None

Input Validation:
    - You may assume filepath and word are valid strings
    - An empty word should return False (unless file also has empty content)

"""

from __future__ import annotations


def find_word_in_file(filepath: str, word: str) -> bool | None:
    """Search for a word in a file (case-insensitive).

    Args:
        filepath: Path to the file to search.
        word: The word to search for.

    Returns:
        True if word found, False if not found, None if file doesn't exist.
    """
    raise NotImplementedError("Implement find_word_in_file")

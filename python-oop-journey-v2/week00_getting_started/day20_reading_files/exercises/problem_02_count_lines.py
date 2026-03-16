"""Problem 02: Count Lines in File

Topic: File I/O - Reading Files
Difficulty: Easy

Write a function that counts the number of lines in a file.

Function Signature:
    def count_lines(filepath: str) -> int | None

Requirements:
    - Return the total number of lines in the file
    - Return None if the file does not exist
    - An empty file should return 0
    - Count all lines including empty ones

Behavior Notes:
    - A file with no content has 0 lines
    - A file with just a newline has 1 line
    - Handle FileNotFoundError by returning None

Examples:
    File with 3 lines of text:
    >>> count_lines("three_lines.txt")
    3
    
    Empty file:
    >>> count_lines("empty.txt")
    0
    
    Non-existent file:
    >>> count_lines("missing.txt")
    None

Input Validation:
    - You may assume filepath is a valid string
    - Return None for non-existent files without raising an exception

"""

from __future__ import annotations


def count_lines(filepath: str) -> int | None:
    """Count the number of lines in a file.

    Args:
        filepath: Path to the file to read.

    Returns:
        Number of lines as integer, or None if file doesn't exist.
    """
    raise NotImplementedError("Implement count_lines")

"""Problem 02: Find Longest Line

Topic: File I/O - Text processing
Difficulty: Easy

Write a function that finds the longest line in a text file.
Returns both the line content (without trailing newline) and its line number (1-based).

Examples:
    >>> find_longest_line("example.txt")
    ('This is the longest line in the file', 3)
    >>> find_longest_line("empty.txt")
    ('', 0)
    >>> find_longest_line("single.txt")  # file with one line
    ('Only line', 1)

Requirements:
    - Return ('', 0) for empty files or non-existent files
    - Line numbers are 1-based (first line is line 1)
    - Strip trailing newlines but preserve other whitespace
    - If multiple lines have the same max length, return the first one
"""

from __future__ import annotations

from pathlib import Path


def find_longest_line(filepath: str | Path) -> tuple[str, int]:
    """Find the longest line in a text file.

    Args:
        filepath: Path to the text file.

    Returns:
        Tuple of (longest_line_content, line_number). Returns ('', 0) for
        empty or non-existent files. Line numbers are 1-based.
    """
    raise NotImplementedError("Implement find_longest_line")

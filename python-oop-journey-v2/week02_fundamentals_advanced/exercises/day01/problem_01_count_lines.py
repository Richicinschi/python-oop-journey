"""Problem 01: Count Lines

Topic: File I/O - Reading files
Difficulty: Easy

Write a function that counts the number of lines in a text file.

Examples:
    >>> count_lines("example.txt")  # file with 3 lines
    3
    >>> count_lines("empty.txt")  # empty file
    0

Requirements:
    - Return 0 for empty files
    - Handle files that don't exist by returning -1
    - Count all lines, including empty ones
    - Use proper file handling with context managers
"""

from __future__ import annotations

from pathlib import Path


def count_lines(filepath: str | Path) -> int:
    """Count the number of lines in a text file.

    Args:
        filepath: Path to the text file.

    Returns:
        Number of lines in the file, or -1 if file doesn't exist.
    """
    raise NotImplementedError("Implement count_lines")

"""Problem 01: Read File Contents

Topic: File I/O - Reading Files
Difficulty: Easy

Write a function that reads and returns the entire contents of a file.

Function Signature:
    def read_file_contents(filepath: str) -> str | None

Requirements:
    - Open the file using UTF-8 encoding
    - Return the entire file content as a string
    - If the file does not exist, return None (handle FileNotFoundError)
    - Close the file properly (use 'with' statement)

Behavior Notes:
    - The function should handle the FileNotFoundError gracefully
    - Do not print anything to stdout
    - Preserve all whitespace and newlines from the file

Examples:
    If file contains "Hello, World!":
    >>> read_file_contents("example.txt")
    'Hello, World!'
    
    If file does not exist:
    >>> read_file_contents("nonexistent.txt")
    None

Input Validation:
    - You may assume filepath is a valid string (could be empty)
    - Return None for non-existent files without raising an exception

"""

from __future__ import annotations


def read_file_contents(filepath: str) -> str | None:
    """Read and return the entire contents of a file.

    Args:
        filepath: Path to the file to read.

    Returns:
        The file contents as a string, or None if the file doesn't exist.
    """
    raise NotImplementedError("Implement read_file_contents")

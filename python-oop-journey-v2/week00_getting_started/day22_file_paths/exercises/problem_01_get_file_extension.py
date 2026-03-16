"""Problem 01: Get File Extension

Topic: File Paths - Path Manipulation
Difficulty: Easy

Write a function that extracts the file extension from a filepath.

Function Signature:
    def get_file_extension(filepath: str) -> str

Requirements:
    - Return the file extension including the dot (e.g., ".txt")
    - Return empty string "" if no extension
    - Handle files with multiple dots (return last extension)
    - Handle hidden files starting with dot

Behavior Notes:
    - Extension is everything after the last dot
    - Hidden files (starting with ".") have no extension by convention
    - Multiple dots: "/path/to/file.tar.gz" → ".gz"
    - No dot in filename: return ""

Examples:
    >>> get_file_extension("document.txt")
    '.txt'
    
    >>> get_file_extension("/path/to/image.png")
    '.png'
    
    >>> get_file_extension("archive.tar.gz")
    '.gz'
    
    No extension:
    >>> get_file_extension("Makefile")
    ''
    
    Hidden file:
    >>> get_file_extension(".bashrc")
    ''

Input Validation:
    - You may assume filepath is a valid string (could be empty)
    - Empty string returns ""

Edge Cases:
    - Ends with dot: "file." → "."
    - Just extension: ".txt" → "" (hidden file convention)

"""

from __future__ import annotations


def get_file_extension(filepath: str) -> str:
    """Extract the file extension from a filepath.

    Args:
        filepath: Path to the file.

    Returns:
        The file extension with dot, or empty string if none.
    """
    raise NotImplementedError("Implement get_file_extension")

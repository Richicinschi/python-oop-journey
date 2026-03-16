"""Problem 03: Get Filename Without Extension

Topic: File Paths - Path Parsing
Difficulty: Easy

Write a function that extracts the filename without its extension.

Function Signature:
    def get_filename_without_ext(filepath: str) -> str

Requirements:
    - Return just the filename (no directory path)
    - Remove the file extension
    - Handle files with multiple extensions
    - Handle paths with directories

Behavior Notes:
    - First get the basename (filename only, no directories)
    - Then remove the extension
    - Hidden files (starting with ".") keep their name
    - Multiple dots: remove only the last extension

Examples:
    >>> get_filename_without_ext("/home/user/document.txt")
    'document'
    
    >>> get_filename_without_ext("image.png")
    'image'
    
    >>> get_filename_without_ext("archive.tar.gz")
    'archive.tar'
    
    Just filename with extension:
    >>> get_filename_without_ext("script.py")
    'script'
    
    Hidden file:
    >>> get_filename_without_ext("/etc/.bashrc")
    '.bashrc'
    
    No extension:
    >>> get_filename_without_ext("Makefile")
    'Makefile'

Input Validation:
    - You may assume filepath is a valid string
    - Empty string returns ""

Implementation Hint:
    - Use os.path.basename() and os.path.splitext()

"""

from __future__ import annotations

import os


def get_filename_without_ext(filepath: str) -> str:
    """Extract the filename without extension.

    Args:
        filepath: Path to the file.

    Returns:
        Filename without extension.
    """
    raise NotImplementedError("Implement get_filename_without_ext")

"""Problem 04: Check if Path Exists

Topic: File Paths - Path Validation
Difficulty: Easy

Write a function that checks if a path exists (file or directory).

Function Signature:
    def path_exists(filepath: str) -> bool

Requirements:
    - Return True if the path exists (as file OR directory)
    - Return False if the path doesn't exist
    - Don't raise exceptions for any input

Behavior Notes:
    - Works for both files and directories
    - Returns False for broken symlinks
    - Returns False for permission errors
    - Never raises an exception

Examples:
    Existing file:
    >>> path_exists("/etc/passwd")  # on Unix
    True
    
    Existing directory:
    >>> path_exists("/home")
    True
    
    Non-existent path:
    >>> path_exists("/nonexistent/path/file.txt")
    False
    
    Empty string:
    >>> path_exists("")
    False

Input Validation:
    - Handle any string input without raising
    - Empty string returns False

Implementation Hint:
    - Use os.path.exists()
    - Wrap in try/except if needed, but exists() rarely raises

"""

from __future__ import annotations

import os


def path_exists(filepath: str) -> bool:
    """Check if a path exists.

    Args:
        filepath: Path to check.

    Returns:
        True if path exists, False otherwise.
    """
    raise NotImplementedError("Implement path_exists")

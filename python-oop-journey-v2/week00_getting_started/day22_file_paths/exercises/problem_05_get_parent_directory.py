"""Problem 05: Get Parent Directory

Topic: File Paths - Path Navigation
Difficulty: Easy

Write a function that returns the parent directory of a given path.

Function Signature:
    def get_parent_directory(filepath: str) -> str

Requirements:
    - Return the parent directory path
    - Return empty string if no parent (root or just filename)
    - Handle both files and directories
    - Normalize the path (resolve .. and .)

Behavior Notes:
    - "/home/user/file.txt" → "/home/user"
    - "folder/subfolder/" → "folder"
    - "file.txt" → "" (no parent)
    - "/file.txt" → "/" (root parent is root)
    - Normalize to resolve .. and .

Examples:
    >>> get_parent_directory("/home/user/documents/file.txt")
    '/home/user/documents'
    
    >>> get_parent_directory("folder/subfolder/file.py")
    'folder/subfolder'
    
    >>> get_parent_directory("just_a_file.txt")
    ''
    
    Root file:
    >>> get_parent_directory("/root_file.txt")
    '/'
    
    With normalization:
    >>> get_parent_directory("/home/./user/../docs")
    '/home'

Input Validation:
    - You may assume filepath is a valid string
    - Empty string returns ""

Implementation Hint:
    - Use os.path.dirname() and os.path.normpath()

"""

from __future__ import annotations

import os


def get_parent_directory(filepath: str) -> str:
    """Return the parent directory of a given path.

    Args:
        filepath: Path to get parent of.

    Returns:
        Parent directory path, or empty string if no parent.
    """
    raise NotImplementedError("Implement get_parent_directory")

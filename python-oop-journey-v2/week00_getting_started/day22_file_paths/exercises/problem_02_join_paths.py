"""Problem 02: Join Paths

Topic: File Paths - Path Construction
Difficulty: Easy

Write a function that joins multiple path components correctly.

Function Signature:
    def join_paths(base: str, *parts: str) -> str

Requirements:
    - Join base path with additional parts using correct separator
    - Handle leading/trailing slashes correctly
    - Return the joined path as a string
    - Use os.path.join behavior (don't implement your own)

Behavior Notes:
    - Use os.path.join for correct cross-platform behavior
    - Multiple consecutive separators should be handled
    - Empty parts should be ignored
    - Preserve absolute paths (if a part starts with /)

Examples:
    >>> join_paths("/home", "user", "documents")
    '/home/user/documents'
    
    >>> join_paths("folder", "subfolder", "file.txt")
    'folder/subfolder/file.txt'  # or 'folder\\subfolder\\file.txt' on Windows
    
    Handle slashes:
    >>> join_paths("/home/", "/user", "docs/")
    '/user/docs'  # absolute path in parts resets
    
    Single part:
    >>> join_paths("/usr")
    '/usr'

Input Validation:
    - You may assume base is a valid string
    - parts may be empty (return base)

Implementation Hint:
    - Use os.path.join() function
    - Don't try to concatenate strings manually

"""

from __future__ import annotations

import os


def join_paths(base: str, *parts: str) -> str:
    """Join multiple path components correctly.

    Args:
        base: Base path.
        *parts: Additional path components.

    Returns:
        The joined path.
    """
    raise NotImplementedError("Implement join_paths")

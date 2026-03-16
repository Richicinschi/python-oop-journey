"""Problem 05: Overwrite File with Backup

Topic: File I/O - Safe Overwriting
Difficulty: Medium

Write a function that overwrites a file but creates a backup of the original first.

Function Signature:
    def overwrite_with_backup(filepath: str, content: str) -> bool

Requirements:
    - If file exists, rename it to "{filename}.bak" before overwriting
    - Write new content to the original filepath
    - Return True if successful
    - Return False if backup already exists (prevent backup overwrite)
    - Return False on any error

Behavior Notes:
    - Backup is named: original filepath + ".bak"
    - If "{filepath}.bak" already exists, do nothing and return False
    - If original file doesn't exist, just create new file (no backup needed)
    - This provides a one-level undo capability

Examples:
    File exists, no backup:
    >>> overwrite_with_backup("data.txt", "New data")
    True
    # Original saved as "data.txt.bak"
    # New content in "data.txt"
    
    Backup already exists:
    >>> overwrite_with_backup("data.txt", "Even newer")
    False
    # Nothing changed (protect existing backup)
    
    File doesn't exist:
    >>> overwrite_with_backup("new_file.txt", "Content")
    True
    # Just creates the file (no backup needed)

Input Validation:
    - You may assume filepath and content are valid strings
    - Handle all errors by returning False

Edge Cases:
    - Backup exists: return False
    - Original doesn't exist: create new file
    - Permission error: return False

"""

from __future__ import annotations

import os


def overwrite_with_backup(filepath: str, content: str) -> bool:
    """Overwrite a file but create a backup of the original first.

    Args:
        filepath: Path to the file.
        content: New content to write.

    Returns:
        True if successful, False if backup exists or on error.
    """
    raise NotImplementedError("Implement overwrite_with_backup")

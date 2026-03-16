"""Problem 04: Create New File

Topic: File I/O - Safe File Creation
Difficulty: Easy

Write a function that creates a new file only if it doesn't already exist.

Function Signature:
    def create_new_file(filepath: str, content: str = "") -> bool

Requirements:
    - Create a new file with the given content
    - Return True if file was created successfully
    - Return False if file already exists (don't overwrite)
    - Return False on permission errors
    - Default content is empty string

Behavior Notes:
    - Do NOT overwrite existing files
    - Check existence before writing
    - Empty content creates an empty file
    - This is a "safe" write that protects existing data

Examples:
    Create new file:
    >>> create_new_file("new.txt", "Hello")
    True
    
    File already exists:
    >>> create_new_file("existing.txt", "New content")
    False
    # Existing file is NOT modified
    
    Create empty file:
    >>> create_new_file("empty.txt")
    True
    # File created with no content

Input Validation:
    - You may assume filepath is a valid string
    - Handle permission errors by returning False

Edge Cases:
    - File exists: return False (protect existing data)
    - File doesn't exist: create it and return True

"""

from __future__ import annotations


def create_new_file(filepath: str, content: str = "") -> bool:
    """Create a new file only if it doesn't already exist.

    Args:
        filepath: Path to the file to create.
        content: Content to write (default empty).

    Returns:
        True if created successfully, False if file exists or on error.
    """
    raise NotImplementedError("Implement create_new_file")

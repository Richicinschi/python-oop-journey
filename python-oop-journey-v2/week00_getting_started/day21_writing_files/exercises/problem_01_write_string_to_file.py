"""Problem 01: Write String to File

Topic: File I/O - Writing Files
Difficulty: Easy

Write a function that writes a string to a file, overwriting any existing content.

Function Signature:
    def write_string_to_file(filepath: str, content: str) -> bool

Requirements:
    - Write the content string to the specified file
    - Overwrite any existing content in the file
    - Return True if write was successful
    - Return False if an error occurs (PermissionError, IOError)
    - Use UTF-8 encoding

Behavior Notes:
    - This function OVERWRITES existing files
    - Creates a new file if it doesn't exist
    - Handle permission errors gracefully (return False)
    - Do not raise exceptions for permission issues

Examples:
    Write "Hello" to file:
    >>> write_string_to_file("output.txt", "Hello")
    True
    
    Overwrite existing file:
    >>> write_string_to_file("existing.txt", "New content")
    True
    
    Permission error (if can't write):
    >>> write_string_to_file("/root/protected.txt", "test")
    False

Input Validation:
    - You may assume filepath and content are valid strings
    - Handle permission/IO errors by returning False

"""

from __future__ import annotations


def write_string_to_file(filepath: str, content: str) -> bool:
    """Write a string to a file, overwriting any existing content.

    Args:
        filepath: Path to the file to write.
        content: The string content to write.

    Returns:
        True if write was successful, False otherwise.
    """
    raise NotImplementedError("Implement write_string_to_file")

"""Problem 02: Append to File

Topic: File I/O - Appending to Files
Difficulty: Easy

Write a function that appends content to an existing file.

Function Signature:
    def append_to_file(filepath: str, content: str) -> bool

Requirements:
    - Append the content to the end of the file
    - Create the file if it doesn't exist
    - Return True if successful, False on error
    - Add a newline before the content if file is not empty
    - Use UTF-8 encoding

Behavior Notes:
    - Appends means adds to the end (doesn't overwrite)
    - Add newline before content ONLY if file has existing content
    - Creates new file if it doesn't exist
    - Handle permission errors gracefully

Examples:
    File exists with "Hello":
    >>> append_to_file("greeting.txt", "World")
    True
    # File now contains: "Hello\nWorld"
    
    File doesn't exist:
    >>> append_to_file("new_file.txt", "First line")
    True
    # File contains: "First line" (no leading newline)
    
    Permission error:
    >>> append_to_file("/root/protected.txt", "test")
    False

Input Validation:
    - You may assume filepath and content are valid strings
    - Empty content should still work (may just add newline)

"""

from __future__ import annotations


def append_to_file(filepath: str, content: str) -> bool:
    """Append content to an existing file.

    Args:
        filepath: Path to the file.
        content: Content to append.

    Returns:
        True if successful, False on error.
    """
    raise NotImplementedError("Implement append_to_file")

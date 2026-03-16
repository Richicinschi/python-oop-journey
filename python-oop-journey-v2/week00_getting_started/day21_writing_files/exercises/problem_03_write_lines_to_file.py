"""Problem 03: Write Lines to File

Topic: File I/O - Writing Multiple Lines
Difficulty: Easy

Write a function that writes a list of strings to a file, each on a new line.

Function Signature:
    def write_lines_to_file(filepath: str, lines: list[str]) -> bool

Requirements:
    - Write each string in the list as a separate line
    - Add newline character after each line (including last)
    - Overwrite any existing content
    - Return True if successful, False on error
    - Empty list should create/overwrite with empty file

Behavior Notes:
    - Each element becomes one line
    - Add '\n' after each line
    - Overwrites existing content completely
    - Handle empty list (creates empty file)

Examples:
    Write list of lines:
    >>> write_lines_to_file("lines.txt", ["Line 1", "Line 2", "Line 3"])
    True
    # File contains: "Line 1\nLine 2\nLine 3\n"
    
    Empty list:
    >>> write_lines_to_file("empty.txt", [])
    True
    # File is created but empty
    
    Single line:
    >>> write_lines_to_file("single.txt", ["Only line"])
    True
    # File contains: "Only line\n"

Input Validation:
    - You may assume filepath is a valid string
    - You may assume lines is a list of strings
    - Handle permission errors by returning False

"""

from __future__ import annotations


def write_lines_to_file(filepath: str, lines: list[str]) -> bool:
    """Write a list of strings to a file, each on a new line.

    Args:
        filepath: Path to the file.
        lines: List of strings to write.

    Returns:
        True if successful, False on error.
    """
    raise NotImplementedError("Implement write_lines_to_file")

"""Problem 03: Error Location

Topic: Debugging Basics
Difficulty: Medium

Write a function that analyzes a traceback string and extracts
the file name and line number where the error occurred.

Input format (simplified traceback):
    "File \"filename.py\", line X\nErrorType: message"

Return a dictionary with:
- "file": the filename
- "line": the line number as int
- "error": the error type

Examples:
    >>> locate_error('File "test.py", line 15\\nValueError: invalid input')
    {'file': 'test.py', 'line': 15, 'error': 'ValueError'}
    >>> locate_error('File "main.py", line 42\\nTypeError: unsupported type')
    {'file': 'main.py', 'line': 42, 'error': 'TypeError'}

Requirements:
    - Extract file name, line number, and error type
    - Return as a dictionary with exact keys
"""

from __future__ import annotations


def locate_error(traceback: str) -> dict:
    """Extract error location from traceback string.

    Args:
        traceback: A simplified traceback string

    Returns:
        Dictionary with file, line, and error keys
    """
    raise NotImplementedError("Implement locate_error")

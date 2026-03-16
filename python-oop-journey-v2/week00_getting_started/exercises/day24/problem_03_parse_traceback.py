"""Problem 03: Parse Traceback

Topic: Reading Tracebacks
Difficulty: Medium

Write a function that extracts information from a simplified traceback string.

Given a traceback in this format:
    "ErrorType: message at line X"

Extract and return the components as a dictionary with keys:
- "error_type": the type of error (e.g., "ZeroDivisionError")
- "message": the error message (e.g., "division by zero")
- "line": the line number as an integer

Examples:
    >>> parse_traceback("ZeroDivisionError: division by zero at line 5")
    {'error_type': 'ZeroDivisionError', 'message': 'division by zero', 'line': 5}
    >>> parse_traceback("NameError: name 'x' is not defined at line 10")
    {'error_type': 'NameError', 'message': "name 'x' is not defined", 'line': 10}

Requirements:
    - Parse the error type, message, and line number
    - Return as a dictionary with the exact keys specified
    - Line number should be an integer
"""

from __future__ import annotations


def parse_traceback(traceback: str) -> dict:
    """Parse a simplified traceback string into components.

    Args:
        traceback: A string in format "ErrorType: message at line X"

    Returns:
        A dictionary with keys: error_type, message, line
    """
    raise NotImplementedError("Implement parse_traceback")

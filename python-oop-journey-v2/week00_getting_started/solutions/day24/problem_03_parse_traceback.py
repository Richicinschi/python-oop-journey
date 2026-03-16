"""Reference solution for Problem 03: Parse Traceback."""

from __future__ import annotations


def parse_traceback(traceback: str) -> dict:
    """Parse a simplified traceback string into components.

    Args:
        traceback: A string in format "ErrorType: message at line X"

    Returns:
        A dictionary with keys: error_type, message, line
    """
    # Format: "ErrorType: message at line X"
    # Split by ": " first to get error type and rest
    parts = traceback.split(": ", 1)
    error_type = parts[0]
    
    # The rest is "message at line X"
    rest = parts[1]
    
    # Split by " at line " to separate message and line number
    message_parts = rest.rsplit(" at line ", 1)
    message = message_parts[0]
    line = int(message_parts[1])
    
    return {
        "error_type": error_type,
        "message": message,
        "line": line,
    }

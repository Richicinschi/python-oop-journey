"""Reference solution for Problem 03: Error Location."""

from __future__ import annotations


def locate_error(traceback: str) -> dict:
    """Extract error location from traceback string.

    Args:
        traceback: A simplified traceback string

    Returns:
        Dictionary with file, line, and error keys
    """
    lines = traceback.strip().split("\n")
    
    # First line: File "filename.py", line X
    file_line = lines[0]
    
    # Extract filename between quotes
    start = file_line.find('"') + 1
    end = file_line.find('"', start)
    filename = file_line[start:end]
    
    # Extract line number after "line "
    line_start = file_line.find("line ") + 5
    line_num = int(file_line[line_start:].rstrip())
    
    # Second line: ErrorType: message
    error_line = lines[1]
    error_type = error_line.split(":")[0]
    
    return {
        "file": filename,
        "line": line_num,
        "error": error_type,
    }

"""Reference solution for Problem 01: Write String to File."""

from __future__ import annotations


def write_string_to_file(filepath: str, content: str) -> bool:
    """Write a string to a file, overwriting any existing content.

    Args:
        filepath: Path to the file to write.
        content: The string content to write.

    Returns:
        True if write was successful, False otherwise.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        return True
    except (PermissionError, IOError):
        return False

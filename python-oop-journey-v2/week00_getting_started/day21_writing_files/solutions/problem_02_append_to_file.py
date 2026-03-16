"""Reference solution for Problem 02: Append to File."""

from __future__ import annotations


def append_to_file(filepath: str, content: str) -> bool:
    """Append content to the end of a file.

    Args:
        filepath: Path to the file to append to.
        content: The string content to append.

    Returns:
        True if append was successful, False otherwise.
    """
    try:
        with open(filepath, "a", encoding="utf-8") as file:
            file.write(content)
        return True
    except (PermissionError, IOError):
        return False

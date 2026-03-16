"""Reference solution for Problem 01: Read File Contents."""

from __future__ import annotations


def read_file_contents(filepath: str) -> str | None:
    """Read and return the entire contents of a file.

    Args:
        filepath: Path to the file to read.

    Returns:
        The file contents as a string, or None if the file doesn't exist.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None

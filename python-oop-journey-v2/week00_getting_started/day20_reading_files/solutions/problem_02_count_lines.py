"""Reference solution for Problem 02: Count Lines."""

from __future__ import annotations


def count_lines(filepath: str) -> int | None:
    """Count the number of lines in a file.

    Args:
        filepath: Path to the file to read.

    Returns:
        The number of lines in the file, or None if the file doesn't exist.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return len(file.readlines())
    except FileNotFoundError:
        return None

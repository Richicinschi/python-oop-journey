"""Reference solution for Problem 03: Write Lines to File."""

from __future__ import annotations


def write_lines_to_file(filepath: str, lines: list[str]) -> bool:
    """Write a list of strings to a file, one per line.

    Args:
        filepath: Path to the file to write.
        lines: List of strings to write as lines.

    Returns:
        True if write was successful, False otherwise.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            for line in lines:
                file.write(line + "\n")
        return True
    except (PermissionError, IOError):
        return False

"""Reference solution for Problem 04: Read First N Lines."""

from __future__ import annotations


def read_first_n_lines(filepath: str, n: int) -> list[str] | None:
    """Read the first n lines from a file.

    Args:
        filepath: Path to the file to read.
        n: Number of lines to read.

    Returns:
        A list of the first n lines (with newlines stripped), or None if file doesn't exist.
        If the file has fewer than n lines, returns all lines.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            lines = []
            for i, line in enumerate(file):
                if i >= n:
                    break
                lines.append(line.rstrip("\n\r"))
            return lines
    except FileNotFoundError:
        return None

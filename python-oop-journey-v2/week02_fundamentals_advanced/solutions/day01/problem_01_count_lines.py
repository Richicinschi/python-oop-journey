"""Reference solution for Problem 01: Count Lines."""

from __future__ import annotations

from pathlib import Path


def count_lines(filepath: str | Path) -> int:
    """Count the number of lines in a text file.

    Args:
        filepath: Path to the text file.

    Returns:
        Number of lines in the file, or -1 if file doesn't exist.
    """
    path = Path(filepath)
    
    if not path.exists():
        return -1
    
    with open(path, 'r') as f:
        return sum(1 for _ in f)

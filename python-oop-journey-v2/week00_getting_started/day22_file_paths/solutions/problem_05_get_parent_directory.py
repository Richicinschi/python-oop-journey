"""Reference solution for Problem 05: Get Parent Directory."""

from __future__ import annotations

from pathlib import Path


def get_parent_directory(filepath: str, levels: int = 1) -> str:
    """Get the parent directory of a path.

    Args:
        filepath: The path to get parent from.
        levels: Number of levels to go up (default 1).

    Returns:
        The parent directory path as a string.
    """
    path = Path(filepath)
    for _ in range(levels):
        path = path.parent
    return str(path)

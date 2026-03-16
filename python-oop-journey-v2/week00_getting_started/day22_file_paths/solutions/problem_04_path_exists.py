"""Reference solution for Problem 04: Path Exists."""

from __future__ import annotations

from pathlib import Path


def path_exists(filepath: str) -> bool:
    """Check if a path exists (file or directory).

    Args:
        filepath: The path to check.

    Returns:
        True if the path exists, False otherwise.
    """
    return Path(filepath).exists()

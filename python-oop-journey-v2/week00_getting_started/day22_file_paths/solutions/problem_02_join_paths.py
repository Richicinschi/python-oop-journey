"""Reference solution for Problem 02: Join Paths."""

from __future__ import annotations

from pathlib import Path


def join_paths(base: str, *parts: str) -> str:
    """Join multiple path components together.

    Args:
        base: The base path.
        *parts: Additional path components to join.

    Returns:
        The joined path as a string.
    """
    path = Path(base)
    for part in parts:
        path = path / part
    return str(path)

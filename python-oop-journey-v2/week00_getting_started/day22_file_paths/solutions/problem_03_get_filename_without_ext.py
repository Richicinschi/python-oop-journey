"""Reference solution for Problem 03: Get Filename Without Extension."""

from __future__ import annotations

from pathlib import Path


def get_filename_without_ext(filepath: str) -> str:
    """Get the filename without its extension.

    Args:
        filepath: The path to the file.

    Returns:
        The filename without extension (e.g., 'document' from 'document.txt').
    """
    return Path(filepath).stem

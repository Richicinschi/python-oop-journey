"""Reference solution for Problem 01: Get File Extension."""

from __future__ import annotations

from pathlib import Path


def get_file_extension(filepath: str) -> str:
    """Extract the file extension from a filepath.

    Args:
        filepath: The path to the file.

    Returns:
        The file extension including the dot (e.g., '.txt'), or empty string if no extension.
    """
    return Path(filepath).suffix

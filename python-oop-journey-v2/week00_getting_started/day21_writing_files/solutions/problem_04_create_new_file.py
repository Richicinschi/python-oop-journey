"""Reference solution for Problem 04: Create New File."""

from __future__ import annotations

from pathlib import Path


def create_new_file(filepath: str, content: str = "") -> bool:
    """Create a new file only if it doesn't already exist.

    Args:
        filepath: Path to the file to create.
        content: Optional content to write to the new file.

    Returns:
        True if file was created, False if file already exists or on error.
    """
    path = Path(filepath)
    if path.exists():
        return False

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        return True
    except (PermissionError, IOError):
        return False

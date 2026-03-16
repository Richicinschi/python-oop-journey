"""Reference solution for Problem 05: Overwrite File."""

from __future__ import annotations

from pathlib import Path


def overwrite_file(filepath: str, content: str) -> bool:
    """Overwrite an existing file with new content.

    Args:
        filepath: Path to the file to overwrite.
        content: The new content to write.

    Returns:
        True if file was overwritten, False if file doesn't exist or on error.
    """
    path = Path(filepath)
    if not path.exists():
        return False

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        return True
    except (PermissionError, IOError):
        return False

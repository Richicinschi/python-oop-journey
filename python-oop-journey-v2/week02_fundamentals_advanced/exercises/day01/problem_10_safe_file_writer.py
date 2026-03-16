"""Problem 10: Safe File Writer

Topic: Context managers, atomic operations
Difficulty: Hard

Create a context manager that writes to a file safely using a temporary
file and atomic rename. If an exception occurs, the original file is preserved.

Examples:
    >>> with SafeFileWriter("config.json") as f:
    ...     json.dump({'key': 'value'}, f)
    >>> # config.json now contains the new data
    
    >>> with SafeFileWriter("config.json") as f:
    ...     json.dump({'key': 'value'}, f)
    ...     raise ValueError("Error!")
    >>> # config.json unchanged due to exception

Requirements:
    - Write to a temporary file first (use .tmp suffix)
    - On successful exit (no exception), rename temp file to target
    - On exception, leave original file unchanged (delete temp file)
    - Create new file if target doesn't exist
    - The file object should be returned by __enter__ for writing
"""

from __future__ import annotations

import os
from pathlib import Path
from types import TracebackType
from typing import Any


class SafeFileWriter:
    """Context manager for atomic file writes with rollback support.
    
    Usage:
        with SafeFileWriter("file.txt") as f:
            f.write("content")  # Writes to temp file
        # On success, temp file is renamed to "file.txt"
        # On exception, original "file.txt" is unchanged
    """

    def __init__(self, filepath: str | Path) -> None:
        """Initialize with target file path.
        
        Args:
            filepath: Path to the target file.
        """
        raise NotImplementedError("Implement __init__")

    def __enter__(self) -> Any:
        """Enter context and return file object for writing."""
        raise NotImplementedError("Implement __enter__")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context and handle atomic rename or cleanup."""
        raise NotImplementedError("Implement __exit__")

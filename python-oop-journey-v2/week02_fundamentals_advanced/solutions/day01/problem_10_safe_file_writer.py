"""Reference solution for Problem 10: Safe File Writer."""

from __future__ import annotations

import os
from pathlib import Path
from types import TracebackType
from typing import Any, IO


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
        self.filepath = Path(filepath)
        self.temp_path = self.filepath.with_suffix(self.filepath.suffix + '.tmp')
        self._file: IO[Any] | None = None

    def __enter__(self) -> IO[Any]:
        """Enter context and return file object for writing."""
        self._file = open(self.temp_path, 'w')
        return self._file

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context and handle atomic rename or cleanup."""
        if self._file is not None:
            self._file.close()
        
        if exc_type is None:
            # Success - rename temp file to target
            # On Windows, need to remove target first if it exists
            if self.filepath.exists():
                os.remove(self.filepath)
            os.rename(self.temp_path, self.filepath)
        else:
            # Exception occurred - clean up temp file
            if self.temp_path.exists():
                os.remove(self.temp_path)

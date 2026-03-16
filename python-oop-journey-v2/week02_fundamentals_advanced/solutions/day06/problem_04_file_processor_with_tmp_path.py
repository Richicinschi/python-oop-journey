"""Reference solution for Problem 04: File Processor with tmp_path."""

from __future__ import annotations

from pathlib import Path
from typing import List


class FileProcessor:
    """Process text files with various operations."""

    def read_lines(self, filepath: str | Path) -> List[str]:
        """Read all lines from a file.

        Args:
            filepath: Path to the file to read.

        Returns:
            List of lines (without trailing newlines).

        Raises:
            FileNotFoundError: If file does not exist.
        """
        path = Path(filepath)
        with path.open("r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f]

    def write_lines(self, filepath: str | Path, lines: List[str]) -> None:
        """Write lines to a file.

        Args:
            filepath: Path to the file to write.
            lines: List of lines to write.
        """
        path = Path(filepath)
        with path.open("w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")

    def count_lines(self, filepath: str | Path) -> int:
        """Count the number of lines in a file.

        Args:
            filepath: Path to the file.

        Returns:
            Number of lines in the file.
        """
        return len(self.read_lines(filepath))

    def append_line(self, filepath: str | Path, line: str) -> None:
        """Append a single line to a file.

        Args:
            filepath: Path to the file.
            line: Line to append.
        """
        path = Path(filepath)
        with path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def find_line(self, filepath: str | Path, pattern: str) -> int:
        """Find the first line containing the pattern.

        Args:
            filepath: Path to the file.
            pattern: Substring to search for.

        Returns:
            Line number (1-indexed) of first match, or -1 if not found.
        """
        lines = self.read_lines(filepath)
        for index, line in enumerate(lines, start=1):
            if pattern in line:
                return index
        return -1

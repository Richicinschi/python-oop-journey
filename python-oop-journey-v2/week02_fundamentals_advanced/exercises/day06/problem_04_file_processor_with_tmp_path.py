"""Problem 04: File Processor with tmp_path

Topic: Testing file operations with pytest's tmp_path fixture
Difficulty: Medium

Create a file processor class and test it using pytest's tmp_path fixture.

Your task:
    1. Implement the FileProcessor class
    2. Write tests using the tmp_path fixture for file operations
    3. Ensure all file operations are properly tested

Example:
    >>> processor = FileProcessor()
    >>> processor.write_lines("test.txt", ["line1", "line2"])
    >>> processor.read_lines("test.txt")
    ['line1', 'line2']
    >>> processor.count_lines("test.txt")
    2
"""

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
        # TODO: Implement file reading
        raise NotImplementedError("Implement read_lines")

    def write_lines(self, filepath: str | Path, lines: List[str]) -> None:
        """Write lines to a file.

        Args:
            filepath: Path to the file to write.
            lines: List of lines to write.
        """
        # TODO: Implement file writing
        raise NotImplementedError("Implement write_lines")

    def count_lines(self, filepath: str | Path) -> int:
        """Count the number of lines in a file.

        Args:
            filepath: Path to the file.

        Returns:
            Number of lines in the file.
        """
        # TODO: Implement line counting
        raise NotImplementedError("Implement count_lines")

    def append_line(self, filepath: str | Path, line: str) -> None:
        """Append a single line to a file.

        Args:
            filepath: Path to the file.
            line: Line to append.
        """
        # TODO: Implement line appending
        raise NotImplementedError("Implement append_line")

    def find_line(self, filepath: str | Path, pattern: str) -> int:
        """Find the first line containing the pattern.

        Args:
            filepath: Path to the file.
            pattern: Substring to search for.

        Returns:
            Line number (1-indexed) of first match, or -1 if not found.
        """
        # TODO: Implement pattern searching
        raise NotImplementedError("Implement find_line")


# TODO: Write tests using pytest's tmp_path fixture
# Example:
# def test_write_and_read_lines(tmp_path):
#     processor = FileProcessor()
#     file_path = tmp_path / "test.txt"
#     processor.write_lines(file_path, ["a", "b", "c"])
#     assert processor.read_lines(file_path) == ["a", "b", "c"]

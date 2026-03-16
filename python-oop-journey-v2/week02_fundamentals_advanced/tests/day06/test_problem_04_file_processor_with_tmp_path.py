"""Tests for Problem 04: File Processor with tmp_path.

Note: These tests use pytest's tmp_path fixture. If you encounter
PermissionError on Windows, ensure your temp directory is writable
or run with appropriate permissions.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import pytest

from week02_fundamentals_advanced.solutions.day06.problem_04_file_processor_with_tmp_path import (
    FileProcessor,
)


# Environment workaround for tmp_path permission issues
@pytest.fixture
def safe_tmp_path(monkeypatch):
    """Provide a temporary path that works in restricted environments."""
    test_dir = Path(os.getcwd()) / ".test_tmp"
    test_dir.mkdir(exist_ok=True)
    try:
        yield test_dir
    finally:
        # Cleanup
        import shutil
        if test_dir.exists():
            shutil.rmtree(test_dir, ignore_errors=True)


class TestReadLines:
    """Tests for read_lines method."""

    def test_read_existing_file(self, safe_tmp_path) -> None:
        """Test reading lines from an existing file."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "test.txt"
        file_path.write_text("line1\nline2\nline3\n")

        lines = processor.read_lines(file_path)
        assert lines == ["line1", "line2", "line3"]

    def test_read_empty_file(self, safe_tmp_path) -> None:
        """Test reading an empty file."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "empty.txt"
        file_path.write_text("")

        lines = processor.read_lines(file_path)
        assert lines == []

    def test_read_single_line(self, safe_tmp_path) -> None:
        """Test reading a file with single line."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "single.txt"
        file_path.write_text("only line\n")

        lines = processor.read_lines(file_path)
        assert lines == ["only line"]

    def test_read_file_without_trailing_newline(self, safe_tmp_path) -> None:
        """Test reading file without trailing newline."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "no_newline.txt"
        file_path.write_text("line1\nline2")  # No trailing newline

        lines = processor.read_lines(file_path)
        assert lines == ["line1", "line2"]

    def test_read_nonexistent_file_raises(self, safe_tmp_path) -> None:
        """Test that reading nonexistent file raises FileNotFoundError."""
        processor = FileProcessor()
        with pytest.raises(FileNotFoundError):
            processor.read_lines(safe_tmp_path / "does_not_exist.txt")


class TestWriteLines:
    """Tests for write_lines method."""

    def test_write_lines_creates_file(self, safe_tmp_path) -> None:
        """Test that write_lines creates a new file."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "new_file.txt"

        processor.write_lines(file_path, ["a", "b", "c"])
        assert file_path.exists()

    def test_write_lines_content(self, safe_tmp_path) -> None:
        """Test that written content is correct."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "content.txt"

        processor.write_lines(file_path, ["hello", "world"])
        content = file_path.read_text()
        assert content == "hello\nworld\n"

    def test_write_empty_list(self, safe_tmp_path) -> None:
        """Test writing empty list creates empty file."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "empty.txt"

        processor.write_lines(file_path, [])
        content = file_path.read_text()
        assert content == ""

    def test_write_overwrites_existing(self, safe_tmp_path) -> None:
        """Test that write_lines overwrites existing file."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "overwrite.txt"
        file_path.write_text("old content\n")

        processor.write_lines(file_path, ["new"])
        content = file_path.read_text()
        assert content == "new\n"


class TestCountLines:
    """Tests for count_lines method."""

    def test_count_multiple_lines(self, safe_tmp_path) -> None:
        """Test counting multiple lines."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "multi.txt"
        processor.write_lines(file_path, ["a", "b", "c", "d"])

        assert processor.count_lines(file_path) == 4

    def test_count_empty_file(self, safe_tmp_path) -> None:
        """Test counting lines in empty file."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "empty.txt"
        processor.write_lines(file_path, [])

        assert processor.count_lines(file_path) == 0

    def test_count_single_line(self, safe_tmp_path) -> None:
        """Test counting single line."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "single.txt"
        processor.write_lines(file_path, ["only"])

        assert processor.count_lines(file_path) == 1


class TestAppendLine:
    """Tests for append_line method."""

    def test_append_to_existing_file(self, safe_tmp_path) -> None:
        """Test appending to an existing file."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "append.txt"
        processor.write_lines(file_path, ["first", "second"])

        processor.append_line(file_path, "third")
        lines = processor.read_lines(file_path)
        assert lines == ["first", "second", "third"]

    def test_append_to_new_file(self, safe_tmp_path) -> None:
        """Test appending to a new file creates it."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "new_append.txt"

        processor.append_line(file_path, "first line")
        lines = processor.read_lines(file_path)
        assert lines == ["first line"]

    def test_multiple_appends(self, safe_tmp_path) -> None:
        """Test multiple consecutive appends."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "multi_append.txt"

        processor.append_line(file_path, "a")
        processor.append_line(file_path, "b")
        processor.append_line(file_path, "c")

        lines = processor.read_lines(file_path)
        assert lines == ["a", "b", "c"]


class TestFindLine:
    """Tests for find_line method."""

    def test_find_existing_pattern(self, safe_tmp_path) -> None:
        """Test finding a pattern that exists."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "search.txt"
        processor.write_lines(file_path, [
            "first line",
            "second line",
            "third line with target",
            "fourth line",
        ])

        result = processor.find_line(file_path, "target")
        assert result == 3  # 1-indexed

    def test_find_at_beginning(self, safe_tmp_path) -> None:
        """Test finding pattern at first line."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "begin.txt"
        processor.write_lines(file_path, ["target here", "other"])

        result = processor.find_line(file_path, "target")
        assert result == 1

    def test_find_not_found(self, safe_tmp_path) -> None:
        """Test finding pattern that doesn't exist."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "notfound.txt"
        processor.write_lines(file_path, ["line1", "line2"])

        result = processor.find_line(file_path, "missing")
        assert result == -1

    def test_find_partial_match(self, safe_tmp_path) -> None:
        """Test finding partial string match."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "partial.txt"
        processor.write_lines(file_path, ["hello world", "goodbye"])

        result = processor.find_line(file_path, "world")
        assert result == 1

    def test_find_in_empty_file(self, safe_tmp_path) -> None:
        """Test finding in empty file."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "empty_search.txt"
        processor.write_lines(file_path, [])

        result = processor.find_line(file_path, "anything")
        assert result == -1


class TestIntegration:
    """Integration tests combining multiple operations."""

    def test_full_workflow(self, safe_tmp_path) -> None:
        """Test a complete workflow of operations."""
        processor = FileProcessor()
        file_path = safe_tmp_path / "workflow.txt"

        # Write initial content
        processor.write_lines(file_path, ["apple", "banana", "cherry"])
        assert processor.count_lines(file_path) == 3

        # Append more
        processor.append_line(file_path, "date")
        assert processor.count_lines(file_path) == 4

        # Find something
        assert processor.find_line(file_path, "banana") == 2

        # Read and verify
        lines = processor.read_lines(file_path)
        assert lines == ["apple", "banana", "cherry", "date"]

    def test_string_and_path_objects(self, safe_tmp_path) -> None:
        """Test that both string paths and Path objects work."""
        processor = FileProcessor()

        # Using string path
        str_path = str(safe_tmp_path / "str_path.txt")
        processor.write_lines(str_path, ["test"])
        assert processor.read_lines(str_path) == ["test"]

        # Using Path object
        path_obj = safe_tmp_path / "path_obj.txt"
        processor.write_lines(path_obj, ["test"])
        assert processor.read_lines(path_obj) == ["test"]

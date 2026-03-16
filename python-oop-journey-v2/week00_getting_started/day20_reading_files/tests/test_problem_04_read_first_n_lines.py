"""Tests for Problem 04: Read First N Lines."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day20_reading_files.solutions.problem_04_read_first_n_lines import (
    read_first_n_lines,
)


import os
import shutil

@pytest.fixture
def safe_tmp_path():
    """Provide a temporary path that works in restricted environments."""
    test_dir = Path(os.getcwd()) / '.test_tmp'
    test_dir.mkdir(exist_ok=True)
    try:
        yield test_dir
    finally:
        if test_dir.exists():
            shutil.rmtree(test_dir, ignore_errors=True)


def test_read_first_n_lines_basic(safe_tmp_path) -> None:
    """Test reading first n lines from a file."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("Line 1\nLine 2\nLine 3\nLine 4\nLine 5", encoding="utf-8")

    result = read_first_n_lines(str(test_file), 3)
    assert result == ["Line 1", "Line 2", "Line 3"]


def test_read_first_n_lines_more_than_available(safe_tmp_path) -> None:
    """Test when n is greater than available lines."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("Line 1\nLine 2", encoding="utf-8")

    result = read_first_n_lines(str(test_file), 5)
    assert result == ["Line 1", "Line 2"]


def test_read_first_n_lines_zero(safe_tmp_path) -> None:
    """Test reading zero lines."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("Line 1\nLine 2\nLine 3", encoding="utf-8")

    result = read_first_n_lines(str(test_file), 0)
    assert result == []


def test_read_first_n_lines_empty_file(safe_tmp_path) -> None:
    """Test reading from an empty file."""
    test_file = safe_tmp_path / "empty.txt"
    test_file.write_text("", encoding="utf-8")

    result = read_first_n_lines(str(test_file), 3)
    assert result == []


def test_read_first_n_lines_nonexistent_file() -> None:
    """Test reading from a non-existent file returns None."""
    result = read_first_n_lines("/nonexistent/path/file.txt", 3)
    assert result is None


def test_read_first_n_lines_strips_newlines(safe_tmp_path) -> None:
    """Test that newlines are stripped from lines."""
    test_file = safe_tmp_path / "test.txt"
    # Use binary mode to avoid Windows text mode newline translation
    test_file.write_bytes(b"Line 1\r\nLine 2\nLine 3")

    result = read_first_n_lines(str(test_file), 2)
    assert result == ["Line 1", "Line 2"]

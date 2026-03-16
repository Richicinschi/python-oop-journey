"""Tests for Problem 01: Read File Contents."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day20_reading_files.solutions.problem_01_read_file_contents import (
    read_file_contents,
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


def test_read_file_contents_success(safe_tmp_path) -> None:
    """Test reading content from an existing file."""
    test_file = safe_tmp_path / "test.txt"
    test_content = "Hello, World!\nThis is a test file."
    test_file.write_text(test_content, encoding="utf-8")

    result = read_file_contents(str(test_file))
    assert result == test_content


def test_read_file_contents_empty_file(safe_tmp_path) -> None:
    """Test reading from an empty file."""
    test_file = safe_tmp_path / "empty.txt"
    test_file.write_text("", encoding="utf-8")

    result = read_file_contents(str(test_file))
    assert result == ""


def test_read_file_contents_nonexistent_file() -> None:
    """Test reading from a non-existent file returns None."""
    result = read_file_contents("/nonexistent/path/file.txt")
    assert result is None


def test_read_file_contents_unicode(safe_tmp_path) -> None:
    """Test reading unicode content."""
    test_file = safe_tmp_path / "unicode.txt"
    test_content = "Hello 世界 🌍 ñoño"
    test_file.write_text(test_content, encoding="utf-8")

    result = read_file_contents(str(test_file))
    assert result == test_content


def test_read_file_contents_single_line(safe_tmp_path) -> None:
    """Test reading a single line file."""
    test_file = safe_tmp_path / "single.txt"
    test_content = "Only one line"
    test_file.write_text(test_content, encoding="utf-8")

    result = read_file_contents(str(test_file))
    assert result == test_content

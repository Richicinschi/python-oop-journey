"""Tests for Problem 02: Count Lines."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day20_reading_files.solutions.problem_02_count_lines import (
    count_lines,
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


def test_count_lines_multiple_lines(safe_tmp_path) -> None:
    """Test counting lines in a multi-line file."""
    test_file = safe_tmp_path / "multiline.txt"
    test_file.write_text("Line 1\nLine 2\nLine 3\n", encoding="utf-8")

    result = count_lines(str(test_file))
    assert result == 3


def test_count_lines_empty_file(safe_tmp_path) -> None:
    """Test counting lines in an empty file."""
    test_file = safe_tmp_path / "empty.txt"
    test_file.write_text("", encoding="utf-8")

    result = count_lines(str(test_file))
    assert result == 0


def test_count_lines_single_line(safe_tmp_path) -> None:
    """Test counting lines in a single-line file."""
    test_file = safe_tmp_path / "single.txt"
    test_file.write_text("Only one line", encoding="utf-8")

    result = count_lines(str(test_file))
    assert result == 1


def test_count_lines_no_trailing_newline(safe_tmp_path) -> None:
    """Test file without trailing newline."""
    test_file = safe_tmp_path / "no_newline.txt"
    test_file.write_text("Line 1\nLine 2\nLine 3", encoding="utf-8")

    result = count_lines(str(test_file))
    assert result == 3


def test_count_lines_nonexistent_file() -> None:
    """Test counting lines in a non-existent file returns None."""
    result = count_lines("/nonexistent/path/file.txt")
    assert result is None

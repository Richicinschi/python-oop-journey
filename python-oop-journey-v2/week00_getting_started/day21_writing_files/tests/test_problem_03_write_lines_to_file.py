"""Tests for Problem 03: Write Lines to File."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day21_writing_files.solutions.problem_03_write_lines_to_file import (
    write_lines_to_file,
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


def test_write_lines_to_file_basic(safe_tmp_path) -> None:
    """Test writing multiple lines to a file."""
    test_file = safe_tmp_path / "lines.txt"
    lines = ["First line", "Second line", "Third line"]

    result = write_lines_to_file(str(test_file), lines)
    assert result is True
    expected = "First line\nSecond line\nThird line\n"
    assert test_file.read_text(encoding="utf-8") == expected


def test_write_lines_to_file_empty_list(safe_tmp_path) -> None:
    """Test writing empty list creates empty file."""
    test_file = safe_tmp_path / "empty.txt"
    lines: list[str] = []

    result = write_lines_to_file(str(test_file), lines)
    assert result is True
    assert test_file.read_text(encoding="utf-8") == ""


def test_write_lines_to_file_single_line(safe_tmp_path) -> None:
    """Test writing a single line."""
    test_file = safe_tmp_path / "single.txt"
    lines = ["Only one line"]

    result = write_lines_to_file(str(test_file), lines)
    assert result is True
    assert test_file.read_text(encoding="utf-8") == "Only one line\n"


def test_write_lines_to_file_overwrite(safe_tmp_path) -> None:
    """Test that writing lines overwrites existing content."""
    test_file = safe_tmp_path / "existing.txt"
    test_file.write_text("old content\n", encoding="utf-8")

    lines = ["New line 1", "New line 2"]
    result = write_lines_to_file(str(test_file), lines)
    assert result is True
    assert test_file.read_text(encoding="utf-8") == "New line 1\nNew line 2\n"


def test_write_lines_to_file_with_empty_strings(safe_tmp_path) -> None:
    """Test writing lines that include empty strings."""
    test_file = safe_tmp_path / "with_empty.txt"
    lines = ["Line 1", "", "Line 3"]

    result = write_lines_to_file(str(test_file), lines)
    assert result is True
    assert test_file.read_text(encoding="utf-8") == "Line 1\n\nLine 3\n"

"""Tests for Problem 02: Append to File."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day21_writing_files.solutions.problem_02_append_to_file import (
    append_to_file,
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


def test_append_to_file_new_file(safe_tmp_path) -> None:
    """Test appending to a new file (creates file)."""
    test_file = safe_tmp_path / "new_file.txt"
    content = "First line"

    result = append_to_file(str(test_file), content)
    assert result is True
    assert test_file.read_text(encoding="utf-8") == content


def test_append_to_file_existing(safe_tmp_path) -> None:
    """Test appending to an existing file."""
    test_file = safe_tmp_path / "existing.txt"
    test_file.write_text("Original content\n", encoding="utf-8")

    result = append_to_file(str(test_file), "Appended content")
    assert result is True
    assert test_file.read_text(encoding="utf-8") == "Original content\nAppended content"


def test_append_multiple_times(safe_tmp_path) -> None:
    """Test multiple appends to the same file."""
    test_file = safe_tmp_path / "multi_append.txt"

    append_to_file(str(test_file), "Line 1")
    append_to_file(str(test_file), "Line 2")
    append_to_file(str(test_file), "Line 3")

    assert test_file.read_text(encoding="utf-8") == "Line 1Line 2Line 3"


def test_append_with_newlines(safe_tmp_path) -> None:
    """Test appending content with newlines."""
    test_file = safe_tmp_path / "with_newlines.txt"

    append_to_file(str(test_file), "Line 1\n")
    append_to_file(str(test_file), "Line 2\n")

    assert test_file.read_text(encoding="utf-8") == "Line 1\nLine 2\n"


def test_append_empty_string(safe_tmp_path) -> None:
    """Test appending empty string."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("content", encoding="utf-8")

    result = append_to_file(str(test_file), "")
    assert result is True
    assert test_file.read_text(encoding="utf-8") == "content"

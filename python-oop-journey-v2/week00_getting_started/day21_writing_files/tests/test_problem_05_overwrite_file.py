"""Tests for Problem 05: Overwrite File."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day21_writing_files.solutions.problem_05_overwrite_file import (
    overwrite_file,
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


def test_overwrite_file_success(safe_tmp_path) -> None:
    """Test overwriting an existing file."""
    test_file = safe_tmp_path / "existing.txt"
    test_file.write_text("old content", encoding="utf-8")

    new_content = "brand new content"
    result = overwrite_file(str(test_file), new_content)
    assert result is True
    assert test_file.read_text(encoding="utf-8") == new_content


def test_overwrite_file_nonexistent(safe_tmp_path) -> None:
    """Test overwriting a file that doesn't exist."""
    test_file = safe_tmp_path / "nonexistent.txt"

    result = overwrite_file(str(test_file), "content")
    assert result is False
    assert not test_file.exists()


def test_overwrite_file_empty_content(safe_tmp_path) -> None:
    """Test overwriting with empty content."""
    test_file = safe_tmp_path / "clear.txt"
    test_file.write_text("content to clear", encoding="utf-8")

    result = overwrite_file(str(test_file), "")
    assert result is True
    assert test_file.read_text(encoding="utf-8") == ""


def test_overwrite_file_multiple_times(safe_tmp_path) -> None:
    """Test overwriting a file multiple times."""
    test_file = safe_tmp_path / "multi.txt"
    test_file.write_text("original", encoding="utf-8")

    overwrite_file(str(test_file), "first overwrite")
    assert test_file.read_text(encoding="utf-8") == "first overwrite"

    overwrite_file(str(test_file), "second overwrite")
    assert test_file.read_text(encoding="utf-8") == "second overwrite"

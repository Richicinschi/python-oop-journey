"""Tests for Problem 01: Write String to File."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day21_writing_files.solutions.problem_01_write_string_to_file import (
    write_string_to_file,
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


def test_write_string_to_file_new_file(safe_tmp_path) -> None:
    """Test writing to a new file."""
    test_file = safe_tmp_path / "new_file.txt"
    content = "Hello, World!"

    result = write_string_to_file(str(test_file), content)
    assert result is True
    assert test_file.read_text(encoding="utf-8") == content


def test_write_string_to_file_overwrite(safe_tmp_path) -> None:
    """Test that writing overwrites existing content."""
    test_file = safe_tmp_path / "existing.txt"
    test_file.write_text("old content", encoding="utf-8")

    new_content = "new content"
    result = write_string_to_file(str(test_file), new_content)
    assert result is True
    assert test_file.read_text(encoding="utf-8") == new_content


def test_write_string_to_file_empty_content(safe_tmp_path) -> None:
    """Test writing empty string to file."""
    test_file = safe_tmp_path / "empty.txt"

    result = write_string_to_file(str(test_file), "")
    assert result is True
    assert test_file.read_text(encoding="utf-8") == ""


def test_write_string_to_file_unicode(safe_tmp_path) -> None:
    """Test writing unicode content."""
    test_file = safe_tmp_path / "unicode.txt"
    content = "Hello 世界 🌍 ñoño"

    result = write_string_to_file(str(test_file), content)
    assert result is True
    assert test_file.read_text(encoding="utf-8") == content


def test_write_string_to_file_multiline(safe_tmp_path) -> None:
    """Test writing multiline content."""
    test_file = safe_tmp_path / "multiline.txt"
    content = "Line 1\nLine 2\nLine 3"

    result = write_string_to_file(str(test_file), content)
    assert result is True
    assert test_file.read_text(encoding="utf-8") == content

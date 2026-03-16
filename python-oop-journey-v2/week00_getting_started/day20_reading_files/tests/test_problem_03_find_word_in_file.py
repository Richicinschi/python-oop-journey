"""Tests for Problem 03: Find Word in File."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day20_reading_files.solutions.problem_03_find_word_in_file import (
    find_word_in_file,
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


def test_find_word_present(safe_tmp_path) -> None:
    """Test finding a word that exists in the file."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("The quick brown fox jumps over the lazy dog.", encoding="utf-8")

    result = find_word_in_file(str(test_file), "fox")
    assert result is True


def test_find_word_not_present(safe_tmp_path) -> None:
    """Test finding a word that doesn't exist in the file."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("The quick brown fox jumps over the lazy dog.", encoding="utf-8")

    result = find_word_in_file(str(test_file), "cat")
    assert result is False


def test_find_word_case_insensitive(safe_tmp_path) -> None:
    """Test that search is case-insensitive."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("The QUICK Brown FoX", encoding="utf-8")

    assert find_word_in_file(str(test_file), "quick") is True
    assert find_word_in_file(str(test_file), "QUICK") is True
    assert find_word_in_file(str(test_file), "Fox") is True


def test_find_word_nonexistent_file() -> None:
    """Test searching in a non-existent file returns None."""
    result = find_word_in_file("/nonexistent/path/file.txt", "word")
    assert result is None


def test_find_word_multiline(safe_tmp_path) -> None:
    """Test finding word across multiple lines."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("First line\nSecond line with target word\nThird line", encoding="utf-8")

    result = find_word_in_file(str(test_file), "target")
    assert result is True

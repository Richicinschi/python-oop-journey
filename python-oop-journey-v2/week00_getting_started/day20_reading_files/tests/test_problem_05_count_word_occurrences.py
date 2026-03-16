"""Tests for Problem 05: Count Word Occurrences."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day20_reading_files.solutions.problem_05_count_word_occurrences import (
    count_word_occurrences,
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


def test_count_word_occurrences_basic(safe_tmp_path) -> None:
    """Test counting word occurrences in a file."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("the cat and the dog and the bird", encoding="utf-8")

    result = count_word_occurrences(str(test_file), "the")
    assert result == 3


def test_count_word_occurrences_case_insensitive(safe_tmp_path) -> None:
    """Test that counting is case-insensitive."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("The THE the tHe", encoding="utf-8")

    result = count_word_occurrences(str(test_file), "the")
    assert result == 4


def test_count_word_occurrences_zero(safe_tmp_path) -> None:
    """Test counting a word that doesn't exist."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("hello world", encoding="utf-8")

    result = count_word_occurrences(str(test_file), "missing")
    assert result == 0


def test_count_word_occurrences_with_punctuation(safe_tmp_path) -> None:
    """Test counting words with surrounding punctuation."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("Hello, world! Hello... HELLO?", encoding="utf-8")

    result = count_word_occurrences(str(test_file), "hello")
    assert result == 3


def test_count_word_occurrences_nonexistent_file() -> None:
    """Test counting in a non-existent file returns None."""
    result = count_word_occurrences("/nonexistent/path/file.txt", "word")
    assert result is None

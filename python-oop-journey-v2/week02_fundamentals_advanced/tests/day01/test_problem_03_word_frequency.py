"""Tests for Problem 03: Word Frequency."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day01.problem_03_word_frequency import word_frequency

import os
import shutil
from pathlib import Path

# Environment workaround for tmp_path permission issues
@pytest.fixture
def safe_tmp_path(monkeypatch):
    """Provide a temporary path that works in restricted environments."""
    test_dir = Path(os.getcwd()) / '.test_tmp'
    test_dir.mkdir(exist_ok=True)
    try:
        yield test_dir
    finally:
        if test_dir.exists():
            shutil.rmtree(test_dir, ignore_errors=True)



def test_word_frequency_basic(safe_tmp_path) -> None:
    """Test basic word frequency counting."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("hello world hello")
    result = word_frequency(test_file)
    assert result == {"hello": 2, "world": 1}


def test_word_frequency_case_insensitive(safe_tmp_path) -> None:
    """Test that counting is case-insensitive."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("Hello HELLO hello")
    result = word_frequency(test_file)
    assert result == {"hello": 3}


def test_word_frequency_strips_punctuation(safe_tmp_path) -> None:
    """Test that punctuation is stripped."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("Hello, world! How are you?")
    result = word_frequency(test_file)
    assert "hello" in result
    assert "world" in result
    assert "hello," not in result
    assert "world!" not in result


def test_word_frequency_empty_file(safe_tmp_path) -> None:
    """Test empty file returns empty dict."""
    test_file = safe_tmp_path / "empty.txt"
    test_file.write_text("")
    assert word_frequency(test_file) == {}


def test_word_frequency_nonexistent_file() -> None:
    """Test non-existent file returns empty dict."""
    assert word_frequency("/nonexistent.txt") == {}


def test_word_frequency_sorted(safe_tmp_path) -> None:
    """Test that result is sorted alphabetically."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("zebra apple mango")
    result = word_frequency(test_file)
    assert list(result.keys()) == ["apple", "mango", "zebra"]


def test_word_frequency_multiple_lines(safe_tmp_path) -> None:
    """Test word frequency across multiple lines."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("hello world\nhello python\nworld python")
    result = word_frequency(test_file)
    assert result == {"hello": 2, "python": 2, "world": 2}


def test_word_frequency_handles_multiple_punctuation(safe_tmp_path) -> None:
    """Test handling multiple punctuation marks."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text('"quoted", (parentheses), [brackets]!')
    result = word_frequency(test_file)
    assert "quoted" in result
    assert "parentheses" in result
    assert "brackets" in result

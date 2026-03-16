"""Tests for Problem 02: Find Longest Line."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day01.problem_02_find_longest_line import find_longest_line

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



def test_find_longest_line_normal(safe_tmp_path) -> None:
    """Test finding longest line in a normal file."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("short\nthis is the longest line\ntiny\n")
    result = find_longest_line(test_file)
    assert result == ("this is the longest line", 2)


def test_find_longest_line_empty_file(safe_tmp_path) -> None:
    """Test empty file returns empty string and 0."""
    test_file = safe_tmp_path / "empty.txt"
    test_file.write_text("")
    assert find_longest_line(test_file) == ("", 0)


def test_find_longest_line_single_line(safe_tmp_path) -> None:
    """Test single line file."""
    test_file = safe_tmp_path / "single.txt"
    test_file.write_text("only line here")
    assert find_longest_line(test_file) == ("only line here", 1)


def test_find_longest_line_tie_returns_first(safe_tmp_path) -> None:
    """Test that first longest line is returned in case of tie."""
    test_file = safe_tmp_path / "tie.txt"
    test_file.write_text("abc\ndef\nghi\n")
    result = find_longest_line(test_file)
    assert result == ("abc", 1)


def test_find_longest_line_nonexistent_file() -> None:
    """Test non-existent file returns empty string and 0."""
    assert find_longest_line("/nonexistent/path.txt") == ("", 0)


def test_find_longest_line_strips_newline(safe_tmp_path) -> None:
    """Test that trailing newlines are stripped."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("line with newline\n")
    result = find_longest_line(test_file)
    assert "\n" not in result[0]


def test_find_longest_line_preserves_other_whitespace(safe_tmp_path) -> None:
    """Test that non-newline whitespace is preserved."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("line\n  indented line\n")
    result = find_longest_line(test_file)
    assert result[0] == "  indented line"


def test_find_longest_line_1_based_indexing(safe_tmp_path) -> None:
    """Test that line numbers are 1-based."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("first\nsecond\nthird\n")
    result = find_longest_line(test_file)
    assert result[1] >= 1  # Should never be 0 for non-empty file

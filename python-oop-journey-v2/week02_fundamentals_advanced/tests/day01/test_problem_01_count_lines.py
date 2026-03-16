"""Tests for Problem 01: Count Lines."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day01.problem_01_count_lines import count_lines

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



def test_count_lines_normal_file(safe_tmp_path) -> None:
    """Test counting lines in a normal file."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("line1\nline2\nline3\n")
    assert count_lines(test_file) == 3


def test_count_lines_empty_file(safe_tmp_path) -> None:
    """Test counting lines in an empty file."""
    test_file = safe_tmp_path / "empty.txt"
    test_file.write_text("")
    assert count_lines(test_file) == 0


def test_count_lines_single_line(safe_tmp_path) -> None:
    """Test counting lines in a single-line file."""
    test_file = safe_tmp_path / "single.txt"
    test_file.write_text("only line")
    assert count_lines(test_file) == 1


def test_count_lines_no_trailing_newline(safe_tmp_path) -> None:
    """Test file without trailing newline."""
    test_file = safe_tmp_path / "no_newline.txt"
    test_file.write_text("line1\nline2")
    assert count_lines(test_file) == 2


def test_count_lines_empty_lines(safe_tmp_path) -> None:
    """Test that empty lines are counted."""
    test_file = safe_tmp_path / "empty_lines.txt"
    test_file.write_text("line1\n\nline3\n")  # 3 lines: line1, empty, line3
    assert count_lines(test_file) == 3


def test_count_lines_nonexistent_file() -> None:
    """Test that non-existent file returns -1."""
    assert count_lines("/path/that/does/not/exist.txt") == -1


def test_count_lines_with_path_object(safe_tmp_path) -> None:
    """Test that function accepts Path objects."""
    test_file = safe_tmp_path / "test.txt"
    test_file.write_text("a\nb\nc\n")
    assert count_lines(test_file) == 3

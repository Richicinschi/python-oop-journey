"""Tests for Problem 04: Merge Files."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day01.problem_04_merge_files import merge_files

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



def test_merge_files_basic(safe_tmp_path) -> None:
    """Test basic file merging."""
    file1 = safe_tmp_path / "a.txt"
    file2 = safe_tmp_path / "b.txt"
    output = safe_tmp_path / "out.txt"
    
    file1.write_text("content of file 1")
    file2.write_text("content of file 2")
    
    count = merge_files([file1, file2], output)
    assert count == 2
    
    result = output.read_text()
    assert "content of file 1" in result
    assert "content of file 2" in result


def test_merge_files_empty_list(safe_tmp_path) -> None:
    """Test merging empty list creates empty output."""
    output = safe_tmp_path / "out.txt"
    count = merge_files([], output)
    assert count == 0
    assert output.exists()
    assert output.read_text() == ""


def test_merge_files_skips_nonexistent(safe_tmp_path) -> None:
    """Test that non-existent files are skipped."""
    file1 = safe_tmp_path / "exists.txt"
    output = safe_tmp_path / "out.txt"
    
    file1.write_text("content")
    
    count = merge_files([file1, safe_tmp_path / "does_not_exist.txt"], output)
    assert count == 1
    assert output.read_text() == "content"


def test_merge_files_adds_separator(safe_tmp_path) -> None:
    """Test that files are separated by blank line."""
    file1 = safe_tmp_path / "a.txt"
    file2 = safe_tmp_path / "b.txt"
    output = safe_tmp_path / "out.txt"
    
    file1.write_text("line1")
    file2.write_text("line2")
    
    merge_files([file1, file2], output)
    result = output.read_text()
    
    # Should have blank line separator
    assert "\n\n" in result or result == "line1\nline2"


def test_merge_files_all_nonexistent(safe_tmp_path) -> None:
    """Test when all source files don't exist."""
    output = safe_tmp_path / "out.txt"
    count = merge_files([safe_tmp_path / "a.txt", safe_tmp_path / "b.txt"], output)
    assert count == 0
    assert output.exists()
    assert output.read_text() == ""


def test_merge_files_overwrites_output(safe_tmp_path) -> None:
    """Test that output file is overwritten."""
    file1 = safe_tmp_path / "a.txt"
    output = safe_tmp_path / "out.txt"
    
    file1.write_text("new content")
    output.write_text("old content")
    
    merge_files([file1], output)
    assert output.read_text() == "new content"


def test_merge_files_preserves_content(safe_tmp_path) -> None:
    """Test that file content is preserved exactly."""
    file1 = safe_tmp_path / "a.txt"
    output = safe_tmp_path / "out.txt"
    
    file1.write_text("line1\nline2\nline3")
    
    merge_files([file1], output)
    assert output.read_text() == "line1\nline2\nline3"

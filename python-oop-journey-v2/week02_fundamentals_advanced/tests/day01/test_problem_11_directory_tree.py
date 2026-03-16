"""Tests for Problem 11: Directory Tree."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day01.problem_11_directory_tree import directory_tree

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



def test_directory_tree_empty_dir(safe_tmp_path) -> None:
    """Test empty directory."""
    result = directory_tree(safe_tmp_path)
    assert safe_tmp_path.name in result
    assert "0 files" in result
    assert "0 directories" in result or "0 directory" in result


def test_directory_tree_with_files(safe_tmp_path) -> None:
    """Test directory with files."""
    (safe_tmp_path / "file1.txt").write_text("content")
    (safe_tmp_path / "file2.txt").write_text("content")
    
    result = directory_tree(safe_tmp_path)
    
    assert "file1.txt" in result
    assert "file2.txt" in result
    assert "2 files" in result


def test_directory_tree_with_subdirectory(safe_tmp_path) -> None:
    """Test directory with subdirectory."""
    subdir = safe_tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file.txt").write_text("content")
    
    result = directory_tree(safe_tmp_path)
    
    assert "subdir" in result
    assert "file.txt" in result
    assert "1 director" in result  # directory or directories


def test_directory_tree_nonexistent_path() -> None:
    """Test non-existent path returns empty string."""
    result = directory_tree("/nonexistent/path/12345")
    assert result == ""


def test_directory_tree_with_filter(safe_tmp_path) -> None:
    """Test filtering by file pattern."""
    (safe_tmp_path / "script.py").write_text("content")
    (safe_tmp_path / "readme.txt").write_text("content")
    (safe_tmp_path / "data.json").write_text("content")
    
    result = directory_tree(safe_tmp_path, include=["*.py"])
    
    assert "script.py" in result
    assert "readme.txt" not in result
    assert "data.json" not in result


def test_directory_tree_multiple_patterns(safe_tmp_path) -> None:
    """Test filtering with multiple patterns."""
    (safe_tmp_path / "a.py").write_text("content")
    (safe_tmp_path / "b.txt").write_text("content")
    (safe_tmp_path / "c.py").write_text("content")
    
    result = directory_tree(safe_tmp_path, include=["*.py", "*.txt"])
    
    assert "a.py" in result
    assert "b.txt" in result
    assert "c.py" in result


def test_directory_tree_subdirs_always_included(safe_tmp_path) -> None:
    """Test that subdirectories are always shown even with filters."""
    subdir = safe_tmp_path / "sub"
    subdir.mkdir()
    (subdir / "file.py").write_text("content")
    
    result = directory_tree(safe_tmp_path, include=["*.txt"])
    
    assert "sub" in result


def test_directory_tree_sorting(safe_tmp_path) -> None:
    """Test that entries are sorted alphabetically."""
    (safe_tmp_path / "zebra.txt").write_text("content")
    (safe_tmp_path / "apple.txt").write_text("content")
    (safe_tmp_path / "mango.txt").write_text("content")
    
    result = directory_tree(safe_tmp_path)
    
    # Check alphabetical order
    zebra_pos = result.find("zebra.txt")
    apple_pos = result.find("apple.txt")
    mango_pos = result.find("mango.txt")
    
    assert apple_pos < mango_pos < zebra_pos


def test_directory_tree_nested_structure(safe_tmp_path) -> None:
    """Test deeply nested directory structure."""
    level1 = safe_tmp_path / "level1"
    level1.mkdir()
    level2 = level1 / "level2"
    level2.mkdir()
    (level2 / "deep.txt").write_text("content")
    
    result = directory_tree(safe_tmp_path)
    
    assert "level1" in result
    assert "level2" in result
    assert "deep.txt" in result

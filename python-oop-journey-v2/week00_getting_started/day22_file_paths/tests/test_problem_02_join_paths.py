"""Tests for Problem 02: Join Paths."""

from __future__ import annotations

from week00_getting_started.day22_file_paths.solutions.problem_02_join_paths import (
    join_paths,
)


def test_join_paths_two_components() -> None:
    """Test joining two path components."""
    result = join_paths("folder", "file.txt")
    # Check that both components are in the path (works on all OS)
    assert "folder" in result
    assert "file.txt" in result
    # On Windows, result might be "folder\file.txt"
    # On Unix, result is "folder/file.txt"


def test_join_paths_multiple_components() -> None:
    """Test joining multiple path components."""
    result = join_paths("home", "user", "documents", "file.txt")
    assert "home" in result
    assert "user" in result
    assert "documents" in result
    assert "file.txt" in result


def test_join_paths_with_empty() -> None:
    """Test joining with empty string."""
    result = join_paths("folder", "")
    assert "folder" in result


def test_join_paths_single_component() -> None:
    """Test with only base path."""
    result = join_paths("file.txt")
    assert result == "file.txt"


def test_join_paths_absolute_base() -> None:
    """Test joining with absolute base path."""
    result = join_paths("/home", "user", "file.txt")
    # On Unix: /home/user/file.txt, On Windows: \home\user\file.txt
    assert "home" in result
    assert "user" in result
    assert "file.txt" in result

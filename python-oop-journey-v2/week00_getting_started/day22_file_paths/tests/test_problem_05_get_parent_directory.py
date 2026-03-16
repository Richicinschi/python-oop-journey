"""Tests for Problem 05: Get Parent Directory."""

from __future__ import annotations

from week00_getting_started.day22_file_paths.solutions.problem_05_get_parent_directory import (
    get_parent_directory,
)


def test_get_parent_directory_one_level() -> None:
    """Test getting parent directory (one level)."""
    result = get_parent_directory("/home/user/document.txt")
    assert "home" in result
    assert "user" in result
    assert "document.txt" not in result


def test_get_parent_directory_multiple_levels() -> None:
    """Test getting parent directory (multiple levels)."""
    result = get_parent_directory("/home/user/documents/files/report.txt", levels=3)
    # After 3 levels up from report.txt: we're at /home/user (Unix) or \home\user (Windows)
    # The deeper directories should not be in the result
    assert "documents" not in result
    assert "files" not in result
    assert "report.txt" not in result
    # The remaining path should include 'home' and 'user'
    assert "home" in result
    assert "user" in result


def test_get_parent_directory_relative_path() -> None:
    """Test with relative path."""
    result = get_parent_directory("folder/subfolder/file.txt")
    assert "folder" in result
    assert "subfolder" in result
    assert "file.txt" not in result


def test_get_parent_directory_file_only() -> None:
    """Test with filename only."""
    result = get_parent_directory("file.txt")
    assert result == "."


def test_get_parent_directory_default_level() -> None:
    """Test default level is 1."""
    result = get_parent_directory("/a/b/c/d.txt")
    assert "a" in result
    assert "b" in result
    assert "c" in result
    assert "d.txt" not in result

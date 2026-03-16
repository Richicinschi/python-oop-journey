"""Tests for Problem 03: Get Filename Without Extension."""

from __future__ import annotations

from week00_getting_started.day22_file_paths.solutions.problem_03_get_filename_without_ext import (
    get_filename_without_ext,
)


def test_get_filename_without_ext_simple() -> None:
    """Test simple filename."""
    result = get_filename_without_ext("document.txt")
    assert result == "document"


def test_get_filename_without_ext_multiple_dots() -> None:
    """Test filename with multiple dots."""
    result = get_filename_without_ext("archive.tar.gz")
    assert result == "archive.tar"


def test_get_filename_without_ext_no_extension() -> None:
    """Test filename without extension."""
    result = get_filename_without_ext("README")
    assert result == "README"


def test_get_filename_without_ext_full_path() -> None:
    """Test with full path."""
    result = get_filename_without_ext("/home/user/script.py")
    assert result == "script"


def test_get_filename_without_ext_hidden_file() -> None:
    """Test hidden file starting with dot."""
    result = get_filename_without_ext(".bashrc")
    assert result == ".bashrc"

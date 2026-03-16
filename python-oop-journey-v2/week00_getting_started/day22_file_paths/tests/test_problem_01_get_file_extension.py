"""Tests for Problem 01: Get File Extension."""

from __future__ import annotations

from week00_getting_started.day22_file_paths.solutions.problem_01_get_file_extension import (
    get_file_extension,
)


def test_get_file_extension_txt() -> None:
    """Test getting .txt extension."""
    result = get_file_extension("document.txt")
    assert result == ".txt"


def test_get_file_extension_py() -> None:
    """Test getting .py extension."""
    result = get_file_extension("script.py")
    assert result == ".py"


def test_get_file_extension_multiple_dots() -> None:
    """Test file with multiple dots."""
    result = get_file_extension("archive.tar.gz")
    assert result == ".gz"


def test_get_file_extension_no_extension() -> None:
    """Test file without extension."""
    result = get_file_extension("README")
    assert result == ""


def test_get_file_extension_full_path() -> None:
    """Test with full path."""
    result = get_file_extension("/home/user/document.pdf")
    assert result == ".pdf"


def test_get_file_extension_hidden_file() -> None:
    """Test hidden file starting with dot."""
    result = get_file_extension(".gitignore")
    assert result == ""


def test_get_file_extension_uppercase() -> None:
    """Test uppercase extension."""
    result = get_file_extension("image.PNG")
    assert result == ".PNG"

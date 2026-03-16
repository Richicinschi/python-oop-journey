"""Tests for Problem 04: Path Exists."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day22_file_paths.solutions.problem_04_path_exists import (
    path_exists,
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


def test_path_exists_file(safe_tmp_path) -> None:
    """Test existing file returns True."""
    test_file = safe_tmp_path / "exists.txt"
    test_file.write_text("content", encoding="utf-8")

    result = path_exists(str(test_file))
    assert result is True


def test_path_exists_directory(safe_tmp_path) -> None:
    """Test existing directory returns True."""
    test_dir = safe_tmp_path / "test_folder"
    test_dir.mkdir()

    result = path_exists(str(test_dir))
    assert result is True


def test_path_exists_nonexistent(safe_tmp_path) -> None:
    """Test non-existent path returns False."""
    nonexistent = safe_tmp_path / "does_not_exist.txt"

    result = path_exists(str(nonexistent))
    assert result is False


def test_path_exists_nested_nonexistent(safe_tmp_path) -> None:
    """Test nested non-existent path returns False."""
    nonexistent = safe_tmp_path / "folder" / "subfolder" / "file.txt"

    result = path_exists(str(nonexistent))
    assert result is False

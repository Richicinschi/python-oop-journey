"""Tests for Problem 04: Create New File."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day21_writing_files.solutions.problem_04_create_new_file import (
    create_new_file,
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


def test_create_new_file_success(safe_tmp_path) -> None:
    """Test creating a new file."""
    test_file = safe_tmp_path / "new_file.txt"

    result = create_new_file(str(test_file))
    assert result is True
    assert test_file.exists()
    assert test_file.read_text(encoding="utf-8") == ""


def test_create_new_file_with_content(safe_tmp_path) -> None:
    """Test creating a new file with initial content."""
    test_file = safe_tmp_path / "with_content.txt"
    content = "Initial content"

    result = create_new_file(str(test_file), content)
    assert result is True
    assert test_file.exists()
    assert test_file.read_text(encoding="utf-8") == content


def test_create_new_file_already_exists(safe_tmp_path) -> None:
    """Test creating a file that already exists."""
    test_file = safe_tmp_path / "existing.txt"
    test_file.write_text("existing content", encoding="utf-8")

    result = create_new_file(str(test_file), "new content")
    assert result is False
    assert test_file.read_text(encoding="utf-8") == "existing content"


def test_create_new_file_preserves_existing(safe_tmp_path) -> None:
    """Test that existing file content is not modified."""
    test_file = safe_tmp_path / "preserve.txt"
    original_content = "Do not change me"
    test_file.write_text(original_content, encoding="utf-8")

    create_new_file(str(test_file), "Change me")
    assert test_file.read_text(encoding="utf-8") == original_content

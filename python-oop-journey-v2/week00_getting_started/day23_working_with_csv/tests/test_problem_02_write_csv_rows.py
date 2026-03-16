"""Tests for Problem 02: Write CSV Rows."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day23_working_with_csv.solutions.problem_02_write_csv_rows import (
    write_csv_rows,
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


def test_write_csv_rows_basic(safe_tmp_path) -> None:
    """Test writing CSV rows."""
    test_file = safe_tmp_path / "output.csv"
    rows = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]

    result = write_csv_rows(str(test_file), rows)
    assert result is True
    content = test_file.read_text(encoding="utf-8")
    # Normalize line endings for cross-platform comparison
    assert content.replace("\r\n", "\n") == "Name,Age\nAlice,30\nBob,25\n"


def test_write_csv_rows_empty(safe_tmp_path) -> None:
    """Test writing empty list creates empty file."""
    test_file = safe_tmp_path / "empty.csv"
    rows: list[list[str]] = []

    result = write_csv_rows(str(test_file), rows)
    assert result is True
    assert test_file.read_text(encoding="utf-8") == ""


def test_write_csv_rows_single_row(safe_tmp_path) -> None:
    """Test writing single row."""
    test_file = safe_tmp_path / "single.csv"
    rows = [["a", "b", "c"]]

    result = write_csv_rows(str(test_file), rows)
    assert result is True
    content = test_file.read_text(encoding="utf-8")
    # Normalize line endings for cross-platform comparison
    assert content.replace("\r\n", "\n") == "a,b,c\n"


def test_write_csv_rows_overwrite(safe_tmp_path) -> None:
    """Test writing overwrites existing file."""
    test_file = safe_tmp_path / "existing.csv"
    test_file.write_text("old,data", encoding="utf-8")

    rows = [["new", "data"]]
    result = write_csv_rows(str(test_file), rows)
    assert result is True
    content = test_file.read_text(encoding="utf-8")
    assert "old" not in content
    assert "new" in content

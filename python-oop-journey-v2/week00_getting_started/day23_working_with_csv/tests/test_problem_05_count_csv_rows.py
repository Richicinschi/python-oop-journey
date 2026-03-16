"""Tests for Problem 05: Count CSV Rows."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day23_working_with_csv.solutions.problem_05_count_csv_rows import (
    count_csv_rows,
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


def test_count_csv_rows_with_header(safe_tmp_path) -> None:
    """Test counting rows with header (default)."""
    test_file = safe_tmp_path / "data.csv"
    test_file.write_text("Name,Age\nAlice,30\nBob,25\nCharlie,35", encoding="utf-8")

    result = count_csv_rows(str(test_file))
    assert result == 3  # 4 total - 1 header = 3 data rows


def test_count_csv_rows_no_header(safe_tmp_path) -> None:
    """Test counting rows without header."""
    test_file = safe_tmp_path / "data.csv"
    test_file.write_text("Alice,30\nBob,25\nCharlie,35", encoding="utf-8")

    result = count_csv_rows(str(test_file), has_header=False)
    assert result == 3


def test_count_csv_rows_empty_file(safe_tmp_path) -> None:
    """Test counting rows in empty file."""
    test_file = safe_tmp_path / "empty.csv"
    test_file.write_text("", encoding="utf-8")

    result = count_csv_rows(str(test_file))
    assert result == 0


def test_count_csv_rows_header_only(safe_tmp_path) -> None:
    """Test counting rows with only header."""
    test_file = safe_tmp_path / "header_only.csv"
    test_file.write_text("Name,Age", encoding="utf-8")

    result = count_csv_rows(str(test_file))
    assert result == 0


def test_count_csv_rows_nonexistent_file() -> None:
    """Test counting rows in non-existent file."""
    result = count_csv_rows("/nonexistent/path/data.csv")
    assert result is None

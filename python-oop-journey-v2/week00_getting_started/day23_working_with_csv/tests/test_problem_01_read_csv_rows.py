"""Tests for Problem 01: Read CSV Rows."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day23_working_with_csv.solutions.problem_01_read_csv_rows import (
    read_csv_rows,
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


def test_read_csv_rows_basic(safe_tmp_path) -> None:
    """Test reading basic CSV rows."""
    test_file = safe_tmp_path / "data.csv"
    test_file.write_text("Name,Age\nAlice,30\nBob,25", encoding="utf-8")

    result = read_csv_rows(str(test_file))
    assert result == [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]


def test_read_csv_rows_empty_file(safe_tmp_path) -> None:
    """Test reading empty CSV file."""
    test_file = safe_tmp_path / "empty.csv"
    test_file.write_text("", encoding="utf-8")

    result = read_csv_rows(str(test_file))
    assert result == []


def test_read_csv_rows_single_row(safe_tmp_path) -> None:
    """Test reading CSV with single row."""
    test_file = safe_tmp_path / "single.csv"
    test_file.write_text("a,b,c", encoding="utf-8")

    result = read_csv_rows(str(test_file))
    assert result == [["a", "b", "c"]]


def test_read_csv_rows_with_quotes(safe_tmp_path) -> None:
    """Test reading CSV with quoted fields."""
    test_file = safe_tmp_path / "quoted.csv"
    test_file.write_text('Name,Description\n"Doe, John","A, person"', encoding="utf-8")

    result = read_csv_rows(str(test_file))
    assert result == [["Name", "Description"], ["Doe, John", "A, person"]]


def test_read_csv_rows_nonexistent_file() -> None:
    """Test reading non-existent file returns None."""
    result = read_csv_rows("/nonexistent/path/data.csv")
    assert result is None

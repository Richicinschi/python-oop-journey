"""Tests for Problem 03: Read CSV as Dict."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day23_working_with_csv.solutions.problem_03_read_csv_dict import (
    read_csv_dict,
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


def test_read_csv_dict_basic(safe_tmp_path) -> None:
    """Test reading CSV as list of dictionaries."""
    test_file = safe_tmp_path / "data.csv"
    test_file.write_text("Name,Age,City\nAlice,30,NYC\nBob,25,LA", encoding="utf-8")

    result = read_csv_dict(str(test_file))
    assert result == [
        {"Name": "Alice", "Age": "30", "City": "NYC"},
        {"Name": "Bob", "Age": "25", "City": "LA"},
    ]


def test_read_csv_dict_empty_file(safe_tmp_path) -> None:
    """Test reading empty CSV file."""
    test_file = safe_tmp_path / "empty.csv"
    test_file.write_text("", encoding="utf-8")

    result = read_csv_dict(str(test_file))
    assert result == []


def test_read_csv_dict_only_header(safe_tmp_path) -> None:
    """Test reading CSV with only header row."""
    test_file = safe_tmp_path / "header_only.csv"
    test_file.write_text("Name,Age,City", encoding="utf-8")

    result = read_csv_dict(str(test_file))
    assert result == []


def test_read_csv_dict_nonexistent_file() -> None:
    """Test reading non-existent file returns None."""
    result = read_csv_dict("/nonexistent/path/data.csv")
    assert result is None

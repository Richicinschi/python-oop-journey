"""Tests for Problem 04: Write CSV from Dict."""

from __future__ import annotations

from pathlib import Path

import pytest

from week00_getting_started.day23_working_with_csv.solutions.problem_04_write_csv_dict import (
    write_csv_dict,
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


def test_write_csv_dict_basic(safe_tmp_path) -> None:
    """Test writing dictionaries to CSV."""
    test_file = safe_tmp_path / "output.csv"
    fieldnames = ["Name", "Age", "City"]
    data = [
        {"Name": "Alice", "Age": "30", "City": "NYC"},
        {"Name": "Bob", "Age": "25", "City": "LA"},
    ]

    result = write_csv_dict(str(test_file), data, fieldnames)
    assert result is True
    content = test_file.read_text(encoding="utf-8")
    assert "Name,Age,City" in content
    assert "Alice,30,NYC" in content


def test_write_csv_dict_empty_data(safe_tmp_path) -> None:
    """Test writing empty data with headers only."""
    test_file = safe_tmp_path / "empty.csv"
    fieldnames = ["Name", "Age"]
    data: list[dict[str, str]] = []

    result = write_csv_dict(str(test_file), data, fieldnames)
    assert result is True
    content = test_file.read_text(encoding="utf-8")
    assert "Name,Age" in content


def test_write_csv_dict_different_order(safe_tmp_path) -> None:
    """Test that fieldnames control column order."""
    test_file = safe_tmp_path / "ordered.csv"
    fieldnames = ["City", "Name", "Age"]
    data = [{"Name": "Alice", "Age": "30", "City": "NYC"}]

    result = write_csv_dict(str(test_file), data, fieldnames)
    assert result is True
    content = test_file.read_text(encoding="utf-8")
    assert content.startswith("City,Name,Age")

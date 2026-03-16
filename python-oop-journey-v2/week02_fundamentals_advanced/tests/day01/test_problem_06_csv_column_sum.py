"""Tests for Problem 06: CSV Column Sum."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day01.problem_06_csv_column_sum import csv_column_sum

import os
import shutil
from pathlib import Path

# Environment workaround for tmp_path permission issues
@pytest.fixture
def safe_tmp_path(monkeypatch):
    """Provide a temporary path that works in restricted environments."""
    test_dir = Path(os.getcwd()) / '.test_tmp'
    test_dir.mkdir(exist_ok=True)
    try:
        yield test_dir
    finally:
        if test_dir.exists():
            shutil.rmtree(test_dir, ignore_errors=True)



def test_csv_column_sum_basic(safe_tmp_path) -> None:
    """Test basic CSV column sum."""
    csv_file = safe_tmp_path / "data.csv"
    csv_file.write_text("name,price,quantity\nApple,1.50,10\nBanana,0.75,20\n")
    
    result = csv_column_sum(csv_file, "price")
    assert result == 2.25


def test_csv_column_sum_nonexistent_column(safe_tmp_path) -> None:
    """Test non-existent column returns 0.0."""
    csv_file = safe_tmp_path / "data.csv"
    csv_file.write_text("name,price\nApple,1.50\n")
    
    result = csv_column_sum(csv_file, "nonexistent")
    assert result == 0.0


def test_csv_column_sum_nonexistent_file() -> None:
    """Test non-existent file returns 0.0."""
    result = csv_column_sum("/nonexistent.csv", "price")
    assert result == 0.0


def test_csv_column_sum_integers(safe_tmp_path) -> None:
    """Test summing integer values."""
    csv_file = safe_tmp_path / "data.csv"
    csv_file.write_text("item,quantity\nA,10\nB,20\nC,30\n")
    
    result = csv_column_sum(csv_file, "quantity")
    assert result == 60.0


def test_csv_column_sum_skips_non_numeric(safe_tmp_path) -> None:
    """Test that non-numeric values are skipped."""
    csv_file = safe_tmp_path / "data.csv"
    csv_file.write_text("name,value\nA,10\nB,N/A\nC,20\n")
    
    result = csv_column_sum(csv_file, "value")
    assert result == 30.0


def test_csv_column_sum_empty_file(safe_tmp_path) -> None:
    """Test empty CSV file."""
    csv_file = safe_tmp_path / "empty.csv"
    csv_file.write_text("")
    
    result = csv_column_sum(csv_file, "price")
    assert result == 0.0


def test_csv_column_sum_empty_column(safe_tmp_path) -> None:
    """Test CSV with empty values in column."""
    csv_file = safe_tmp_path / "data.csv"
    csv_file.write_text("name,price\nA,\nB,5.0\n")
    
    result = csv_column_sum(csv_file, "price")
    assert result == 5.0


def test_csv_column_sum_mixed_float_int(safe_tmp_path) -> None:
    """Test summing mixed float and integer values."""
    csv_file = safe_tmp_path / "data.csv"
    csv_file.write_text("item,value\nA,10\nB,2.5\nC,3.5\n")
    
    result = csv_column_sum(csv_file, "value")
    assert result == 16.0


def test_csv_column_sum_negative_values(safe_tmp_path) -> None:
    """Test summing negative values."""
    csv_file = safe_tmp_path / "data.csv"
    csv_file.write_text("item,value\nA,-10\nB,20\nC,-5\n")
    
    result = csv_column_sum(csv_file, "value")
    assert result == 5.0

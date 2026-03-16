"""Tests for Problem 03: Safe File Reader with Statistics."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from week00_getting_started.solutions.day29.problem_03_safe_file_reader import (
    compute_file_stats,
    read_numbers_from_file,
)


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


@pytest.fixture
def sample_data_file(safe_tmp_path):
    """Create a sample data file with numbers."""
    test_file = safe_tmp_path / "numbers.txt"
    test_file.write_text("10\n20\n30\n40\n50\n")
    return test_file


def test_read_numbers_from_file_success(safe_tmp_path):
    """Test reading valid numbers from a file."""
    test_file = safe_tmp_path / "test_numbers.txt"
    test_file.write_text("1\n2\n3\n4\n5\n")
    
    result = read_numbers_from_file(str(test_file))
    assert result == [1, 2, 3, 4, 5]


def test_read_numbers_empty_file(safe_tmp_path):
    """Test reading from an empty file."""
    test_file = safe_tmp_path / "empty.txt"
    test_file.write_text("")
    
    result = read_numbers_from_file(str(test_file))
    assert result == []


def test_compute_file_stats_success(safe_tmp_path):
    """Test computing statistics from a valid file."""
    test_file = safe_tmp_path / "stats_test.txt"
    test_file.write_text("10\n20\n30\n40\n50\n")
    
    result = compute_file_stats(str(test_file))
    assert result is not None
    assert result["count"] == 5
    assert result["sum"] == 150
    assert result["average"] == 30.0
    assert result["min"] == 10
    assert result["max"] == 50


def test_compute_file_stats_empty_file(safe_tmp_path):
    """Test computing statistics from an empty file."""
    test_file = safe_tmp_path / "empty.txt"
    test_file.write_text("")
    
    result = compute_file_stats(str(test_file))
    assert result is None


def test_compute_file_stats_with_invalid_lines(safe_tmp_path):
    """Test computing statistics with some invalid lines."""
    test_file = safe_tmp_path / "mixed.txt"
    test_file.write_text("10\ninvalid\n20\nnot_a_number\n30\n")
    
    result = compute_file_stats(str(test_file))
    assert result is not None
    assert result["count"] == 3
    assert result["sum"] == 60


def test_compute_file_stats_negative_numbers(safe_tmp_path):
    """Test computing statistics with negative numbers."""
    test_file = safe_tmp_path / "negative.txt"
    test_file.write_text("-10\n-20\n10\n20\n")
    
    result = compute_file_stats(str(test_file))
    assert result is not None
    assert result["count"] == 4
    assert result["sum"] == 0
    assert result["min"] == -20
    assert result["max"] == 20

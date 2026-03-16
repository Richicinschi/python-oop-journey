"""Tests for Problem 10: Report Generator."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from week00_getting_started.solutions.day29.problem_10_report_generator import (
    format_table,
    generate_csv_report,
    generate_statistics_report,
    generate_summary_report,
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


def test_format_table_with_valid_data():
    """Test formatting data as a table."""
    headers = ["Name", "Age", "City"]
    rows = [
        ["Alice", "30", "NYC"],
        ["Bob", "25", "LA"],
    ]
    result = format_table(headers, rows)
    assert "Name" in result
    assert "Alice" in result
    assert "Bob" in result


def test_format_table_empty_rows():
    """Test formatting with empty rows."""
    headers = ["Name", "Value"]
    rows = []
    result = format_table(headers, rows)
    assert "Name" in result


def test_generate_summary_report_with_sales_data():
    """Test generating summary report for sales data."""
    data = {
        "product_a": [100, 200, 300],
        "product_b": [50, 75, 100],
    }
    result = generate_summary_report("Sales Report", data)
    assert "Sales Report" in result
    assert "product_a" in result
    assert "product_b" in result
    assert "Total" in result or "600" in result or "225" in result


def test_generate_summary_report_empty_data():
    """Test generating summary report with empty data."""
    data = {}
    result = generate_summary_report("Empty Report", data)
    assert "Empty Report" in result


def test_generate_statistics_report():
    """Test generating statistics report."""
    values = [10, 20, 30, 40, 50]
    result = generate_statistics_report("Test Stats", values)
    assert "Test Stats" in result
    assert "Count" in result or "5" in result


def test_generate_statistics_report_empty():
    """Test generating statistics report with empty list."""
    result = generate_statistics_report("Empty Stats", [])
    assert "Empty Stats" in result or "N/A" in result or "n/a" in result


def test_generate_csv_report_success(safe_tmp_path):
    """Test generating CSV report file."""
    headers = ["Name", "Age", "City"]
    rows = [
        ["Alice", "30", "NYC"],
        ["Bob", "25", "LA"],
    ]
    output_path = safe_tmp_path / "test_report.csv"
    
    result = generate_csv_report(str(output_path), headers, rows)
    assert result is True
    assert output_path.exists()
    
    content = output_path.read_text()
    assert "Name" in content
    assert "Alice" in content


def test_generate_csv_report_empty_rows(safe_tmp_path):
    """Test generating CSV report with empty rows."""
    headers = ["Name", "Value"]
    rows = []
    output_path = safe_tmp_path / "empty_report.csv"
    
    result = generate_csv_report(str(output_path), headers, rows)
    assert result is True
    assert output_path.exists()

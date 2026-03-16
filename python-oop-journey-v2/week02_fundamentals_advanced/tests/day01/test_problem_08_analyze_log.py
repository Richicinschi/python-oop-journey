"""Tests for Problem 08: Analyze Log."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day01.problem_08_analyze_log import analyze_log

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



def test_analyze_log_basic(safe_tmp_path) -> None:
    """Test basic log analysis."""
    log_file = safe_tmp_path / "app.log"
    log_file.write_text(
        "ERROR: Something went wrong\n"
        "INFO: Normal operation\n"
        "WARNING: Low disk space\n"
        "DEBUG: Detailed info\n"
    )
    
    result = analyze_log(log_file)
    
    assert result["ERROR"] == 1
    assert result["INFO"] == 1
    assert result["WARNING"] == 1
    assert result["DEBUG"] == 1
    assert result["total_lines"] == 4
    assert result["unknown_lines"] == 0


def test_analyze_log_case_insensitive(safe_tmp_path) -> None:
    """Test case-insensitive log level detection."""
    log_file = safe_tmp_path / "app.log"
    log_file.write_text(
        "error: lowercase\n"
        "ERROR: uppercase\n"
        "Error: mixed case\n"
    )
    
    result = analyze_log(log_file)
    
    assert result["ERROR"] == 3


def test_analyze_log_various_formats(safe_tmp_path) -> None:
    """Test various log level formats."""
    log_file = safe_tmp_path / "app.log"
    log_file.write_text(
        "ERROR: colon format\n"
        "INFO - dash format\n"
        "WARNING space format\n"
    )
    
    result = analyze_log(log_file)
    
    assert result["ERROR"] == 1
    assert result["INFO"] == 1
    assert result["WARNING"] == 1


def test_analyze_log_unknown_lines(safe_tmp_path) -> None:
    """Test counting unknown lines."""
    log_file = safe_tmp_path / "app.log"
    log_file.write_text(
        "ERROR: valid\n"
        "Random line without level\n"
        "Another random line\n"
    )
    
    result = analyze_log(log_file)
    
    assert result["ERROR"] == 1
    assert result["unknown_lines"] == 2
    assert result["total_lines"] == 3


def test_analyze_log_nonexistent_file() -> None:
    """Test non-existent file returns zeros."""
    result = analyze_log("/nonexistent.log")
    
    assert result["ERROR"] == 0
    assert result["WARNING"] == 0
    assert result["INFO"] == 0
    assert result["DEBUG"] == 0
    assert result["total_lines"] == 0
    assert result["unknown_lines"] == 0


def test_analyze_log_empty_file(safe_tmp_path) -> None:
    """Test empty log file."""
    log_file = safe_tmp_path / "empty.log"
    log_file.write_text("")
    
    result = analyze_log(log_file)
    
    assert result["total_lines"] == 0
    assert result["unknown_lines"] == 0


def test_analyze_log_empty_lines(safe_tmp_path) -> None:
    """Test that empty lines are counted as unknown."""
    log_file = safe_tmp_path / "app.log"
    log_file.write_text(
        "ERROR: valid\n"
        "\n"
        "INFO: also valid\n"
    )
    
    result = analyze_log(log_file)
    
    assert result["total_lines"] == 3
    assert result["unknown_lines"] == 1


def test_analyze_log_level_only(safe_tmp_path) -> None:
    """Test line with just the log level."""
    log_file = safe_tmp_path / "app.log"
    log_file.write_text("ERROR\n")
    
    result = analyze_log(log_file)
    
    assert result["ERROR"] == 1
    assert result["unknown_lines"] == 0

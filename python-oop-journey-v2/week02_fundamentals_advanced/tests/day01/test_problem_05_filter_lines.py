"""Tests for Problem 05: Filter Lines."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day01.problem_05_filter_lines import filter_lines

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



def test_filter_lines_basic(safe_tmp_path) -> None:
    """Test basic line filtering."""
    input_file = safe_tmp_path / "input.txt"
    output_file = safe_tmp_path / "output.txt"
    
    input_file.write_text("ERROR: something\nINFO: normal\nERROR: again\n")
    
    count = filter_lines(input_file, output_file, "ERROR")
    assert count == 2
    
    result = output_file.read_text()
    assert "ERROR: something" in result
    assert "ERROR: again" in result
    assert "INFO" not in result


def test_filter_lines_no_matches(safe_tmp_path) -> None:
    """Test when no lines match pattern."""
    input_file = safe_tmp_path / "input.txt"
    output_file = safe_tmp_path / "output.txt"
    
    input_file.write_text("line1\nline2\n")
    
    count = filter_lines(input_file, output_file, "NOTFOUND")
    assert count == 0
    assert output_file.exists()
    assert output_file.read_text() == ""


def test_filter_lines_nonexistent_input(safe_tmp_path) -> None:
    """Test non-existent input file returns -1."""
    output_file = safe_tmp_path / "output.txt"
    result = filter_lines(safe_tmp_path / "nonexistent.txt", output_file, "pattern")
    assert result == -1


def test_filter_lines_case_sensitive(safe_tmp_path) -> None:
    """Test that pattern matching is case-sensitive."""
    input_file = safe_tmp_path / "input.txt"
    output_file = safe_tmp_path / "output.txt"
    
    input_file.write_text("ERROR\nerror\nError\n")
    
    count = filter_lines(input_file, output_file, "ERROR")
    assert count == 1
    
    result = output_file.read_text()
    assert result == "ERROR\n"


def test_filter_lines_preserves_newlines(safe_tmp_path) -> None:
    """Test that original line endings are preserved."""
    input_file = safe_tmp_path / "input.txt"
    output_file = safe_tmp_path / "output.txt"
    
    input_file.write_text("match line\nother line\n")
    
    filter_lines(input_file, output_file, "match")
    result = output_file.read_text()
    
    assert result == "match line\n"


def test_filter_lines_empty_file(safe_tmp_path) -> None:
    """Test filtering empty file."""
    input_file = safe_tmp_path / "empty.txt"
    output_file = safe_tmp_path / "output.txt"
    
    input_file.write_text("")
    
    count = filter_lines(input_file, output_file, "anything")
    assert count == 0
    assert output_file.read_text() == ""

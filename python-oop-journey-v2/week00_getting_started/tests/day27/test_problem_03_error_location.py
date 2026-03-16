"""Tests for Problem 03: Error Location."""

from __future__ import annotations

from week00_getting_started.solutions.day27.problem_03_error_location import (
    locate_error,
)


def test_value_error() -> None:
    """Test locating ValueError."""
    traceback = 'File "test.py", line 15\nValueError: invalid input'
    result = locate_error(traceback)
    assert result == {"file": "test.py", "line": 15, "error": "ValueError"}


def test_type_error() -> None:
    """Test locating TypeError."""
    traceback = 'File "main.py", line 42\nTypeError: unsupported type'
    result = locate_error(traceback)
    assert result == {"file": "main.py", "line": 42, "error": "TypeError"}


def test_key_error() -> None:
    """Test locating KeyError."""
    traceback = 'File "data.py", line 100\nKeyError: missing_key'
    result = locate_error(traceback)
    assert result == {"file": "data.py", "line": 100, "error": "KeyError"}


def test_different_filename() -> None:
    """Test with different filename format."""
    traceback = 'File "my_module_v2.py", line 7\nIndexError: list index out of range'
    result = locate_error(traceback)
    assert result == {"file": "my_module_v2.py", "line": 7, "error": "IndexError"}

"""Tests for Problem 03: Parse Traceback."""

from __future__ import annotations

from week00_getting_started.solutions.day24.problem_03_parse_traceback import (
    parse_traceback,
)


def test_parse_zero_division() -> None:
    """Test parsing ZeroDivisionError traceback."""
    result = parse_traceback("ZeroDivisionError: division by zero at line 5")
    assert result == {
        "error_type": "ZeroDivisionError",
        "message": "division by zero",
        "line": 5,
    }


def test_parse_name_error() -> None:
    """Test parsing NameError traceback."""
    result = parse_traceback("NameError: name 'x' is not defined at line 10")
    assert result == {
        "error_type": "NameError",
        "message": "name 'x' is not defined",
        "line": 10,
    }


def test_parse_type_error() -> None:
    """Test parsing TypeError traceback."""
    result = parse_traceback("TypeError: unsupported operand type(s) at line 15")
    assert result == {
        "error_type": "TypeError",
        "message": "unsupported operand type(s)",
        "line": 15,
    }


def test_parse_value_error() -> None:
    """Test parsing ValueError traceback."""
    result = parse_traceback("ValueError: invalid literal for int() at line 20")
    assert result == {
        "error_type": "ValueError",
        "message": "invalid literal for int()",
        "line": 20,
    }


def test_parse_index_error() -> None:
    """Test parsing IndexError traceback."""
    result = parse_traceback("IndexError: list index out of range at line 25")
    assert result == {
        "error_type": "IndexError",
        "message": "list index out of range",
        "line": 25,
    }

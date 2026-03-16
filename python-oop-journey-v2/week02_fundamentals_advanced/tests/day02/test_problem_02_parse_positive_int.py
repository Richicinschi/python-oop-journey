"""Tests for Problem 02: Parse Positive Integer."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day02.problem_02_parse_positive_int import (
    parse_positive_int,
)


def test_parse_positive_int_valid() -> None:
    """Test parsing valid positive integers."""
    assert parse_positive_int("42") == 42
    assert parse_positive_int("1") == 1
    assert parse_positive_int("999999") == 999999


def test_parse_positive_int_with_whitespace() -> None:
    """Test parsing with whitespace stripping."""
    assert parse_positive_int("  42  ") == 42
    assert parse_positive_int("  100") == 100
    assert parse_positive_int("100  ") == 100


def test_parse_positive_int_zero() -> None:
    """Test parsing zero returns error."""
    result = parse_positive_int("0")
    assert result == "Error: Value must be positive"


def test_parse_positive_int_negative() -> None:
    """Test parsing negative numbers returns error."""
    result = parse_positive_int("-5")
    assert result == "Error: Value must be positive"
    result = parse_positive_int("-100")
    assert result == "Error: Value must be positive"


def test_parse_positive_int_invalid_format() -> None:
    """Test parsing invalid strings returns error."""
    result = parse_positive_int("abc")
    assert result == "Error: Invalid integer format"
    
    result = parse_positive_int("12.34")
    assert result == "Error: Invalid integer format"
    
    result = parse_positive_int("10abc")
    assert result == "Error: Invalid integer format"
    
    result = parse_positive_int("")
    assert result == "Error: Invalid integer format"


def test_parse_positive_int_float_string() -> None:
    """Test parsing float strings returns error."""
    result = parse_positive_int("3.14")
    assert result == "Error: Invalid integer format"

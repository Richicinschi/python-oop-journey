"""Tests for Problem 09: Validate and Convert."""

from __future__ import annotations

from week01_fundamentals.solutions.day01.problem_09_validate_and_convert import validate_and_convert


def test_valid_positive_integer() -> None:
    """Test valid positive integer strings."""
    assert validate_and_convert("123") == 123
    assert validate_and_convert("0") == 0
    assert validate_and_convert("999999") == 999999


def test_valid_negative_integer() -> None:
    """Test valid negative integer strings."""
    assert validate_and_convert("-456") == -456
    assert validate_and_convert("-1") == -1
    assert validate_and_convert("-999999") == -999999


def test_invalid_float_string() -> None:
    """Test float strings are invalid."""
    assert validate_and_convert("12.34") is None
    assert validate_and_convert("0.5") is None
    assert validate_and_convert("-3.14") is None


def test_invalid_non_numeric() -> None:
    """Test non-numeric strings are invalid."""
    assert validate_and_convert("abc") is None
    assert validate_and_convert("12abc") is None
    assert validate_and_convert("abc12") is None
    assert validate_and_convert("12 34") is None


def test_empty_string() -> None:
    """Test empty strings are invalid."""
    assert validate_and_convert("") is None


def test_whitespace_only() -> None:
    """Test whitespace-only strings are invalid."""
    assert validate_and_convert("   ") is None
    assert validate_and_convert("\t") is None
    assert validate_and_convert("\n") is None


def test_whitespace_stripping() -> None:
    """Test that whitespace is stripped."""
    assert validate_and_convert("  123  ") == 123
    assert validate_and_convert("\t456\n") == 456
    assert validate_and_convert("  -789  ") == -789


def test_plus_sign() -> None:
    """Test explicit positive sign."""
    assert validate_and_convert("+123") == 123
    assert validate_and_convert("  +456  ") == 456


def test_leading_zeros() -> None:
    """Test strings with leading zeros."""
    assert validate_and_convert("007") == 7
    assert validate_and_convert("000") == 0
    assert validate_and_convert("-007") == -7

"""Tests for Problem 10: Zigzag Conversion."""

from __future__ import annotations

from week01_fundamentals.solutions.day02.problem_10_zigzag_conversion import zigzag_conversion


def test_3_rows() -> None:
    """Test PAYPALISHIRING with 3 rows."""
    assert zigzag_conversion("PAYPALISHIRING", 3) == "PAHNAPLSIIGYIR"


def test_4_rows() -> None:
    """Test PAYPALISHIRING with 4 rows."""
    assert zigzag_conversion("PAYPALISHIRING", 4) == "PINALSIGYAHRPI"


def test_1_row() -> None:
    """Test with 1 row (no zigzag)."""
    assert zigzag_conversion("ABCDEF", 1) == "ABCDEF"


def test_single_character() -> None:
    """Test single character."""
    assert zigzag_conversion("A", 1) == "A"


def test_num_rows_equals_length() -> None:
    """Test when num_rows equals string length."""
    assert zigzag_conversion("ABC", 3) == "ABC"


def test_num_rows_greater_than_length() -> None:
    """Test when num_rows greater than string length."""
    assert zigzag_conversion("ABC", 5) == "ABC"


def test_2_rows() -> None:
    """Test with 2 rows."""
    assert zigzag_conversion("ABCDEF", 2) == "ACEBDF"


def test_short_string_3_rows() -> None:
    """Test short string with 3 rows."""
    assert zigzag_conversion("AB", 3) == "AB"


def test_repeating_pattern() -> None:
    """Test with repeating pattern."""
    assert zigzag_conversion("ABABABAB", 2) == "AAAABBBB"


def test_numbers() -> None:
    """Test with numbers."""
    assert zigzag_conversion("123456789", 3) == "159246837"

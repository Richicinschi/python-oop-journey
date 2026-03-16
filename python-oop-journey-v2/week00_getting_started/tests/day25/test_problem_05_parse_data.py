"""Tests for Problem 05: Parse Data."""

from __future__ import annotations

from week00_getting_started.solutions.day25.problem_05_parse_data import parse_data


def test_simple_pairs() -> None:
    """Test parsing simple key-value pairs."""
    result = parse_data("name:Alice,age:30")
    assert result == {"name": "Alice", "age": "30"}


def test_empty_string() -> None:
    """Test empty string returns empty dict."""
    assert parse_data("") == {}


def test_no_colon() -> None:
    """Test string without colon returns empty dict."""
    assert parse_data("invalid") == {}


def test_malformed_pairs() -> None:
    """Test skipping malformed pairs."""
    result = parse_data("good:pair,badpair,also:good")
    assert result == {"good": "pair", "also": "good"}


def test_single_pair() -> None:
    """Test single key-value pair."""
    assert parse_data("key:value") == {"key": "value"}


def test_empty_key() -> None:
    """Test empty key is skipped."""
    result = parse_data(":value,good:pair")
    assert result == {"good": "pair"}


def test_colon_in_value() -> None:
    """Test colon in value is preserved."""
    result = parse_data("time:10:30,date:today")
    assert result == {"time": "10:30", "date": "today"}

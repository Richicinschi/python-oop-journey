"""Tests for Problem 02: Handle KeyError."""

from __future__ import annotations

from week00_getting_started.solutions.day26.problem_02_handle_key_error import (
    safe_dict_get,
)


def test_key_exists() -> None:
    """Test getting existing key."""
    assert safe_dict_get({"name": "Alice"}, "name", "Unknown") == "Alice"


def test_key_missing() -> None:
    """Test getting missing key returns default."""
    assert safe_dict_get({"name": "Alice"}, "age", 0) == 0
    assert safe_dict_get({"a": 1}, "b", "default") == "default"


def test_not_a_dict() -> None:
    """Test non-dict input returns None."""
    assert safe_dict_get("string", "key", "default") is None
    assert safe_dict_get([1, 2, 3], 0, "default") is None
    assert safe_dict_get(None, "key", "default") is None


def test_empty_dict() -> None:
    """Test empty dictionary."""
    assert safe_dict_get({}, "key", "default") == "default"


def test_none_default() -> None:
    """Test None as default value."""
    assert safe_dict_get({}, "key", None) is None

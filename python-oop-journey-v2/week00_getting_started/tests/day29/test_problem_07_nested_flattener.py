"""Tests for Problem 07: Nested Data Flattener."""

from __future__ import annotations

from week00_getting_started.solutions.day29.problem_07_nested_flattener import (
    flatten_dict,
    flatten_list,
    flatten_mixed,
)


def test_flatten_list_simple() -> None:
    """Test flatten_list with simple nested list."""
    assert flatten_list([1, [2, 3], 4]) == [1, 2, 3, 4]


def test_flatten_list_deeply_nested() -> None:
    """Test flatten_list with deeply nested structure."""
    assert flatten_list([1, [2, [3, [4, 5]]], 6]) == [1, 2, 3, 4, 5, 6]


def test_flatten_list_empty() -> None:
    """Test flatten_list with empty list."""
    assert flatten_list([]) == []


def test_flatten_list_no_nesting() -> None:
    """Test flatten_list with no nesting."""
    assert flatten_list([1, 2, 3]) == [1, 2, 3]


def test_flatten_list_empty_inner() -> None:
    """Test flatten_list with empty inner lists."""
    assert flatten_list([1, [], 2, [], 3]) == [1, 2, 3]


def test_flatten_dict_simple() -> None:
    """Test flatten_dict with simple nested dict."""
    input_dict = {"a": 1, "b": {"c": 2}}
    assert flatten_dict(input_dict) == {"a": 1, "b.c": 2}


def test_flatten_dict_deeply_nested() -> None:
    """Test flatten_dict with deeply nested structure."""
    input_dict = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
    assert flatten_dict(input_dict) == {"a": 1, "b.c": 2, "b.d.e": 3}


def test_flatten_dict_with_prefix() -> None:
    """Test flatten_dict with prefix."""
    input_dict = {"a": 1, "b": 2}
    assert flatten_dict(input_dict, "prefix") == {"prefix.a": 1, "prefix.b": 2}


def test_flatten_dict_empty() -> None:
    """Test flatten_dict with empty dict."""
    assert flatten_dict({}) == {}


def test_flatten_dict_multiple_at_level() -> None:
    """Test flatten_dict with multiple keys at nested level."""
    input_dict = {"a": {"b": 1, "c": 2}, "d": {"e": 3, "f": 4}}
    result = flatten_dict(input_dict)
    assert result == {"a.b": 1, "a.c": 2, "d.e": 3, "d.f": 4}


def test_flatten_mixed_simple() -> None:
    """Test flatten_mixed with simple nested list."""
    assert flatten_mixed([1, [2, 3], 4]) == [1, 2, 3, 4]


def test_flatten_mixed_preserves_dicts() -> None:
    """Test flatten_mixed preserves dictionaries."""
    input_list = [1, {"a": [2, 3]}, [4, 5]]
    result = flatten_mixed(input_list)
    assert result == [1, {"a": [2, 3]}, 4, 5]


def test_flatten_mixed_preserves_strings() -> None:
    """Test flatten_mixed preserves string elements."""
    input_list = ["hello", ["world", "foo"], "bar"]
    assert flatten_mixed(input_list) == ["hello", "world", "foo", "bar"]


def test_flatten_mixed_deeply_nested() -> None:
    """Test flatten_mixed with deeply nested lists."""
    input_list = [1, [[2, 3], [4, [5, 6]]]]
    assert flatten_mixed(input_list) == [1, 2, 3, 4, 5, 6]

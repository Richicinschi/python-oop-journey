"""Tests for Problem 04: Merge Dictionaries."""

from __future__ import annotations

from week00_getting_started.solutions.day14.problem_04_merge_dictionaries import merge_dictionaries


def test_merge_no_overlap() -> None:
    """Test merging dictionaries with no overlapping keys."""
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    assert merge_dictionaries(dict1, dict2) == {"a": 1, "b": 2, "c": 3, "d": 4}


def test_merge_with_overlap() -> None:
    """Test merging with overlapping keys - dict2 values should win."""
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"b": 20, "c": 30, "d": 4}
    assert merge_dictionaries(dict1, dict2) == {"a": 1, "b": 20, "c": 30, "d": 4}


def test_merge_empty_dict1() -> None:
    """Test merging when first dict is empty."""
    dict1 = {}
    dict2 = {"a": 1, "b": 2}
    assert merge_dictionaries(dict1, dict2) == {"a": 1, "b": 2}


def test_merge_empty_dict2() -> None:
    """Test merging when second dict is empty."""
    dict1 = {"a": 1, "b": 2}
    dict2 = {}
    assert merge_dictionaries(dict1, dict2) == {"a": 1, "b": 2}


def test_merge_both_empty() -> None:
    """Test merging two empty dicts."""
    assert merge_dictionaries({}, {}) == {}

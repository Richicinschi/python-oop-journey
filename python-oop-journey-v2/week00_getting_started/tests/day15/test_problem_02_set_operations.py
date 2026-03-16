"""Tests for Problem 02: Set Operations."""

from __future__ import annotations

from week00_getting_started.solutions.day15.problem_02_set_operations import set_operations


def test_set_operations_basic() -> None:
    """Test basic set operations."""
    set1 = {1, 2, 3, 4}
    set2 = {3, 4, 5, 6}
    result = set_operations(set1, set2)
    
    assert result["union"] == {1, 2, 3, 4, 5, 6}
    assert result["intersection"] == {3, 4}
    assert result["difference"] == {1, 2}


def test_set_operations_no_overlap() -> None:
    """Test with disjoint sets."""
    set1 = {1, 2}
    set2 = {3, 4}
    result = set_operations(set1, set2)
    
    assert result["union"] == {1, 2, 3, 4}
    assert result["intersection"] == set()
    assert result["difference"] == {1, 2}


def test_set_operations_identical() -> None:
    """Test with identical sets."""
    set1 = {1, 2, 3}
    set2 = {1, 2, 3}
    result = set_operations(set1, set2)
    
    assert result["union"] == {1, 2, 3}
    assert result["intersection"] == {1, 2, 3}
    assert result["difference"] == set()


def test_set_operations_empty() -> None:
    """Test with one empty set."""
    set1 = {1, 2, 3}
    set2 = set()
    result = set_operations(set1, set2)
    
    assert result["union"] == {1, 2, 3}
    assert result["intersection"] == set()
    assert result["difference"] == {1, 2, 3}

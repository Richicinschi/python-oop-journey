"""Tests for Problem 03: Check Membership."""

from __future__ import annotations

from week00_getting_started.solutions.day15.problem_03_check_membership import check_membership


def test_membership_exists() -> None:
    """Test checking for existing item."""
    data = {"apple", "banana", "cherry"}
    assert check_membership(data, "banana") is True
    assert check_membership(data, "apple") is True


def test_membership_missing() -> None:
    """Test checking for non-existing item."""
    data = {"apple", "banana", "cherry"}
    assert check_membership(data, "date") is False
    assert check_membership(data, "grape") is False


def test_membership_empty_set() -> None:
    """Test checking in empty set."""
    assert check_membership(set(), "anything") is False


def test_membership_case_sensitive() -> None:
    """Test that membership is case sensitive."""
    data = {"Apple", "Banana"}
    assert check_membership(data, "apple") is False
    assert check_membership(data, "Apple") is True

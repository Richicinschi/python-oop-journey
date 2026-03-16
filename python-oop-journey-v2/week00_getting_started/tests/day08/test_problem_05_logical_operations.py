"""Tests for Problem 05: Logical Operations."""

from __future__ import annotations

from week00_getting_started.solutions.day08.problem_05_logical_operations import (
    logical_and,
    logical_or,
    logical_not,
    logical_xor,
)


def test_logical_and() -> None:
    """Test logical AND operation."""
    assert logical_and(True, True) is True
    assert logical_and(True, False) is False
    assert logical_and(False, True) is False
    assert logical_and(False, False) is False


def test_logical_or() -> None:
    """Test logical OR operation."""
    assert logical_or(True, True) is True
    assert logical_or(True, False) is True
    assert logical_or(False, True) is True
    assert logical_or(False, False) is False


def test_logical_not() -> None:
    """Test logical NOT operation."""
    assert logical_not(True) is False
    assert logical_not(False) is True


def test_logical_xor() -> None:
    """Test logical XOR operation."""
    assert logical_xor(True, True) is False
    assert logical_xor(True, False) is True
    assert logical_xor(False, True) is True
    assert logical_xor(False, False) is False


def test_logical_operations_combined() -> None:
    """Test combinations of logical operations."""
    # (True AND False) OR (True XOR False) = False OR True = True
    result = logical_or(logical_and(True, False), logical_xor(True, False))
    assert result is True

    # NOT(True AND False) = NOT(False) = True
    result = logical_not(logical_and(True, False))
    assert result is True

    # (True OR False) AND (False XOR False) = True AND False = False
    result = logical_and(logical_or(True, False), logical_xor(False, False))
    assert result is False

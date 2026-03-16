"""Tests for Problem 05: Fix The Error."""

from __future__ import annotations

from week00_getting_started.solutions.day24.problem_05_fix_the_error import suggest_fix


def test_fix_missing_quotes() -> None:
    """Test fixing missing quotes in print."""
    assert suggest_fix("print(Hello)") == "print('Hello')"


def test_fix_missing_colon() -> None:
    """Test fixing missing colon in if statement."""
    assert suggest_fix("if x > 5 print(x)") == "if x > 5: print(x)"


def test_identify_zero_division() -> None:
    """Test identifying ZeroDivisionError."""
    assert suggest_fix("10 / 0") == "Cannot fix - would raise ZeroDivisionError"


def test_identify_value_error() -> None:
    """Test identifying ValueError."""
    assert suggest_fix("int('abc')") == "Cannot fix - would raise ValueError"


def test_identify_index_error() -> None:
    """Test identifying IndexError."""
    assert suggest_fix("lst[5]") == "Cannot fix - would raise IndexError"


def test_identify_key_error() -> None:
    """Test identifying KeyError."""
    assert suggest_fix("d['missing']") == "Cannot fix - would raise KeyError"

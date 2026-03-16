"""Tests for Problem 06: Is Happy Number."""

from __future__ import annotations

from week01_fundamentals.solutions.day05.problem_06_is_happy_number import is_happy_number


def test_is_happy_number_true_cases() -> None:
    assert is_happy_number(1) is True
    assert is_happy_number(7) is True
    assert is_happy_number(10) is True
    assert is_happy_number(13) is True
    assert is_happy_number(19) is True
    assert is_happy_number(23) is True
    assert is_happy_number(28) is True
    assert is_happy_number(100) is True


def test_is_happy_number_false_cases() -> None:
    assert is_happy_number(2) is False
    assert is_happy_number(3) is False
    assert is_happy_number(4) is False
    assert is_happy_number(5) is False
    assert is_happy_number(6) is False
    assert is_happy_number(8) is False
    assert is_happy_number(9) is False
    assert is_happy_number(11) is False


def test_is_happy_number_edge_cases() -> None:
    assert is_happy_number(0) is False
    assert is_happy_number(-1) is False
    assert is_happy_number(-19) is False

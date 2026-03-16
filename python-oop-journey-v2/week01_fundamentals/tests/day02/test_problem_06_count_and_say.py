"""Tests for Problem 06: Count and Say."""

from __future__ import annotations

from week01_fundamentals.solutions.day02.problem_06_count_and_say import count_and_say


def test_n_equals_1() -> None:
    """Test base case n=1."""
    assert count_and_say(1) == "1"


def test_n_equals_2() -> None:
    """Test n=2."""
    assert count_and_say(2) == "11"


def test_n_equals_3() -> None:
    """Test n=3."""
    assert count_and_say(3) == "21"


def test_n_equals_4() -> None:
    """Test n=4."""
    assert count_and_say(4) == "1211"


def test_n_equals_5() -> None:
    """Test n=5."""
    assert count_and_say(5) == "111221"


def test_n_equals_6() -> None:
    """Test n=6."""
    assert count_and_say(6) == "312211"


def test_n_equals_7() -> None:
    """Test n=7."""
    assert count_and_say(7) == "13112221"


def test_n_equals_0() -> None:
    """Test n=0 (invalid input)."""
    assert count_and_say(0) == ""


def test_negative_n() -> None:
    """Test negative n (invalid input)."""
    assert count_and_say(-1) == ""

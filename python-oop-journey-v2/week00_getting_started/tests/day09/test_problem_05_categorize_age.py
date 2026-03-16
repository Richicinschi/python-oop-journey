"""Tests for Problem 05: Categorize Age."""

from __future__ import annotations

from week00_getting_started.solutions.day09.problem_05_categorize_age import categorize_age


def test_categorize_age_infant() -> None:
    """Test infant category (0-1)."""
    assert categorize_age(0) == "infant"
    assert categorize_age(1) == "infant"


def test_categorize_age_toddler() -> None:
    """Test toddler category (2-3)."""
    assert categorize_age(2) == "toddler"
    assert categorize_age(3) == "toddler"


def test_categorize_age_child() -> None:
    """Test child category (4-12)."""
    assert categorize_age(4) == "child"
    assert categorize_age(10) == "child"
    assert categorize_age(12) == "child"


def test_categorize_age_teenager() -> None:
    """Test teenager category (13-19)."""
    assert categorize_age(13) == "teenager"
    assert categorize_age(15) == "teenager"
    assert categorize_age(19) == "teenager"


def test_categorize_age_adult() -> None:
    """Test adult category (20-64)."""
    assert categorize_age(20) == "adult"
    assert categorize_age(30) == "adult"
    assert categorize_age(64) == "adult"


def test_categorize_age_senior() -> None:
    """Test senior category (65+)."""
    assert categorize_age(65) == "senior"
    assert categorize_age(70) == "senior"
    assert categorize_age(100) == "senior"

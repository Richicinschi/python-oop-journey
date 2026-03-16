"""Tests for Problem 01: Greet User."""

from __future__ import annotations

from week00_getting_started.solutions.day16.problem_01_greet_user import greet_user


def test_greet_user_with_common_name() -> None:
    """Test greeting with a common name."""
    assert greet_user("Alice") == "Hello, Alice!"
    assert greet_user("Bob") == "Hello, Bob!"


def test_greet_user_with_empty_string() -> None:
    """Test greeting with an empty string."""
    assert greet_user("") == "Hello, !"


def test_greet_user_with_long_name() -> None:
    """Test greeting with a long name."""
    long_name = "Alexanderson"
    assert greet_user(long_name) == f"Hello, {long_name}!"


def test_greet_user_with_special_characters() -> None:
    """Test greeting with names containing special characters."""
    assert greet_user("Mary-Jane") == "Hello, Mary-Jane!"
    assert greet_user("O'Connor") == "Hello, O'Connor!"

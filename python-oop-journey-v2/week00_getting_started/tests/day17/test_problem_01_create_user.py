"""Tests for Problem 01: Create User."""

from __future__ import annotations

from week00_getting_started.solutions.day17.problem_01_create_user import create_user


def test_create_user_with_all_parameters() -> None:
    """Test creating a user with all parameters provided."""
    user = create_user("Alice", 30, "New York")
    assert user == {"name": "Alice", "age": 30, "city": "New York"}


def test_create_user_with_default_city() -> None:
    """Test creating a user with default city."""
    user = create_user("Bob", 25)
    assert user == {"name": "Bob", "age": 25, "city": "Unknown"}


def test_create_user_with_keyword_arguments() -> None:
    """Test creating a user with keyword arguments."""
    user = create_user(name="Carol", age=35, city="London")
    assert user == {"name": "Carol", "age": 35, "city": "London"}


def test_create_user_mixed_arguments() -> None:
    """Test creating a user with mixed positional and keyword arguments."""
    user = create_user("Dave", 40, city="Tokyo")
    assert user == {"name": "Dave", "age": 40, "city": "Tokyo"}

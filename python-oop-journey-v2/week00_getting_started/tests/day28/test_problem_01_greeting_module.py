"""Tests for Problem 01: Greeting Module."""

from __future__ import annotations

from week00_getting_started.solutions.day28.problem_01_greeting_module import (
    goodbye,
    hello,
    welcome,
)


def test_hello_with_name() -> None:
    """Test hello function with a name."""
    assert hello("Alice") == "Hello, Alice!"
    assert hello("Bob") == "Hello, Bob!"


def test_hello_with_empty_string() -> None:
    """Test hello function with empty string."""
    assert hello("") == "Hello, !"


def test_goodbye_with_name() -> None:
    """Test goodbye function with a name."""
    assert goodbye("Alice") == "Goodbye, Alice!"
    assert goodbye("Charlie") == "Goodbye, Charlie!"


def test_goodbye_with_empty_string() -> None:
    """Test goodbye function with empty string."""
    assert goodbye("") == "Goodbye, !"


def test_welcome_with_occasion() -> None:
    """Test welcome function with name and occasion."""
    assert welcome("Alice", "party") == "Welcome to the party, Alice!"
    assert welcome("Bob", "meeting") == "Welcome to the meeting, Bob!"


def test_welcome_with_different_occasions() -> None:
    """Test welcome with various occasion types."""
    assert welcome("Guest", "conference") == "Welcome to the conference, Guest!"
    assert welcome("Student", "class") == "Welcome to the class, Student!"

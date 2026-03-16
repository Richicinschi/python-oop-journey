"""Tests for Problem 02: Celsius to Fahrenheit."""

from __future__ import annotations

from week01_fundamentals.solutions.day01.problem_02_celsius_to_fahrenheit import celsius_to_fahrenheit


def test_freezing_point() -> None:
    """Test conversion at water freezing point."""
    assert celsius_to_fahrenheit(0) == 32.0


def test_boiling_point() -> None:
    """Test conversion at water boiling point."""
    assert celsius_to_fahrenheit(100) == 212.0


def test_negative_40() -> None:
    """Test -40 where both scales are equal."""
    assert celsius_to_fahrenheit(-40) == -40.0


def test_room_temperature() -> None:
    """Test room temperature conversion."""
    result = celsius_to_fahrenheit(20)
    assert abs(result - 68.0) < 0.001  # 20°C = 68°F


def test_body_temperature() -> None:
    """Test body temperature conversion."""
    result = celsius_to_fahrenheit(37)
    assert abs(result - 98.6) < 0.001  # 37°C ≈ 98.6°F


def test_decimal_input() -> None:
    """Test with decimal Celsius values."""
    result = celsius_to_fahrenheit(25.5)
    assert abs(result - 77.9) < 0.001


def test_very_cold() -> None:
    """Test very cold temperatures."""
    result = celsius_to_fahrenheit(-273.15)
    assert abs(result - (-459.67)) < 0.001  # Absolute zero

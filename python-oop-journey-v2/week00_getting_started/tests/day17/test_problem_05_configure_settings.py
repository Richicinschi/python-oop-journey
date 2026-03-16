"""Tests for Problem 05: Configure Settings."""

from __future__ import annotations

from week00_getting_started.solutions.day17.problem_05_configure_settings import configure_settings


def test_default_settings() -> None:
    """Test with all default values."""
    settings = configure_settings()
    assert settings == {
        "theme": "light",
        "font_size": 12,
        "show_line_numbers": True,
        "auto_save": False,
    }


def test_custom_theme() -> None:
    """Test with custom theme."""
    settings = configure_settings(theme="dark")
    assert settings["theme"] == "dark"
    assert settings["font_size"] == 12


def test_custom_font_size() -> None:
    """Test with custom font size."""
    settings = configure_settings(font_size=14)
    assert settings["font_size"] == 14
    assert settings["theme"] == "light"


def test_all_custom_settings() -> None:
    """Test with all custom settings."""
    settings = configure_settings(
        theme="dark",
        font_size=16,
        show_line_numbers=False,
        auto_save=True,
    )
    assert settings == {
        "theme": "dark",
        "font_size": 16,
        "show_line_numbers": False,
        "auto_save": True,
    }


def test_keyword_arguments() -> None:
    """Test with keyword arguments in different order."""
    settings = configure_settings(
        auto_save=True,
        theme="dark",
        show_line_numbers=False,
        font_size=10,
    )
    assert settings["auto_save"] is True
    assert settings["theme"] == "dark"
    assert settings["show_line_numbers"] is False
    assert settings["font_size"] == 10

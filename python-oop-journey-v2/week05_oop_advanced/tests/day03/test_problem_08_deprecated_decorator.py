"""Tests for Problem 08: Deprecated Decorator."""

from __future__ import annotations

import pytest
import warnings

from week05_oop_advanced.solutions.day03.problem_08_deprecated_decorator import (
    deprecated, old_function, another_old_function, calculate_legacy
)


class TestDeprecatedDecorator:
    """Tests for the deprecated decorator."""
    
    def test_deprecated_emits_warning(self) -> None:
        """Test that deprecated function emits DeprecationWarning."""
        with pytest.warns(DeprecationWarning):
            old_function()
    
    def test_deprecated_returns_result(self) -> None:
        """Test that deprecated function still returns correct result."""
        with warnings.catch_warnings():
            warnings.simplefilter("always")
            result = old_function()
        
        assert result == "I am old"
    
    def test_deprecated_custom_message(self) -> None:
        """Test that custom message is included in warning."""
        with pytest.warns(DeprecationWarning, match="Use new_function"):
            another_old_function()
    
    def test_deprecated_default_message(self) -> None:
        """Test default warning message format."""
        with pytest.warns(DeprecationWarning, match="old_function is deprecated"):
            old_function()
    
    def test_deprecated_with_args(self) -> None:
        """Test deprecated function with arguments."""
        with warnings.catch_warnings():
            warnings.simplefilter("always")
            result = calculate_legacy(5, 3)
        
        assert result == 8


class TestDeprecatedEdgeCases:
    """Tests for deprecated edge cases."""
    
    def test_deprecated_preserves_function_name(self) -> None:
        """Test that deprecated preserves function name."""
        assert old_function.__name__ == "old_function"
    
    def test_deprecated_preserves_docstring(self) -> None:
        """Test that deprecated preserves docstring."""
        assert old_function.__doc__ == "An old function that is deprecated."
    
    def test_deprecated_with_version_message(self) -> None:
        """Test deprecated with version removal message."""
        with pytest.warns(DeprecationWarning, match="v2.0"):
            calculate_legacy(1, 1)

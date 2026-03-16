"""Tests for Problem 01: Custom Range Iterator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day05.problem_01_custom_range_iterator import CustomRange


class TestCustomRangeBasic:
    """Tests for basic CustomRange functionality."""
    
    def test_custom_range_with_start_stop(self) -> None:
        result = list(CustomRange(0, 5))
        assert result == [0, 1, 2, 3, 4]
    
    def test_custom_range_with_stop_only(self) -> None:
        result = list(CustomRange(5))
        assert result == [0, 1, 2, 3, 4]
    
    def test_custom_range_with_step(self) -> None:
        result = list(CustomRange(0, 10, 2))
        assert result == [0, 2, 4, 6, 8]
    
    def test_custom_range_with_negative_step(self) -> None:
        result = list(CustomRange(10, 0, -2))
        assert result == [10, 8, 6, 4, 2]
    
    def test_custom_range_empty_when_start_equals_stop(self) -> None:
        result = list(CustomRange(5, 5))
        assert result == []
    
    def test_custom_range_empty_with_positive_step_and_start_greater_than_stop(self) -> None:
        result = list(CustomRange(10, 5))
        assert result == []
    
    def test_custom_range_empty_with_negative_step_and_start_less_than_stop(self) -> None:
        result = list(CustomRange(0, 10, -1))
        assert result == []


class TestCustomRangeEdgeCases:
    """Tests for edge cases."""
    
    def test_custom_range_zero_step_raises_error(self) -> None:
        with pytest.raises(ValueError, match="step cannot be zero"):
            CustomRange(0, 10, 0)
    
    def test_custom_range_single_element(self) -> None:
        result = list(CustomRange(5, 6))
        assert result == [5]
    
    def test_custom_range_negative_numbers(self) -> None:
        result = list(CustomRange(-5, 5))
        assert result == [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]


class TestCustomRangeReuse:
    """Tests that CustomRange can be iterated multiple times."""
    
    def test_custom_range_can_be_reused(self) -> None:
        r = CustomRange(0, 3)
        first = list(r)
        second = list(r)
        assert first == second == [0, 1, 2]
    
    def test_custom_range_multiple_iterations_independent(self) -> None:
        r = CustomRange(0, 5, 2)
        assert list(r) == [0, 2, 4]
        assert list(r) == [0, 2, 4]
        assert list(r) == [0, 2, 4]


class TestCustomRangeLen:
    """Tests for __len__ method."""
    
    def test_len_basic_range(self) -> None:
        assert len(CustomRange(0, 5)) == 5
    
    def test_len_with_step(self) -> None:
        assert len(CustomRange(0, 10, 2)) == 5
    
    def test_len_with_negative_step(self) -> None:
        assert len(CustomRange(10, 0, -2)) == 5
    
    def test_len_empty_range(self) -> None:
        assert len(CustomRange(5, 5)) == 0
    
    def test_len_uneven_step(self) -> None:
        assert len(CustomRange(0, 10, 3)) == 4  # 0, 3, 6, 9


class TestCustomRangeIteratorProtocol:
    """Tests for proper iterator protocol implementation."""
    
    def test_iter_returns_self(self) -> None:
        r = CustomRange(0, 3)
        assert iter(r) is r
    
    def test_next_returns_values(self) -> None:
        r = CustomRange(0, 3)
        assert next(r) == 0
        assert next(r) == 1
        assert next(r) == 2
    
    def test_next_raises_stop_iteration(self) -> None:
        r = CustomRange(0, 2)
        next(r)
        next(r)
        with pytest.raises(StopIteration):
            next(r)


class TestCustomRangeComparisonWithBuiltIn:
    """Tests comparing CustomRange behavior with built-in range."""
    
    def test_matches_builtin_range_basic(self) -> None:
        custom = list(CustomRange(0, 10))
        builtin = list(range(0, 10))
        assert custom == builtin
    
    def test_matches_builtin_range_with_step(self) -> None:
        custom = list(CustomRange(0, 20, 3))
        builtin = list(range(0, 20, 3))
        assert custom == builtin
    
    def test_matches_builtin_range_negative_step(self) -> None:
        custom = list(CustomRange(20, 0, -3))
        builtin = list(range(20, 0, -3))
        assert custom == builtin

"""Tests for Problem 06: Range Box."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day04.problem_06_range_box import RangeBox


class TestRangeBoxInit:
    """Test RangeBox initialization."""
    
    def test_init_basic(self) -> None:
        box = RangeBox(1, 5)
        assert box.min_val == 1
        assert box.max_val == 5
    
    def test_init_single_value(self) -> None:
        box = RangeBox(5, 5)
        assert box.min_val == 5
        assert box.max_val == 5
    
    def test_init_invalid_raises(self) -> None:
        with pytest.raises(ValueError, match="min_val"):
            RangeBox(5, 1)


class TestRangeBoxContains:
    """Test RangeBox membership testing."""
    
    def test_contains_value_in_range(self) -> None:
        box = RangeBox(1, 5)
        assert 3 in box
    
    def test_contains_at_min_boundary(self) -> None:
        box = RangeBox(1, 5)
        assert 1 in box
    
    def test_contains_at_max_boundary(self) -> None:
        box = RangeBox(1, 5)
        assert 5 in box
    
    def test_contains_value_below_range(self) -> None:
        box = RangeBox(1, 5)
        assert 0 not in box
    
    def test_contains_value_above_range(self) -> None:
        box = RangeBox(1, 5)
        assert 6 not in box
    
    def test_contains_float_value(self) -> None:
        box = RangeBox(1, 5)
        assert 2.5 in box
    
    def test_contains_float_at_boundary(self) -> None:
        box = RangeBox(1, 5)
        assert 1.0 in box
        assert 5.0 in box


class TestRangeBoxIteration:
    """Test RangeBox iteration."""
    
    def test_iteration(self) -> None:
        box = RangeBox(1, 5)
        values = list(box)
        assert values == [1, 2, 3, 4, 5]
    
    def test_iteration_single_value(self) -> None:
        box = RangeBox(5, 5)
        values = list(box)
        assert values == [5]
    
    def test_iteration_negative_values(self) -> None:
        box = RangeBox(-3, 3)
        values = list(box)
        assert values == [-3, -2, -1, 0, 1, 2, 3]


class TestRangeBoxLen:
    """Test RangeBox length."""
    
    def test_len_basic(self) -> None:
        box = RangeBox(1, 5)
        assert len(box) == 5
    
    def test_len_single_value(self) -> None:
        box = RangeBox(5, 5)
        assert len(box) == 1
    
    def test_len_large_range(self) -> None:
        box = RangeBox(0, 100)
        assert len(box) == 101


class TestRangeBoxRepr:
    """Test RangeBox representation."""
    
    def test_repr(self) -> None:
        box = RangeBox(1, 5)
        assert repr(box) == "RangeBox(1, 5)"


class TestRangeBoxIsEmpty:
    """Test RangeBox is_empty method."""
    
    def test_is_empty_false(self) -> None:
        box = RangeBox(1, 5)
        assert not box.is_empty()
    
    def test_is_empty_single_value(self) -> None:
        box = RangeBox(5, 5)
        assert not box.is_empty()


class TestRangeBoxClamp:
    """Test RangeBox clamp method."""
    
    def test_clamp_value_in_range(self) -> None:
        box = RangeBox(1, 5)
        assert box.clamp(3) == 3
    
    def test_clamp_value_below_range(self) -> None:
        box = RangeBox(1, 5)
        assert box.clamp(0) == 1
    
    def test_clamp_value_above_range(self) -> None:
        box = RangeBox(1, 5)
        assert box.clamp(10) == 5
    
    def test_clamp_at_boundaries(self) -> None:
        box = RangeBox(1, 5)
        assert box.clamp(1) == 1
        assert box.clamp(5) == 5
    
    def test_clamp_float(self) -> None:
        box = RangeBox(1, 5)
        assert box.clamp(2.5) == 2.5
        assert box.clamp(0.5) == 1
        assert box.clamp(10.5) == 5

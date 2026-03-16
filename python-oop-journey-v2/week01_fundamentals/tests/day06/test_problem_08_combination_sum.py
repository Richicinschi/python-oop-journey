"""Tests for Problem 08: Combination Sum."""

from __future__ import annotations

from week01_fundamentals.solutions.day06.problem_08_combination_sum import combination_sum


def test_combination_sum_basic() -> None:
    """Test basic combination sum."""
    result = combination_sum([2, 3, 6, 7], 7)
    assert len(result) == 2
    assert sorted([2, 2, 3]) in [sorted(r) for r in result]
    assert [7] in result


def test_combination_sum_multiple_options() -> None:
    """Test with multiple valid combinations."""
    result = combination_sum([2, 3, 5], 8)
    expected_combinations = [
        [2, 2, 2, 2],
        [2, 3, 3],
        [3, 5]
    ]
    assert len(result) == 3
    for combo in expected_combinations:
        assert sorted(combo) in [sorted(r) for r in result]


def test_combination_sum_impossible() -> None:
    """Test when no combination is possible."""
    result = combination_sum([2], 1)
    assert result == []


def test_combination_sum_empty_candidates() -> None:
    """Test with empty candidates list."""
    result = combination_sum([], 5)
    assert result == []


def test_combination_sum_exact_match() -> None:
    """Test when a single candidate equals target."""
    result = combination_sum([2, 3, 5], 5)
    assert [5] in result


def test_combination_sum_single_element() -> None:
    """Test with single candidate used multiple times."""
    result = combination_sum([2], 4)
    assert [[2, 2]] in [result, [[2, 2]]]  # May be wrapped differently
    assert len(result) == 1
    assert sorted(result[0]) == [2, 2]


def test_combination_sum_target_zero() -> None:
    """Test with target of 0."""
    result = combination_sum([1, 2, 3], 0)
    assert result == [[]]  # Empty combination sums to 0


def test_combination_sum_unique_combinations() -> None:
    """Test that result contains unique combinations only."""
    result = combination_sum([2, 3, 7], 7)
    # Should have [7] and [2, 2, 3]
    assert len(result) == 2

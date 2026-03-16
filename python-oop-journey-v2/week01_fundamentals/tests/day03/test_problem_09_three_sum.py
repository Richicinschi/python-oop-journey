"""Tests for Problem 09: Three Sum."""

from __future__ import annotations

from week01_fundamentals.solutions.day03.problem_09_three_sum import three_sum


def test_example_1() -> None:
    """Test first example from problem."""
    nums = [-1, 0, 1, 2, -1, -4]
    result = three_sum(nums)
    # Sort each triplet and the result for comparison
    result = [sorted(triplet) for triplet in result]
    result.sort()
    expected = [[-1, -1, 2], [-1, 0, 1]]
    assert result == expected


def test_example_2() -> None:
    """Test second example from problem."""
    nums = [0, 1, 1]
    assert three_sum(nums) == []


def test_example_3() -> None:
    """Test third example from problem."""
    nums = [0, 0, 0]
    assert three_sum(nums) == [[0, 0, 0]]


def test_no_solution() -> None:
    """Test with no valid triplets."""
    nums = [1, 2, 3, 4, 5]
    assert three_sum(nums) == []


def test_all_zeros() -> None:
    """Test with multiple zeros."""
    nums = [0, 0, 0, 0, 0]
    assert three_sum(nums) == [[0, 0, 0]]


def test_two_zeros() -> None:
    """Test with only two zeros."""
    nums = [0, 0, 1, -1]
    result = three_sum(nums)
    result = [sorted(triplet) for triplet in result]
    result.sort()
    assert result == [[-1, 0, 1]]


def test_negative_and_positive() -> None:
    """Test with mix of negative and positive."""
    nums = [-2, 0, 0, 2, 2]
    result = three_sum(nums)
    result = [sorted(triplet) for triplet in result]
    result.sort()
    assert result == [[-2, 0, 2]]


def test_multiple_solutions() -> None:
    """Test with multiple valid solutions."""
    nums = [-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 4]
    result = three_sum(nums)
    result = [sorted(triplet) for triplet in result]
    result.sort()
    # The valid triplets that sum to 0:
    # -4 + 0 + 4 = 0
    # -4 + 1 + 3 = 0
    # -4 + 2 + 2 = 0
    # -2 + -2 + 4 = 0
    # -2 + 0 + 2 = 0
    expected = [
        [-4, 0, 4],
        [-4, 1, 3],
        [-4, 2, 2],
        [-2, -2, 4],
        [-2, 0, 2],
    ]
    assert result == expected


def test_minimum_length() -> None:
    """Test with minimum array length (3)."""
    nums = [1, -1, 0]
    result = three_sum(nums)
    result = [sorted(triplet) for triplet in result]
    assert result == [[-1, 0, 1]]


def test_minimum_length_no_solution() -> None:
    """Test with minimum array length and no solution."""
    nums = [1, 2, 3]
    assert three_sum(nums) == []


def test_large_numbers() -> None:
    """Test with large numbers."""
    nums = [-100000, 50000, 50000]
    result = three_sum(nums)
    result = [sorted(triplet) for triplet in result]
    assert result == [[-100000, 50000, 50000]]

"""Tests for Problem 04: Zip Data."""

from __future__ import annotations

from week00_getting_started.solutions.day19.problem_04_zip_data import (
    pair_names_with_ages,
    create_dictionary_from_pairs,
    transpose_matrix,
    combine_three_lists,
)


def test_pair_names_with_ages_equal_length() -> None:
    """Test pairing names with ages of equal length."""
    names = ["Alice", "Bob", "Carol"]
    ages = [25, 30, 35]
    assert pair_names_with_ages(names, ages) == [
        ("Alice", 25),
        ("Bob", 30),
        ("Carol", 35),
    ]


def test_pair_names_with_ages_different_length() -> None:
    """Test pairing when lists have different lengths."""
    names = ["Alice", "Bob"]
    ages = [25, 30, 35]
    assert pair_names_with_ages(names, ages) == [("Alice", 25), ("Bob", 30)]


def test_create_dictionary_from_pairs() -> None:
    """Test creating dictionary from keys and values."""
    keys = ["a", "b", "c"]
    values = [1, 2, 3]
    assert create_dictionary_from_pairs(keys, values) == {"a": 1, "b": 2, "c": 3}


def test_transpose_matrix() -> None:
    """Test transposing a matrix."""
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    result = transpose_matrix(matrix)
    assert result == [(1, 4), (2, 5), (3, 6)]


def test_transpose_square_matrix() -> None:
    """Test transposing a square matrix."""
    matrix = [
        [1, 2],
        [3, 4],
    ]
    result = transpose_matrix(matrix)
    assert result == [(1, 3), (2, 4)]


def test_combine_three_lists() -> None:
    """Test combining three lists."""
    names = ["Alice", "Bob"]
    ages = [25, 30]
    cities = ["NYC", "LA"]
    result = combine_three_lists(names, ages, cities)
    assert result == [("Alice", 25, "NYC"), ("Bob", 30, "LA")]

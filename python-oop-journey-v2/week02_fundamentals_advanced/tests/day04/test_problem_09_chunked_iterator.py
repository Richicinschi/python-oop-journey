"""Tests for Problem 09: Chunked Iterator."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day04.problem_09_chunked_iterator import (
    chunked_iterator,
)


def test_exact_chunks() -> None:
    """Test when data divides evenly into chunks."""
    data = [1, 2, 3, 4, 5, 6]
    result = list(chunked_iterator(data, 2))
    assert result == [[1, 2], [3, 4], [5, 6]]


def test_partial_final_chunk() -> None:
    """Test when last chunk is partial."""
    data = [1, 2, 3, 4, 5]
    result = list(chunked_iterator(data, 2))
    assert result == [[1, 2], [3, 4], [5]]


def test_chunk_larger_than_data() -> None:
    """Test when chunk size exceeds data length."""
    data = [1, 2, 3]
    result = list(chunked_iterator(data, 5))
    assert result == [[1, 2, 3]]


def test_empty_list() -> None:
    """Test with empty list."""
    assert list(chunked_iterator([], 3)) == []


def test_single_element() -> None:
    """Test with single element."""
    assert list(chunked_iterator([42], 1)) == [[42]]


def test_chunk_size_one() -> None:
    """Test with chunk size of 1."""
    data = [1, 2, 3, 4]
    result = list(chunked_iterator(data, 1))
    assert result == [[1], [2], [3], [4]]


def test_invalid_chunk_size_zero() -> None:
    """Test that chunk size of 0 raises ValueError."""
    with pytest.raises(ValueError, match="chunk_size must be positive"):
        list(chunked_iterator([1, 2, 3], 0))


def test_invalid_chunk_size_negative() -> None:
    """Test that negative chunk size raises ValueError."""
    with pytest.raises(ValueError, match="chunk_size must be positive"):
        list(chunked_iterator([1, 2, 3], -1))


def test_preserves_order() -> None:
    """Test that order within chunks is preserved."""
    data = ["a", "b", "c", "d", "e"]
    result = list(chunked_iterator(data, 2))
    assert result == [["a", "b"], ["c", "d"], ["e"]]


def test_lazy_evaluation() -> None:
    """Test that generator yields chunks lazily."""
    data = [1, 2, 3, 4, 5, 6]
    gen = chunked_iterator(data, 2)

    # Get chunks one at a time
    assert next(gen) == [1, 2]
    assert next(gen) == [3, 4]
    assert next(gen) == [5, 6]

    try:
        next(gen)
        assert False, "Generator should be exhausted"
    except StopIteration:
        pass


def test_with_strings() -> None:
    """Test with string data."""
    data = ["a", "b", "c", "d"]
    result = list(chunked_iterator(data, 3))
    assert result == [["a", "b", "c"], ["d"]]

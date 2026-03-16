"""Tests for Problem 10: Word Search."""

from __future__ import annotations

from week01_fundamentals.solutions.day06.problem_10_word_search import exist


# Standard test board from the problem description
BOARD = [
    ['A', 'B', 'C', 'E'],
    ['S', 'F', 'C', 'S'],
    ['A', 'D', 'E', 'E']
]


def test_word_search_found_horizontal() -> None:
    """Test finding word horizontally."""
    assert exist(BOARD, "ABCCED") is True


def test_word_search_found_alternative() -> None:
    """Test finding another valid word."""
    assert exist(BOARD, "SEE") is True


def test_word_search_not_found_reuse() -> None:
    """Test that cells cannot be reused."""
    assert exist(BOARD, "ABCB") is False


def test_word_search_single_letter() -> None:
    """Test single letter word."""
    assert exist(BOARD, "A") is True
    assert exist(BOARD, "Z") is False


def test_word_search_empty_word() -> None:
    """Test empty word."""
    assert exist(BOARD, "") is False


def test_word_search_empty_board() -> None:
    """Test empty board."""
    assert exist([], "ABC") is False
    assert exist([[]], "ABC") is False


def test_word_search_word_too_long() -> None:
    """Test word longer than board."""
    assert exist(BOARD, "ABCDEFGHIJKLMNOP") is False


def test_word_search_snake_path() -> None:
    """Test word that requires turning/snaking."""
    assert exist(BOARD, "SFDFS") is False  # Would need to reuse


def test_word_search_full_word() -> None:
    """Test finding word starting with different letters."""
    assert exist(BOARD, "ASA") is True  # A(0,0) -> S(1,0) -> A(2,0)


def test_word_search_not_in_board() -> None:
    """Test word with letters not in board."""
    assert exist(BOARD, "XYZ") is False


def test_word_search_longer_path() -> None:
    """Test with a longer valid path."""
    # S(1,0) -> F(1,1) -> C(1,2) = "SFC"
    assert exist(BOARD, "SFC") is True

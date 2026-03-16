"""Tests for Problem 09: N-Queens."""

from __future__ import annotations

from week01_fundamentals.solutions.day06.problem_09_n_queens import solve_n_queens


def test_n_queens_n_equals_1() -> None:
    """Test 1-queens (single queen on 1x1 board)."""
    assert solve_n_queens(1) == 1


def test_n_queens_n_equals_2() -> None:
    """Test 2-queens (no solution)."""
    assert solve_n_queens(2) == 0


def test_n_queens_n_equals_3() -> None:
    """Test 3-queens (no solution)."""
    assert solve_n_queens(3) == 0


def test_n_queens_n_equals_4() -> None:
    """Test 4-queens (2 solutions)."""
    assert solve_n_queens(4) == 2


def test_n_queens_n_equals_5() -> None:
    """Test 5-queens."""
    assert solve_n_queens(5) == 10


def test_n_queens_n_equals_6() -> None:
    """Test 6-queens."""
    assert solve_n_queens(6) == 4


def test_n_queens_n_equals_8() -> None:
    """Test 8-queens (classic chessboard)."""
    assert solve_n_queens(8) == 92


def test_n_queens_zero() -> None:
    """Test n=0 (edge case)."""
    assert solve_n_queens(0) == 0


def test_n_queens_negative() -> None:
    """Test negative n."""
    assert solve_n_queens(-1) == 0

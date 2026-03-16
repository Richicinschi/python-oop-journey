"""Reference solution for Problem 10: Valid Sudoku."""

from __future__ import annotations


def valid_sudoku(board: list[list[str]]) -> bool:
    """Determine if Sudoku board is valid.

    Uses sets to track seen numbers in each row, column, and 3x3 box.

    Time Complexity: O(1) since board is always 9x9 = 81 cells
    Space Complexity: O(1) - fixed amount of storage

    Args:
        board: 9x9 grid where each cell is a digit ("1"-"9") or "."

    Returns:
        True if board is valid, False otherwise
    """
    # Use sets to track seen numbers in rows, columns, and boxes
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for i in range(9):
        for j in range(9):
            cell = board[i][j]

            if cell == ".":
                continue

            # Check row
            if cell in rows[i]:
                return False
            rows[i].add(cell)

            # Check column
            if cell in cols[j]:
                return False
            cols[j].add(cell)

            # Check 3x3 box (index 0-8)
            box_index = (i // 3) * 3 + (j // 3)
            if cell in boxes[box_index]:
                return False
            boxes[box_index].add(cell)

    return True

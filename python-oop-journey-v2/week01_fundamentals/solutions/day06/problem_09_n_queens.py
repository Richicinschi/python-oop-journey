"""Reference solution for Problem 09: N-Queens."""

from __future__ import annotations


def solve_n_queens(n: int) -> int:
    """Count the number of distinct n-queens solutions.
    
    Args:
        n: The size of the chessboard (n x n)
        
    Returns:
        The number of distinct valid queen placements
        
    Examples:
        >>> solve_n_queens(1)
        1
        >>> solve_n_queens(2)
        0
        >>> solve_n_queens(4)
        2
        >>> solve_n_queens(8)
        92
    """
    if n <= 0:
        return 0
    
    # Track occupied columns and diagonals
    # cols[c] = True if column c has a queen
    # diag1[d] = True if diagonal (row + col = d) has a queen
    # diag2[d] = True if diagonal (row - col = d) has a queen
    cols = [False] * n
    diag1 = [False] * (2 * n - 1)  # row + col ranges from 0 to 2n-2
    diag2 = [False] * (2 * n - 1)  # row - col ranges from -(n-1) to (n-1)
    
    def is_safe(row: int, col: int) -> bool:
        """Check if placing a queen at (row, col) is safe."""
        return not (cols[col] or diag1[row + col] or diag2[row - col + n - 1])
    
    def place_queen(row: int, col: int) -> None:
        """Mark queen placement at (row, col)."""
        cols[col] = True
        diag1[row + col] = True
        diag2[row - col + n - 1] = True
    
    def remove_queen(row: int, col: int) -> None:
        """Unmark queen placement at (row, col)."""
        cols[col] = False
        diag1[row + col] = False
        diag2[row - col + n - 1] = False
    
    def backtrack(row: int) -> int:
        """Try placing queens from row to n-1, return count of solutions."""
        # Base case: all queens placed successfully
        if row == n:
            return 1
        
        count = 0
        # Try placing queen in each column of current row
        for col in range(n):
            if is_safe(row, col):
                place_queen(row, col)
                count += backtrack(row + 1)
                remove_queen(row, col)  # Backtrack
        
        return count
    
    return backtrack(0)

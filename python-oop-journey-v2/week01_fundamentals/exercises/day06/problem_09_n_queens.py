"""Problem 09: N-Queens

Topic: Recursion, Backtracking
Difficulty: Hard

The n-queens puzzle is the problem of placing n queens on an n×n chessboard
such that no two queens attack each other.

Queens attack each other if they share:
- The same row
- The same column
- The same diagonal (both directions)

Example for n=4:
    solve_n_queens(4) returns 2 (two distinct solutions)
    
    Solution 1:          Solution 2:
    . Q . .              . . Q .
    . . . Q              Q . . .
    Q . . .              . . . Q
    . . Q .              . Q . .

Requirements:
    - Implement solve_n_queens(n) that returns the number of distinct solutions
    - Use recursion with backtracking
    - Queens must not attack each other
    - Return 0 if no solution exists (n < 4, except n=1)

Hint: Place queens one row at a time. For each row, try each column and
recursively place queens in subsequent rows if the position is safe.
"""

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
    raise NotImplementedError("Implement solve_n_queens")

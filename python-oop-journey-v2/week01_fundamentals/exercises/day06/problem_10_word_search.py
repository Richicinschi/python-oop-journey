"""Problem 10: Word Search

Topic: Recursion, Backtracking, DFS
Difficulty: Hard

Given a 2D board of characters and a word, find if the word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells,
where "adjacent" cells are horizontally or vertically neighboring.
The same letter cell may not be used more than once.

Example:
    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    
    exist(board, "ABCCED") → True (path: A→B→C→C→E→D)
    exist(board, "SEE") → True (path: S→E→E)
    exist(board, "ABCB") → False (cannot reuse 'B')

Requirements:
    - Use depth-first search (DFS) with recursion
    - Check all 4 directions (up, down, left, right)
    - Mark cells as visited during search
    - Backtrack (unmark) after exploring each path
    - Return True if word exists, False otherwise

Hint: Start from each cell that matches the first letter of the word,
then recursively search for the remaining letters.
"""

from __future__ import annotations


def exist(board: list[list[str]], word: str) -> bool:
    """Check if word exists in the 2D board.
    
    Args:
        board: 2D grid of uppercase letters
        word: The word to search for
        
    Returns:
        True if word exists in board, False otherwise
        
    Examples:
        >>> board = [
        ...     ['A', 'B', 'C', 'E'],
        ...     ['S', 'F', 'C', 'S'],
        ...     ['A', 'D', 'E', 'E']
        ... ]
        >>> exist(board, "ABCCED")
        True
        >>> exist(board, "ABCB")
        False
    """
    raise NotImplementedError("Implement exist")

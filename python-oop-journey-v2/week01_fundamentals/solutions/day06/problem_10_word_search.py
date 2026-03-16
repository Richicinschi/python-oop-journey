"""Reference solution for Problem 10: Word Search."""

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
    if not board or not board[0] or not word:
        return False
    
    rows = len(board)
    cols = len(board[0])
    
    # Track visited cells
    visited = [[False] * cols for _ in range(rows)]
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def dfs(row: int, col: int, word_index: int) -> bool:
        """Search for word starting from word_index at position (row, col).
        
        Args:
            row: Current row
            col: Current column
            word_index: Index in word we're currently matching
            
        Returns:
            True if remaining word can be matched from this position
        """
        # Base case: found the entire word
        if word_index == len(word):
            return True
        
        # Check bounds and validity
        if (row < 0 or row >= rows or 
            col < 0 or col >= cols or 
            visited[row][col] or 
            board[row][col] != word[word_index]):
            return False
        
        # Mark as visited
        visited[row][col] = True
        
        # Try all four directions
        for dr, dc in directions:
            if dfs(row + dr, col + dc, word_index + 1):
                return True
        
        # Backtrack: unmark as visited
        visited[row][col] = False
        
        return False
    
    # Try starting from each cell that matches the first letter
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == word[0]:
                if dfs(row, col, 0):
                    return True
    
    return False

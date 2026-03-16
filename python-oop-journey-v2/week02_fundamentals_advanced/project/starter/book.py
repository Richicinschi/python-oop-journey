"""Book data structure and operations.

This module handles the creation and validation of book dictionaries.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


# Valid ISBN lengths (ISBN-10 or ISBN-13)
VALID_ISBN_LENGTHS = (10, 13)


def is_valid_isbn(isbn: str) -> bool:
    """Validate ISBN format.
    
    Rules:
    - Must be a string
    - Length must be 10 or 13 characters
    - Can contain only alphanumeric characters and hyphens
    - Must contain at least one digit
    
    Args:
        isbn: The ISBN string to validate
        
    Returns:
        True if valid, False otherwise
    """
    # TODO: Implement ISBN validation
    # Hint: Check type, length, allowed characters, and presence of at least one digit
    raise NotImplementedError("Implement is_valid_isbn")


def normalize_isbn(isbn: str) -> str:
    """Normalize ISBN by removing hyphens and converting to uppercase.
    
    Args:
        isbn: Raw ISBN string
        
    Returns:
        Normalized ISBN (no hyphens, uppercase)
        
    Raises:
        ValueError: If isbn is not a string
    """
    # TODO: Implement ISBN normalization
    raise NotImplementedError("Implement normalize_isbn")


def create_book(title: str, author: str, isbn: str) -> dict[str, Any]:
    """Create a new book dictionary.
    
    The book is created with available=True and checked_out_at=None.
    The ISBN is normalized before storage.
    
    Args:
        title: Book title
        author: Book author
        isbn: Book ISBN (will be normalized)
        
    Returns:
        A dictionary representing the book with keys:
        - isbn: Normalized ISBN string
        - title: Title string
        - author: Author string
        - available: Boolean (True)
        - checked_out_at: None (timestamp when checked out)
        
    Raises:
        ValueError: If title or author is empty
        InvalidISBNError: If ISBN format is invalid
    """
    # TODO: Implement create_book
    # Hint: Validate inputs, normalize ISBN, return book dict
    raise NotImplementedError("Implement create_book")


def format_book_display(book: dict[str, Any]) -> str:
    """Format a book for display.
    
    Args:
        book: Book dictionary
        
    Returns:
        Formatted string like:
        "Effective Python" by Brett Slatkin [ISBN: 9780134685991] - Available
        or
        "Effective Python" by Brett Slatkin [ISBN: 9780134685991] - Checked Out
    """
    # TODO: Implement format_book_display
    raise NotImplementedError("Implement format_book_display")


def get_book_status(book: dict[str, Any]) -> str:
    """Get the status of a book.
    
    Args:
        book: Book dictionary
        
    Returns:
        "available" if book is available, "checked_out" otherwise
    """
    # TODO: Implement get_book_status
    raise NotImplementedError("Implement get_book_status")


def book_matches_query(book: dict[str, Any], query: str) -> bool:
    """Check if a book matches a search query.
    
    Matches if the query appears (case-insensitive) in:
    - Title
    - Author
    - ISBN
    
    Args:
        book: Book dictionary
        query: Search query string
        
    Returns:
        True if book matches query, False otherwise
    """
    # TODO: Implement book_matches_query
    # Hint: Use case-insensitive partial matching
    raise NotImplementedError("Implement book_matches_query")

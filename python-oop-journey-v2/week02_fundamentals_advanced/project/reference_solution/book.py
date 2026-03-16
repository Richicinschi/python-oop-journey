"""Book data structure and operations.

This module handles the creation and validation of book dictionaries.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from week02_fundamentals_advanced.project.reference_solution.exceptions import InvalidISBNError


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
    if not isinstance(isbn, str):
        return False
    
    # Remove hyphens for length check
    cleaned = isbn.replace("-", "")
    
    if len(cleaned) not in VALID_ISBN_LENGTHS:
        return False
    
    # Check for at least one digit and valid characters
    has_digit = False
    for char in cleaned:
        if char.isdigit():
            has_digit = True
        elif not char.isalnum():
            return False
    
    return has_digit


def normalize_isbn(isbn: str) -> str:
    """Normalize ISBN by removing hyphens and converting to uppercase.
    
    Args:
        isbn: Raw ISBN string
        
    Returns:
        Normalized ISBN (no hyphens, uppercase)
        
    Raises:
        ValueError: If isbn is not a string
    """
    if not isinstance(isbn, str):
        raise ValueError("ISBN must be a string")
    return isbn.replace("-", "").upper()


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
    if not title or not isinstance(title, str) or not title.strip():
        raise ValueError("Title must be a non-empty string")
    
    if not author or not isinstance(author, str) or not author.strip():
        raise ValueError("Author must be a non-empty string")
    
    if not is_valid_isbn(isbn):
        raise InvalidISBNError(
            isbn if isinstance(isbn, str) else str(isbn),
            "ISBN must be 10 or 13 characters with at least one digit"
        )
    
    normalized = normalize_isbn(isbn)
    
    return {
        "isbn": normalized,
        "title": title.strip(),
        "author": author.strip(),
        "available": True,
        "checked_out_at": None,
    }


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
    title = book.get("title", "Unknown Title")
    author = book.get("author", "Unknown Author")
    isbn = book.get("isbn", "Unknown ISBN")
    available = book.get("available", True)
    
    status = "Available" if available else "Checked Out"
    return f'"{title}" by {author} [ISBN: {isbn}] - {status}'


def get_book_status(book: dict[str, Any]) -> str:
    """Get the status of a book.
    
    Args:
        book: Book dictionary
        
    Returns:
        "available" if book is available, "checked_out" otherwise
    """
    return "available" if book.get("available", True) else "checked_out"


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
    if not query:
        return True
    
    query_lower = query.lower()
    
    title = book.get("title", "").lower()
    author = book.get("author", "").lower()
    isbn = book.get("isbn", "").lower()
    
    return (
        query_lower in title
        or query_lower in author
        or query_lower in isbn
    )

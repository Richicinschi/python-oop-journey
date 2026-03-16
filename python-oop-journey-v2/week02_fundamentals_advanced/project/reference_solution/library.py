"""Main library management API.

This module provides the primary interface for managing a library collection.
It orchestrates operations from book.py and storage.py.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from week02_fundamentals_advanced.project.reference_solution.book import (
    create_book,
    is_valid_isbn,
    normalize_isbn,
    book_matches_query,
    get_book_status,
)
from week02_fundamentals_advanced.project.reference_solution.exceptions import (
    BookNotFoundError,
    BookAlreadyExistsError,
    BookNotAvailableError,
    BookAlreadyAvailableError,
    InvalidISBNError,
)


def add_book(
    library: dict[str, Any],
    title: str,
    author: str,
    isbn: str
) -> dict[str, Any]:
    """Add a new book to the library.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        title: Book title
        author: Book author
        isbn: Book ISBN
        
    Returns:
        The newly created book dictionary
        
    Raises:
        InvalidISBNError: If ISBN format is invalid
        BookAlreadyExistsError: If a book with this ISBN already exists
    """
    if not is_valid_isbn(isbn):
        raise InvalidISBNError(
            isbn if isinstance(isbn, str) else str(isbn),
            "ISBN must be 10 or 13 characters with at least one digit"
        )
    
    normalized_isbn = normalize_isbn(isbn)
    
    if normalized_isbn in library:
        raise BookAlreadyExistsError(normalized_isbn)
    
    book = create_book(title, author, isbn)
    library[normalized_isbn] = book
    
    return book


def find_book(library: dict[str, Any], isbn: str) -> dict[str, Any] | None:
    """Find a book by its ISBN.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        isbn: Book ISBN to search for
        
    Returns:
        Book dictionary if found, None otherwise
    """
    if not isinstance(isbn, str):
        return None
    
    normalized_isbn = normalize_isbn(isbn)
    return library.get(normalized_isbn)


def get_book(library: dict[str, Any], isbn: str) -> dict[str, Any]:
    """Get a book by its ISBN, raising exception if not found.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        isbn: Book ISBN to search for
        
    Returns:
        Book dictionary
        
    Raises:
        BookNotFoundError: If book doesn't exist
    """
    book = find_book(library, isbn)
    if book is None:
        raise BookNotFoundError(normalize_isbn(isbn) if isinstance(isbn, str) else str(isbn))
    return book


def search_books(library: dict[str, Any], query: str) -> list[dict[str, Any]]:
    """Search books by title, author, or ISBN.
    
    Performs case-insensitive partial matching on title, author, and ISBN.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        query: Search query string
        
    Returns:
        List of matching book dictionaries (may be empty)
    """
    query = query.lower().strip() if query else ""
    
    if not query:
        return list_all_books(library)
    
    matches = [
        book for book in library.values()
        if book_matches_query(book, query)
    ]
    
    # Sort by title
    matches.sort(key=lambda b: b.get("title", "").lower())
    return matches


def list_all_books(library: dict[str, Any]) -> list[dict[str, Any]]:
    """Return all books in the library.
    
    Books are returned sorted by title.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        
    Returns:
        List of all book dictionaries, sorted by title
    """
    books = list(library.values())
    books.sort(key=lambda b: b.get("title", "").lower())
    return books


def list_available_books(library: dict[str, Any]) -> list[dict[str, Any]]:
    """Return all available (not checked out) books.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        
    Returns:
        List of available book dictionaries, sorted by title
    """
    books = [
        book for book in library.values()
        if book.get("available", True)
    ]
    books.sort(key=lambda b: b.get("title", "").lower())
    return books


def list_checked_out_books(library: dict[str, Any]) -> list[dict[str, Any]]:
    """Return all checked out books.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        
    Returns:
        List of checked out book dictionaries, sorted by title
    """
    books = [
        book for book in library.values()
        if not book.get("available", True)
    ]
    books.sort(key=lambda b: b.get("title", "").lower())
    return books


def is_book_available(library: dict[str, Any], isbn: str) -> bool:
    """Check if a book is available for checkout.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        isbn: Book ISBN to check
        
    Returns:
        True if book exists and is available, False otherwise
    """
    book = find_book(library, isbn)
    if book is None:
        return False
    return book.get("available", True)


def checkout_book(library: dict[str, Any], isbn: str) -> dict[str, Any]:
    """Checkout a book from the library.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        isbn: Book ISBN to checkout
        
    Returns:
        The updated book dictionary
        
    Raises:
        BookNotFoundError: If book doesn't exist
        BookNotAvailableError: If book is already checked out
    """
    book = get_book(library, isbn)
    
    if not book.get("available", True):
        raise BookNotAvailableError(
            book.get("isbn", isbn),
            book.get("title", "")
        )
    
    book["available"] = False
    book["checked_out_at"] = datetime.now().isoformat()
    
    return book


def return_book(library: dict[str, Any], isbn: str) -> dict[str, Any]:
    """Return a checked out book to the library.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        isbn: Book ISBN to return
        
    Returns:
        The updated book dictionary
        
    Raises:
        BookNotFoundError: If book doesn't exist
        BookAlreadyAvailableError: If book is already available
    """
    book = get_book(library, isbn)
    
    if book.get("available", True):
        raise BookAlreadyAvailableError(
            book.get("isbn", isbn),
            book.get("title", "")
        )
    
    book["available"] = True
    book["checked_out_at"] = None
    
    return book


def remove_book(library: dict[str, Any], isbn: str) -> dict[str, Any]:
    """Remove a book from the library.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        isbn: Book ISBN to remove
        
    Returns:
        The removed book dictionary
        
    Raises:
        BookNotFoundError: If book doesn't exist
    """
    normalized_isbn = normalize_isbn(isbn)
    
    if normalized_isbn not in library:
        raise BookNotFoundError(normalized_isbn)
    
    return library.pop(normalized_isbn)


def get_library_stats(library: dict[str, Any]) -> dict[str, Any]:
    """Get statistics about the library.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        
    Returns:
        Dictionary with stats:
        - total_books: Total number of books
        - available_books: Number of available books
        - checked_out_books: Number of checked out books
        - checkout_rate: Percentage of books checked out (0.0 - 1.0)
    """
    total = len(library)
    
    if total == 0:
        return {
            "total_books": 0,
            "available_books": 0,
            "checked_out_books": 0,
            "checkout_rate": 0.0,
        }
    
    checked_out = sum(
        1 for book in library.values()
        if not book.get("available", True)
    )
    available = total - checked_out
    
    return {
        "total_books": total,
        "available_books": available,
        "checked_out_books": checked_out,
        "checkout_rate": checked_out / total,
    }


def clear_library(library: dict[str, Any]) -> None:
    """Remove all books from the library.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        
    Returns:
        None
    """
    library.clear()

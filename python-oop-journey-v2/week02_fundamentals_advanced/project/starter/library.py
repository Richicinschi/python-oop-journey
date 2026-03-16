"""Main library management API.

This module provides the primary interface for managing a library collection.
It orchestrates operations from book.py and storage.py.
"""

from __future__ import annotations

from typing import Any

from week02_fundamentals_advanced.project.starter.book import (
    create_book,
    is_valid_isbn,
    normalize_isbn,
    book_matches_query,
    get_book_status,
)
from week02_fundamentals_advanced.project.starter.exceptions import (
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
    # TODO: Implement add_book
    # Steps:
    # 1. Validate the ISBN format
    # 2. Normalize the ISBN
    # 3. Check if book already exists (raise BookAlreadyExistsError if so)
    # 4. Create the book using create_book()
    # 5. Add to library dict
    # 6. Return the book
    raise NotImplementedError("Implement add_book")


def find_book(library: dict[str, Any], isbn: str) -> dict[str, Any] | None:
    """Find a book by its ISBN.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        isbn: Book ISBN to search for
        
    Returns:
        Book dictionary if found, None otherwise
    """
    # TODO: Implement find_book
    # Hint: Normalize ISBN before lookup, return None if not found
    raise NotImplementedError("Implement find_book")


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
    # TODO: Implement get_book
    # Hint: Use find_book, raise BookNotFoundError if None
    raise NotImplementedError("Implement get_book")


def search_books(library: dict[str, Any], query: str) -> list[dict[str, Any]]:
    """Search books by title, author, or ISBN.
    
    Performs case-insensitive partial matching on title, author, and ISBN.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        query: Search query string
        
    Returns:
        List of matching book dictionaries (may be empty)
    """
    # TODO: Implement search_books
    # Hint: Use book_matches_query on each book, collect matches
    raise NotImplementedError("Implement search_books")


def list_all_books(library: dict[str, Any]) -> list[dict[str, Any]]:
    """Return all books in the library.
    
    Books are returned sorted by title.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        
    Returns:
        List of all book dictionaries, sorted by title
    """
    # TODO: Implement list_all_books
    # Hint: Get all values, sort by title
    raise NotImplementedError("Implement list_all_books")


def list_available_books(library: dict[str, Any]) -> list[dict[str, Any]]:
    """Return all available (not checked out) books.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        
    Returns:
        List of available book dictionaries, sorted by title
    """
    # TODO: Implement list_available_books
    raise NotImplementedError("Implement list_available_books")


def list_checked_out_books(library: dict[str, Any]) -> list[dict[str, Any]]:
    """Return all checked out books.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        
    Returns:
        List of checked out book dictionaries, sorted by title
    """
    # TODO: Implement list_checked_out_books
    raise NotImplementedError("Implement list_checked_out_books")


def is_book_available(library: dict[str, Any], isbn: str) -> bool:
    """Check if a book is available for checkout.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        isbn: Book ISBN to check
        
    Returns:
        True if book exists and is available, False otherwise
    """
    # TODO: Implement is_book_available
    # Hint: Find book, return False if not found, check available status
    raise NotImplementedError("Implement is_book_available")


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
    # TODO: Implement checkout_book
    # Steps:
    # 1. Get the book (raises BookNotFoundError if not exists)
    # 2. Check if available (raise BookNotAvailableError if not)
    # 3. Set available = False
    # 4. Set checked_out_at to current timestamp (use datetime.now().isoformat())
    # 5. Return the book
    raise NotImplementedError("Implement checkout_book")


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
    # TODO: Implement return_book
    # Steps:
    # 1. Get the book (raises BookNotFoundError if not exists)
    # 2. Check if checked out (raise BookAlreadyAvailableError if already available)
    # 3. Set available = True
    # 4. Set checked_out_at = None
    # 5. Return the book
    raise NotImplementedError("Implement return_book")


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
    # TODO: Implement remove_book
    # Hint: Use dict.pop() with default to check existence
    raise NotImplementedError("Implement remove_book")


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
    # TODO: Implement get_library_stats
    raise NotImplementedError("Implement get_library_stats")


def clear_library(library: dict[str, Any]) -> None:
    """Remove all books from the library.
    
    Args:
        library: Dictionary mapping ISBNs to book dictionaries
        
    Returns:
        None
    """
    # TODO: Implement clear_library
    # Hint: Clear the dict in place (use .clear())
    raise NotImplementedError("Implement clear_library")

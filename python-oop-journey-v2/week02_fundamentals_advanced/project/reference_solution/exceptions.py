"""Custom exceptions for the library system.

This module defines the exception hierarchy for library-related errors.
All exceptions inherit from LibraryError for easy catching.
"""

from __future__ import annotations


class LibraryError(Exception):
    """Base exception for all library-related errors."""
    
    def __init__(self, message: str = "A library error occurred") -> None:
        self.message = message
        super().__init__(self.message)


class BookNotFoundError(LibraryError):
    """Raised when a requested book ISBN does not exist in the library."""
    
    def __init__(self, isbn: str) -> None:
        self.isbn = isbn
        message = f"Book with ISBN '{isbn}' not found in library"
        super().__init__(message)


class BookAlreadyExistsError(LibraryError):
    """Raised when trying to add a book with a duplicate ISBN."""
    
    def __init__(self, isbn: str) -> None:
        self.isbn = isbn
        message = f"Book with ISBN '{isbn}' already exists in library"
        super().__init__(message)


class BookNotAvailableError(LibraryError):
    """Raised when trying to checkout a book that is already checked out."""
    
    def __init__(self, isbn: str, title: str = "") -> None:
        self.isbn = isbn
        self.title = title
        book_desc = f"'{title}'" if title else f"ISBN '{isbn}'"
        message = f"Book {book_desc} is not available for checkout (already checked out)"
        super().__init__(message)


class BookAlreadyAvailableError(LibraryError):
    """Raised when trying to return a book that is already available."""
    
    def __init__(self, isbn: str, title: str = "") -> None:
        self.isbn = isbn
        self.title = title
        book_desc = f"'{title}'" if title else f"ISBN '{isbn}'"
        message = f"Book {book_desc} is already available (not checked out)"
        super().__init__(message)


class StorageError(LibraryError):
    """Raised when file I/O operations fail."""
    
    def __init__(self, message: str, filepath: str = "") -> None:
        self.filepath = filepath
        full_message = f"{message}"
        if filepath:
            full_message += f" (file: {filepath})"
        super().__init__(full_message)


class InvalidISBNError(LibraryError):
    """Raised when an ISBN format is invalid."""
    
    def __init__(self, isbn: str, reason: str = "") -> None:
        self.isbn = isbn
        self.reason = reason
        message = f"Invalid ISBN format: '{isbn}'"
        if reason:
            message += f" - {reason}"
        super().__init__(message)

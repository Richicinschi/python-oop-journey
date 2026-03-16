"""Custom exceptions for the library system.

This module defines the exception hierarchy for library-related errors.
All exceptions inherit from LibraryError for easy catching.
"""

from __future__ import annotations


class LibraryError(Exception):
    """Base exception for all library-related errors."""
    
    def __init__(self, message: str = "A library error occurred") -> None:
        # TODO: Store the message and call super().__init__
        raise NotImplementedError("Implement LibraryError.__init__")


class BookNotFoundError(LibraryError):
    """Raised when a requested book ISBN does not exist in the library."""
    
    def __init__(self, isbn: str) -> None:
        # TODO: Store ISBN and create a descriptive message
        raise NotImplementedError("Implement BookNotFoundError.__init__")


class BookAlreadyExistsError(LibraryError):
    """Raised when trying to add a book with a duplicate ISBN."""
    
    def __init__(self, isbn: str) -> None:
        # TODO: Store ISBN and create a descriptive message
        raise NotImplementedError("Implement BookAlreadyExistsError.__init__")


class BookNotAvailableError(LibraryError):
    """Raised when trying to checkout a book that is already checked out."""
    
    def __init__(self, isbn: str, title: str = "") -> None:
        # TODO: Store ISBN, title and create a descriptive message
        raise NotImplementedError("Implement BookNotAvailableError.__init__")


class BookAlreadyAvailableError(LibraryError):
    """Raised when trying to return a book that is already available."""
    
    def __init__(self, isbn: str, title: str = "") -> None:
        # TODO: Store ISBN, title and create a descriptive message
        raise NotImplementedError("Implement BookAlreadyAvailableError.__init__")


class StorageError(LibraryError):
    """Raised when file I/O operations fail."""
    
    def __init__(self, message: str, filepath: str = "") -> None:
        # TODO: Store message and filepath
        raise NotImplementedError("Implement StorageError.__init__")


class InvalidISBNError(LibraryError):
    """Raised when an ISBN format is invalid."""
    
    def __init__(self, isbn: str, reason: str = "") -> None:
        # TODO: Store ISBN, reason and create a descriptive message
        raise NotImplementedError("Implement InvalidISBNError.__init__")

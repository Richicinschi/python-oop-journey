"""Problem 07: Book

Topic: String representation, data modeling
Difficulty: Easy

Create a Book class with title, author, and ISBN.

Examples:
    >>> book = Book("1984", "George Orwell", "978-0451524935")
    >>> book.title
    '1984'
    >>> book.author
    'George Orwell'
    >>> book.isbn
    '978-0451524935'
    >>> str(book)
    "'1984' by George Orwell (ISBN: 978-0451524935)"
    >>> book2 = Book("Animal Farm", "George Orwell", "978-0451526342")
    >>> book == book2  # Same author comparison
    False

Requirements:
    - __init__ takes title (str), author (str), and isbn (str)
    - Store all three as instance attributes
    - is_valid_isbn() returns True if ISBN is non-empty string
    - get_short_description() returns "'Title' by Author"
    - Proper __str__ and __repr__ implementations
"""

from __future__ import annotations


class Book:
    """A class representing a book with title, author, and ISBN."""

    def __init__(self, title: str, author: str, isbn: str) -> None:
        """Initialize a book with title, author, and ISBN."""
        raise NotImplementedError("Initialize title, author, and isbn")

    def is_valid_isbn(self) -> bool:
        """Return True if ISBN is a non-empty string."""
        raise NotImplementedError("Implement is_valid_isbn method")

    def get_short_description(self) -> str:
        """Return a short description: 'Title' by Author."""
        raise NotImplementedError("Implement get_short_description method")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        raise NotImplementedError("Implement __str__ method")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        raise NotImplementedError("Implement __repr__ method")

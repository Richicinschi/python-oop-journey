"""Reference solution for Problem 07: Book."""

from __future__ import annotations


class Book:
    """A class representing a book with title, author, and ISBN."""

    def __init__(self, title: str, author: str, isbn: str) -> None:
        """Initialize a book with title, author, and ISBN.
        
        Args:
            title: The book's title
            author: The book's author
            isbn: The book's ISBN number
        """
        self.title = title
        self.author = author
        self.isbn = isbn

    def is_valid_isbn(self) -> bool:
        """Return True if ISBN is a non-empty string."""
        return isinstance(self.isbn, str) and len(self.isbn) > 0

    def get_short_description(self) -> str:
        """Return a short description: 'Title' by Author."""
        return f"'{self.title}' by {self.author}"

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn})"

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"

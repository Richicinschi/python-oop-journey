"""Book repository implementation using the Repository pattern."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from ..domain.book import Book, BookCopy
from ..domain.enums import CopyStatus


class BookRepository(ABC):
    """Abstract repository for Book and BookCopy entities.

    Following the Repository pattern, this abstracts the data access
    layer from the domain logic.
    """

    # Book operations
    @abstractmethod
    def save_book(self, book: Book) -> Book:
        """Save a book to the repository."""
        raise NotImplementedError

    @abstractmethod
    def find_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """Find a book by its ISBN."""
        raise NotImplementedError

    @abstractmethod
    def find_books_by_title(self, title: str) -> list[Book]:
        """Find books matching the given title (partial match)."""
        raise NotImplementedError

    @abstractmethod
    def find_books_by_author(self, author: str) -> list[Book]:
        """Find books by author (partial match)."""
        raise NotImplementedError

    @abstractmethod
    def find_books_by_genre(self, genre: str) -> list[Book]:
        """Find books by genre."""
        raise NotImplementedError

    @abstractmethod
    def get_all_books(self) -> list[Book]:
        """Get all books in the repository."""
        raise NotImplementedError

    @abstractmethod
    def delete_book(self, isbn: str) -> bool:
        """Delete a book from the repository."""
        raise NotImplementedError

    # BookCopy operations
    @abstractmethod
    def save_copy(self, copy: BookCopy) -> BookCopy:
        """Save a book copy to the repository."""
        raise NotImplementedError

    @abstractmethod
    def find_copy_by_barcode(self, barcode: str) -> Optional[BookCopy]:
        """Find a book copy by its barcode."""
        raise NotImplementedError

    @abstractmethod
    def find_copies_by_isbn(self, isbn: str) -> list[BookCopy]:
        """Find all copies of a specific book by ISBN."""
        raise NotImplementedError

    @abstractmethod
    def find_available_copies_by_isbn(self, isbn: str) -> list[BookCopy]:
        """Find available copies of a specific book."""
        raise NotImplementedError

    @abstractmethod
    def get_all_copies(self) -> list[BookCopy]:
        """Get all book copies in the repository."""
        raise NotImplementedError

    @abstractmethod
    def delete_copy(self, barcode: str) -> bool:
        """Delete a book copy from the repository."""
        raise NotImplementedError


class InMemoryBookRepository(BookRepository):
    """In-memory implementation of BookRepository.

    Stores books and copies in dictionaries. Suitable for testing
    and small-scale applications.
    """

    def __init__(self) -> None:
        self._books: dict[str, Book] = {}  # isbn -> Book
        self._copies: dict[str, BookCopy] = {}  # barcode -> BookCopy

    def save_book(self, book: Book) -> Book:
        """Save a book to the repository."""
        self._books[book.isbn] = book
        return book

    def find_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """Find a book by its ISBN."""
        return self._books.get(isbn)

    def find_books_by_title(self, title: str) -> list[Book]:
        """Find books matching the given title (case-insensitive partial match)."""
        title_lower = title.lower()
        return [
            book for book in self._books.values() if title_lower in book.title.lower()
        ]

    def find_books_by_author(self, author: str) -> list[Book]:
        """Find books by author (case-insensitive partial match)."""
        author_lower = author.lower()
        result = []
        for book in self._books.values():
            for book_author in book.authors:
                if author_lower in book_author.lower():
                    result.append(book)
                    break
        return result

    def find_books_by_genre(self, genre: str) -> list[Book]:
        """Find books by genre (case-insensitive)."""
        genre_lower = genre.lower()
        return [
            book for book in self._books.values() if genre_lower in book.genre.lower()
        ]

    def get_all_books(self) -> list[Book]:
        """Get all books in the repository."""
        return list(self._books.values())

    def delete_book(self, isbn: str) -> bool:
        """Delete a book from the repository."""
        book = self._books.pop(isbn, None)
        if book:
            # Also delete all copies
            for copy in book.copies:
                self._copies.pop(copy.barcode, None)
            return True
        return False

    def save_copy(self, copy: BookCopy) -> BookCopy:
        """Save a book copy to the repository."""
        self._copies[copy.barcode] = copy
        # Also add to book's copies list
        book = self._books.get(copy.book_isbn)
        if book:
            # Check if copy already in list
            if not any(c.barcode == copy.barcode for c in book.copies):
                book.copies.append(copy)
        return copy

    def find_copy_by_barcode(self, barcode: str) -> Optional[BookCopy]:
        """Find a book copy by its barcode."""
        return self._copies.get(barcode)

    def find_copies_by_isbn(self, isbn: str) -> list[BookCopy]:
        """Find all copies of a specific book by ISBN."""
        book = self._books.get(isbn)
        if book:
            return book.copies.copy()
        return []

    def find_available_copies_by_isbn(self, isbn: str) -> list[BookCopy]:
        """Find available copies of a specific book."""
        book = self._books.get(isbn)
        if book:
            return [copy for copy in book.copies if copy.status == CopyStatus.AVAILABLE]
        return []

    def get_all_copies(self) -> list[BookCopy]:
        """Get all book copies in the repository."""
        return list(self._copies.values())

    def delete_copy(self, barcode: str) -> bool:
        """Delete a book copy from the repository."""
        copy = self._copies.pop(barcode, None)
        if copy:
            # Also remove from book's copies list
            book = self._books.get(copy.book_isbn)
            if book:
                book.copies = [c for c in book.copies if c.barcode != barcode]
            return True
        return False

    def clear(self) -> None:
        """Clear all data (useful for testing)."""
        self._books.clear()
        self._copies.clear()

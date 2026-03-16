"""Tests for Problem 07: Book."""

from __future__ import annotations

from week03_oop_basics.solutions.day01.problem_07_book import Book


def test_book_creation() -> None:
    """Test creating a book."""
    book = Book("1984", "George Orwell", "978-0451524935")
    assert book.title == "1984"
    assert book.author == "George Orwell"
    assert book.isbn == "978-0451524935"


def test_book_valid_isbn() -> None:
    """Test valid ISBN check."""
    book = Book("1984", "George Orwell", "978-0451524935")
    assert book.is_valid_isbn() is True


def test_book_invalid_isbn_empty() -> None:
    """Test invalid ISBN with empty string."""
    book = Book("Test", "Author", "")
    assert book.is_valid_isbn() is False


def test_book_short_description() -> None:
    """Test getting short description."""
    book = Book("1984", "George Orwell", "978-0451524935")
    desc = book.get_short_description()
    assert "1984" in desc
    assert "George Orwell" in desc


def test_str_representation() -> None:
    """Test the __str__ method."""
    book = Book("1984", "George Orwell", "978-0451524935")
    result = str(book)
    assert "1984" in result
    assert "George Orwell" in result
    assert "978-0451524935" in result


def test_repr_representation() -> None:
    """Test the __repr__ method."""
    book = Book("1984", "George Orwell", "978-0451524935")
    result = repr(book)
    assert "Book" in result
    assert "1984" in result
    assert "George Orwell" in result


def test_book_attributes_accessible() -> None:
    """Test that attributes are directly accessible."""
    book = Book("Title", "Author", "ISBN")
    assert hasattr(book, "title")
    assert hasattr(book, "author")
    assert hasattr(book, "isbn")

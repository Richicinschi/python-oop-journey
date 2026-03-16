"""Tests for Problem 03: Library Collection."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day05.problem_03_library_collection import (
    Book,
    Patron,
    Library,
)


class TestBook:
    """Tests for Book class."""
    
    def test_book_init(self) -> None:
        """Test book initialization."""
        book = Book("Python Guide", "John Doe", "123-456")
        assert book.title == "Python Guide"
        assert book.author == "John Doe"
        assert book.isbn == "123-456"
        assert book.is_checked_out is False
    
    def test_book_check_out(self) -> None:
        """Test checking out a book."""
        book = Book("Python Guide", "John Doe", "123-456")
        assert book.check_out() is True
        assert book.is_checked_out is True
    
    def test_book_check_out_already_checked(self) -> None:
        """Test checking out an already checked out book."""
        book = Book("Python Guide", "John Doe", "123-456")
        book.check_out()
        assert book.check_out() is False
    
    def test_book_return(self) -> None:
        """Test returning a book."""
        book = Book("Python Guide", "John Doe", "123-456")
        book.check_out()
        assert book.return_book() is True
        assert book.is_checked_out is False
    
    def test_book_return_not_checked_out(self) -> None:
        """Test returning a book that wasn't checked out."""
        book = Book("Python Guide", "John Doe", "123-456")
        assert book.return_book() is False


class TestPatron:
    """Tests for Patron class."""
    
    def test_patron_init(self) -> None:
        """Test patron initialization."""
        patron = Patron("Alice", "CARD001")
        assert patron.name == "Alice"
        assert patron.library_card_id == "CARD001"
        assert patron.checked_out_books == []
    
    def test_patron_checkout_book(self) -> None:
        """Test patron checking out a book."""
        patron = Patron("Alice", "CARD001")
        book = Book("Python Guide", "John Doe", "123-456")
        assert patron.checkout_book(book) is True
        assert len(patron.checked_out_books) == 1
        assert book.is_checked_out is True
    
    def test_patron_checkout_unavailable_book(self) -> None:
        """Test patron checking out an unavailable book."""
        patron = Patron("Alice", "CARD001")
        book = Book("Python Guide", "John Doe", "123-456")
        book.check_out()  # Already checked out
        assert patron.checkout_book(book) is False
    
    def test_patron_return_book(self) -> None:
        """Test patron returning a book."""
        patron = Patron("Alice", "CARD001")
        book = Book("Python Guide", "John Doe", "123-456")
        patron.checkout_book(book)
        assert patron.return_book(book) is True
        assert len(patron.checked_out_books) == 0
        assert book.is_checked_out is False
    
    def test_patron_return_book_not_checked(self) -> None:
        """Test patron returning a book they don't have."""
        patron = Patron("Alice", "CARD001")
        book = Book("Python Guide", "John Doe", "123-456")
        assert patron.return_book(book) is False


class TestLibrary:
    """Tests for Library class."""
    
    def test_library_init(self) -> None:
        """Test library initialization."""
        library = Library("City Library")
        assert library.name == "City Library"
        assert library.books == {}
        assert library.patrons == {}
    
    def test_add_book(self) -> None:
        """Test adding a book."""
        library = Library("City Library")
        book = Book("Python Guide", "John Doe", "123-456")
        library.add_book(book)
        assert "123-456" in library.books
    
    def test_register_patron(self) -> None:
        """Test registering a patron."""
        library = Library("City Library")
        patron = Patron("Alice", "CARD001")
        library.register_patron(patron)
        assert "CARD001" in library.patrons
    
    def test_find_book(self) -> None:
        """Test finding a book."""
        library = Library("City Library")
        book = Book("Python Guide", "John Doe", "123-456")
        library.add_book(book)
        found = library.find_book("123-456")
        assert found is book
    
    def test_find_book_not_found(self) -> None:
        """Test finding a non-existent book."""
        library = Library("City Library")
        found = library.find_book("999-999")
        assert found is None
    
    def test_find_patron(self) -> None:
        """Test finding a patron."""
        library = Library("City Library")
        patron = Patron("Alice", "CARD001")
        library.register_patron(patron)
        found = library.find_patron("CARD001")
        assert found is patron
    
    def test_checkout_book_success(self) -> None:
        """Test successful book checkout."""
        library = Library("City Library")
        book = Book("Python Guide", "John Doe", "123-456")
        patron = Patron("Alice", "CARD001")
        library.add_book(book)
        library.register_patron(patron)
        result = library.checkout_book("CARD001", "123-456")
        assert "checked out" in result.lower()
        assert book.is_checked_out is True
    
    def test_checkout_book_patron_not_found(self) -> None:
        """Test checkout with unknown patron."""
        library = Library("City Library")
        book = Book("Python Guide", "John Doe", "123-456")
        library.add_book(book)
        result = library.checkout_book("INVALID", "123-456")
        assert "not found" in result.lower()
    
    def test_checkout_book_already_checked(self) -> None:
        """Test checkout of already checked out book."""
        library = Library("City Library")
        book = Book("Python Guide", "John Doe", "123-456")
        patron1 = Patron("Alice", "CARD001")
        patron2 = Patron("Bob", "CARD002")
        library.add_book(book)
        library.register_patron(patron1)
        library.register_patron(patron2)
        library.checkout_book("CARD001", "123-456")
        result = library.checkout_book("CARD002", "123-456")
        assert "already checked out" in result.lower()
    
    def test_return_book_success(self) -> None:
        """Test successful book return."""
        library = Library("City Library")
        book = Book("Python Guide", "John Doe", "123-456")
        patron = Patron("Alice", "CARD001")
        library.add_book(book)
        library.register_patron(patron)
        library.checkout_book("CARD001", "123-456")
        result = library.return_book("CARD001", "123-456")
        assert "returned" in result.lower()
        assert book.is_checked_out is False
    
    def test_get_available_books(self) -> None:
        """Test getting available books."""
        library = Library("City Library")
        book1 = Book("Python Guide", "John Doe", "123-456")
        book2 = Book("Java Guide", "Jane Doe", "789-012")
        patron = Patron("Alice", "CARD001")
        library.add_book(book1)
        library.add_book(book2)
        library.register_patron(patron)
        library.checkout_book("CARD001", "123-456")
        
        available = library.get_available_books()
        assert len(available) == 1
        assert available[0] is book2

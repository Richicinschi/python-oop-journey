"""Tests for Problem 06: Book and EBook."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day01.problem_06_book_and_ebook import (
    Book, EBook, PrintedBook
)


class TestBook:
    """Tests for the base Book class."""
    
    def test_book_init(self) -> None:
        book = Book("1984", "George Orwell", "978-0451524935", 1949, "Dystopian")
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.isbn == "978-0451524935"
        assert book.publication_year == 1949
        assert book.genre == "Dystopian"
    
    def test_book_get_info(self) -> None:
        book = Book("1984", "George Orwell", "978-0451524935", 1949, "Dystopian")
        info = book.get_book_info()
        assert "1984" in info
        assert "George Orwell" in info
        assert "978-0451524935" in info
        assert "1949" in info
    
    def test_book_get_format(self) -> None:
        book = Book("Test", "Test", "123", 2020, "Test")
        assert book.get_format() == "Unknown"
    
    def test_book_calculate_reading_time(self) -> None:
        book = Book("Test", "Test", "123", 2020, "Test")
        assert book.calculate_reading_time() == 0
    
    def test_book_is_available(self) -> None:
        book = Book("Test", "Test", "123", 2020, "Test")
        assert book.is_available() is True


class TestEBook:
    """Tests for the EBook class."""
    
    def test_ebook_inheritance(self) -> None:
        ebook = EBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 2.5, "EPUB")
        assert isinstance(ebook, Book)
    
    def test_ebook_init(self) -> None:
        ebook = EBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 2.5, "EPUB", True)
        assert ebook.file_size_mb == 2.5
        assert ebook.file_format == "EPUB"
        assert ebook.has_drm is True
    
    def test_ebook_init_default_drm(self) -> None:
        ebook = EBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 2.5, "EPUB")
        assert ebook.has_drm is False
    
    def test_ebook_get_format(self) -> None:
        ebook = EBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 2.5, "EPUB")
        assert ebook.get_format() == "Digital"
    
    def test_ebook_get_info_includes_digital(self) -> None:
        ebook = EBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 2.5, "EPUB", True)
        info = ebook.get_book_info()
        assert "Digital" in info
        assert "EPUB" in info
        assert "2.5 MB" in info
        assert "DRM: Yes" in info
    
    def test_ebook_calculate_reading_time(self) -> None:
        ebook = EBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 2.5, "EPUB")
        # 2.5 MB * 500 words/MB = 1250 words / 250 wpm = 5 minutes
        assert ebook.calculate_reading_time() == 5
        assert ebook.calculate_reading_time(125) == 10  # At 125 wpm
    
    def test_ebook_download(self) -> None:
        ebook = EBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 2.5, "EPUB")
        result = ebook.download()
        assert "1984" in result
        assert "2.5 MB" in result
    
    def test_ebook_remove_drm_success(self) -> None:
        ebook = EBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 2.5, "EPUB", True)
        assert ebook.has_drm is True
        result = ebook.remove_drm()
        assert result is True
        assert ebook.has_drm is False
    
    def test_ebook_remove_drm_no_drm(self) -> None:
        ebook = EBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 2.5, "EPUB", False)
        result = ebook.remove_drm()
        assert result is False


class TestPrintedBook:
    """Tests for the PrintedBook class."""
    
    def test_printedbook_inheritance(self) -> None:
        pbook = PrintedBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 328, "paperback", 300.0)
        assert isinstance(pbook, Book)
    
    def test_printedbook_init(self) -> None:
        pbook = PrintedBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 328, "paperback", 300.0)
        assert pbook.page_count == 328
        assert pbook.cover_type == "paperback"
        assert pbook.weight_grams == 300.0
        assert pbook.condition == "new"
    
    def test_printedbook_get_format(self) -> None:
        pbook = PrintedBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 328, "paperback", 300.0)
        assert pbook.get_format() == "Physical"
    
    def test_printedbook_get_info_includes_physical(self) -> None:
        pbook = PrintedBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 328, "hardcover", 450.0)
        info = pbook.get_book_info()
        assert "Physical" in info
        assert "328" in info
        assert "hardcover" in info
        assert "450.0g" in info
    
    def test_printedbook_calculate_reading_time(self) -> None:
        pbook = PrintedBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 275, "paperback", 300.0)
        # 275 pages * 275 words/page = 75625 words / 250 wpm = 302.5 minutes
        assert pbook.calculate_reading_time() == 302
    
    def test_printedbook_is_available(self) -> None:
        pbook = PrintedBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 328, "paperback", 300.0)
        assert pbook.is_available() is True
    
    def test_printedbook_checkout(self) -> None:
        pbook = PrintedBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 328, "paperback", 300.0)
        result = pbook.checkout()
        assert result is True
        assert pbook.is_available() is False
    
    def test_printedbook_checkout_already_out(self) -> None:
        pbook = PrintedBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 328, "paperback", 300.0)
        pbook.checkout()
        result = pbook.checkout()
        assert result is False
    
    def test_printedbook_return(self) -> None:
        pbook = PrintedBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 328, "paperback", 300.0)
        pbook.checkout()
        pbook.return_book()
        assert pbook.is_available() is True
    
    def test_printedbook_update_condition(self) -> None:
        pbook = PrintedBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian", 328, "paperback", 300.0)
        pbook.update_condition("good")
        assert pbook.condition == "good"


class TestPolymorphism:
    """Tests demonstrating polymorphic behavior."""
    
    def test_polymorphic_format(self) -> None:
        books: list[Book] = [
            Book("Test", "Test", "123", 2020, "Test"),
            EBook("1984", "Orwell", "123", 1949, "Dystopian", 2.5, "EPUB"),
            PrintedBook("1984", "Orwell", "123", 1949, "Dystopian", 328, "paperback", 300.0)
        ]
        
        formats = [b.get_format() for b in books]
        assert formats == ["Unknown", "Digital", "Physical"]
    
    def test_polymorphic_availability(self) -> None:
        books: list[Book] = [
            Book("Test", "Test", "123", 2020, "Test"),
            EBook("1984", "Orwell", "123", 1949, "Dystopian", 2.5, "EPUB"),
            PrintedBook("1984", "Orwell", "123", 1949, "Dystopian", 328, "paperback", 300.0)
        ]
        
        # All should be available initially
        assert all(b.is_available() for b in books)
        
        # Check out the printed book
        books[2].checkout()
        assert books[0].is_available() is True  # Base book always available
        assert books[1].is_available() is True  # EBook always available
        assert books[2].is_available() is False  # Printed book checked out

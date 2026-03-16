"""Problem 03: Library Collection.

Implement a Library class that aggregates Books and Patrons.
This demonstrates aggregation where books and patrons exist independently.

Classes to implement:
- Book: with attributes title, author, isbn, is_checked_out
- Patron: with attributes name, library_card_id, checked_out_books
- Library: aggregates Books and Patrons

Methods required:
- Book.check_out() / Book.return_book()
- Patron.checkout_book(book: Book) -> bool
- Patron.return_book(book: Book) -> bool
- Library.add_book(book: Book) - aggregates existing book
- Library.register_patron(patron: Patron) - aggregates existing patron
- Library.find_book(isbn: str) -> Book | None
- Library.checkout_book(patron_id: str, isbn: str) -> str
"""

from __future__ import annotations
from typing import Optional


class Book:
    """A book that can be checked out."""
    
    def __init__(self, title: str, author: str, isbn: str) -> None:
        # TODO: Initialize title, author, isbn, is_checked_out (False)
        pass
    
    def check_out(self) -> bool:
        # TODO: Set is_checked_out to True if not already checked out
        pass
    
    def return_book(self) -> bool:
        # TODO: Set is_checked_out to False if checked out
        pass


class Patron:
    """A library patron who can check out books."""
    
    def __init__(self, name: str, library_card_id: str) -> None:
        # TODO: Initialize name, library_card_id, checked_out_books (empty list)
        pass
    
    def checkout_book(self, book: Book) -> bool:
        # TODO: Check out book and add to checked_out_books if successful
        pass
    
    def return_book(self, book: Book) -> bool:
        # TODO: Return book and remove from checked_out_books if successful
        pass


class Library:
    """A library that aggregates books and patrons."""
    
    def __init__(self, name: str) -> None:
        # TODO: Initialize name, books dict (isbn -> Book), patrons dict (id -> Patron)
        pass
    
    def add_book(self, book: Book) -> None:
        # TODO: Add existing book to library collection
        pass
    
    def register_patron(self, patron: Patron) -> None:
        # TODO: Register existing patron
        pass
    
    def find_book(self, isbn: str) -> Optional[Book]:
        # TODO: Return book by ISBN or None
        pass
    
    def find_patron(self, patron_id: str) -> Optional[Patron]:
        # TODO: Return patron by ID or None
        pass
    
    def checkout_book(self, patron_id: str, isbn: str) -> str:
        # TODO: Find patron and book, attempt checkout, return status message
        pass
    
    def return_book(self, patron_id: str, isbn: str) -> str:
        # TODO: Find patron and book, attempt return, return status message
        pass
    
    def get_available_books(self) -> list[Book]:
        # TODO: Return list of books not checked out
        pass

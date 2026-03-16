"""Solution for Problem 03: Library Collection.

Library with Books and Patrons - demonstrates aggregation where
books and patrons exist independently of the library.
"""

from __future__ import annotations
from typing import Optional


class Book:
    """A book that can be checked out.
    
    Books exist independently and can be transferred between libraries.
    """
    
    def __init__(self, title: str, author: str, isbn: str) -> None:
        """Initialize the book.
        
        Args:
            title: Book title.
            author: Book author.
            isbn: ISBN identifier.
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_checked_out = False
    
    def check_out(self) -> bool:
        """Check out the book.
        
        Returns:
            True if checkout succeeded, False if already checked out.
        """
        if self.is_checked_out:
            return False
        self.is_checked_out = True
        return True
    
    def return_book(self) -> bool:
        """Return the book.
        
        Returns:
            True if return succeeded, False if not checked out.
        """
        if not self.is_checked_out:
            return False
        self.is_checked_out = False
        return True


class Patron:
    """A library patron who can check out books.
    
    Patrons exist independently and can be members of multiple libraries.
    """
    
    def __init__(self, name: str, library_card_id: str) -> None:
        """Initialize the patron.
        
        Args:
            name: Patron name.
            library_card_id: Library card identifier.
        """
        self.name = name
        self.library_card_id = library_card_id
        self.checked_out_books: list[Book] = []
    
    def checkout_book(self, book: Book) -> bool:
        """Check out a book.
        
        Args:
            book: Book to check out.
            
        Returns:
            True if checkout succeeded.
        """
        if book.check_out():
            self.checked_out_books.append(book)
            return True
        return False
    
    def return_book(self, book: Book) -> bool:
        """Return a book.
        
        Args:
            book: Book to return.
            
        Returns:
            True if return succeeded.
        """
        if book in self.checked_out_books and book.return_book():
            self.checked_out_books.remove(book)
            return True
        return False


class Library:
    """A library that aggregates books and patrons.
    
    The library maintains collections of books and patrons, but these
    objects exist independently and can exist after the library closes.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize the library.
        
        Args:
            name: Library name.
        """
        self.name = name
        self.books: dict[str, Book] = {}  # isbn -> Book
        self.patrons: dict[str, Patron] = {}  # card_id -> Patron
    
    def add_book(self, book: Book) -> None:
        """Add a book to the library's collection.
        
        Args:
            book: Existing book to add (aggregation).
        """
        self.books[book.isbn] = book
    
    def register_patron(self, patron: Patron) -> None:
        """Register a patron with the library.
        
        Args:
            patron: Existing patron to register (aggregation).
        """
        self.patrons[patron.library_card_id] = patron
    
    def find_book(self, isbn: str) -> Optional[Book]:
        """Find a book by ISBN.
        
        Args:
            isbn: ISBN to search for.
            
        Returns:
            Book if found, None otherwise.
        """
        return self.books.get(isbn)
    
    def find_patron(self, patron_id: str) -> Optional[Patron]:
        """Find a patron by library card ID.
        
        Args:
            patron_id: Library card ID to search for.
            
        Returns:
            Patron if found, None otherwise.
        """
        return self.patrons.get(patron_id)
    
    def checkout_book(self, patron_id: str, isbn: str) -> str:
        """Check out a book to a patron.
        
        Args:
            patron_id: Patron's library card ID.
            isbn: Book ISBN.
            
        Returns:
            Status message.
        """
        patron = self.find_patron(patron_id)
        if patron is None:
            return f"Patron {patron_id} not found"
        
        book = self.find_book(isbn)
        if book is None:
            return f"Book {isbn} not found"
        
        if patron.checkout_book(book):
            return f"'{book.title}' checked out to {patron.name}"
        return f"'{book.title}' is already checked out"
    
    def return_book(self, patron_id: str, isbn: str) -> str:
        """Process a book return.
        
        Args:
            patron_id: Patron's library card ID.
            isbn: Book ISBN.
            
        Returns:
            Status message.
        """
        patron = self.find_patron(patron_id)
        if patron is None:
            return f"Patron {patron_id} not found"
        
        book = self.find_book(isbn)
        if book is None:
            return f"Book {isbn} not found"
        
        if patron.return_book(book):
            return f"'{book.title}' returned by {patron.name}"
        return f"'{book.title}' was not checked out by {patron.name}"
    
    def get_available_books(self) -> list[Book]:
        """Get all available (not checked out) books.
        
        Returns:
            List of available books.
        """
        return [book for book in self.books.values() if not book.is_checked_out]
    
    def get_checked_out_books(self) -> list[Book]:
        """Get all checked out books.
        
        Returns:
            List of checked out books.
        """
        return [book for book in self.books.values() if book.is_checked_out]

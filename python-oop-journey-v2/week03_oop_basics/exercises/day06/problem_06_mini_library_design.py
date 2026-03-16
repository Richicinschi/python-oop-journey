"""Problem 06: Mini Library Design.

Topic: Class Design Principles
Difficulty: Medium

Design a library system with the following classes:
- Book: Book with ISBN, title, author, and genre
- Copy: Individual copy of a book with unique ID and condition
- Member: Library member with ID and contact info
- Loan: Tracks borrowed copies with due dates
- Library: Manages books, copies, members, and loans

Requirements:
- Books can have multiple copies
- Members can borrow available copies
- Due dates are calculated based on loan period
- Overdue loans can be identified
- Books can be returned
- Search books by title, author, or genre

Hints:
    - Hint 1: Library tracks: books dict {isbn: Book}, copies list [Copy], loans list [Loan]
    - Hint 2: Loan calculates due_date = loan_date + timedelta(days=loan_period_days)
    - Hint 3: is_overdue property checks: not returned AND date.today() > due_date
"""

from __future__ import annotations

from datetime import date, timedelta
from enum import Enum, auto


class Genre(Enum):
    """Book genres."""
    FICTION = auto()
    NON_FICTION = auto()
    SCIENCE = auto()
    HISTORY = auto()
    MYSTERY = auto()
    ROMANCE = auto()
    TECHNOLOGY = auto()


class BookCondition(Enum):
    """Condition of a book copy."""
    NEW = auto()
    GOOD = auto()
    FAIR = auto()
    POOR = auto()


class Member:
    """Library member.
    
    Attributes:
        member_id: Unique member identifier
        name: Member name
        email: Contact email
        phone: Contact phone
        is_active: Whether membership is active
    """
    
    def __init__(self, member_id: str, name: str, email: str, phone: str = "") -> None:
        raise NotImplementedError("Implement Member.__init__")
    
    def deactivate(self) -> None:
        """Deactivate membership."""
        raise NotImplementedError("Implement Member.deactivate")


class Book:
    """Book information.
    
    Attributes:
        isbn: International Standard Book Number
        title: Book title
        author: Book author
        genre: Book genre
        publication_year: Year published
    """
    
    def __init__(
        self,
        isbn: str,
        title: str,
        author: str,
        genre: Genre,
        publication_year: int
    ) -> None:
        raise NotImplementedError("Implement Book.__init__")
    
    def matches_search(self, query: str) -> bool:
        """Check if book matches search query.
        
        Args:
            query: Search string
            
        Returns:
            True if query in title or author (case-insensitive)
        """
        raise NotImplementedError("Implement Book.matches_search")


class Copy:
    """Physical copy of a book.
    
    Attributes:
        copy_id: Unique copy identifier
        book: Book this is a copy of
        condition: Physical condition
        is_available: Whether copy is available for loan
    """
    
    def __init__(self, copy_id: str, book: Book, condition: BookCondition = BookCondition.GOOD) -> None:
        raise NotImplementedError("Implement Copy.__init__")
    
    def mark_available(self) -> None:
        """Mark copy as available."""
        raise NotImplementedError("Implement Copy.mark_available")
    
    def mark_unavailable(self) -> None:
        """Mark copy as unavailable (loaned)."""
        raise NotImplementedError("Implement Copy.mark_unavailable")


class Loan:
    """Loan record for a borrowed book.
    
    Attributes:
        loan_id: Unique loan identifier
        copy: Copy being borrowed
        member: Member borrowing
        loan_date: Date borrowed
        due_date: Date due for return
        return_date: Actual return date (None if not returned)
    """
    
    def __init__(
        self,
        loan_id: str,
        copy: Copy,
        member: Member,
        loan_date: date,
        loan_period_days: int = 14
    ) -> None:
        raise NotImplementedError("Implement Loan.__init__")
    
    @property
    def is_returned(self) -> bool:
        """Check if book has been returned."""
        raise NotImplementedError("Implement Loan.is_returned")
    
    @property
    def is_overdue(self) -> bool:
        """Check if loan is overdue."""
        raise NotImplementedError("Implement Loan.is_overdue")
    
    def return_book(self, return_date: date | None = None) -> None:
        """Process book return.
        
        Args:
            return_date: Date returned (defaults to today)
        """
        raise NotImplementedError("Implement Loan.return_book")
    
    def days_remaining(self) -> int:
        """Days until due (negative if overdue)."""
        raise NotImplementedError("Implement Loan.days_remaining")


class Library:
    """Library managing books, copies, members, and loans.
    
    Attributes:
        name: Library name
    """
    
    def __init__(self, name: str) -> None:
        raise NotImplementedError("Implement Library.__init__")
    
    def add_book(self, book: Book) -> None:
        """Add a book to the library catalog."""
        raise NotImplementedError("Implement Library.add_book")
    
    def add_copy(self, copy: Copy) -> None:
        """Add a copy to the library."""
        raise NotImplementedError("Implement Library.add_copy")
    
    def register_member(self, member: Member) -> None:
        """Register a new member."""
        raise NotImplementedError("Implement Library.register_member")
    
    def find_book(self, isbn: str) -> Book | None:
        """Find book by ISBN."""
        raise NotImplementedError("Implement Library.find_book")
    
    def search_books(self, query: str) -> list[Book]:
        """Search books by title or author."""
        raise NotImplementedError("Implement Library.search_books")
    
    def get_available_copies(self, book: Book) -> list[Copy]:
        """Get available copies of a book."""
        raise NotImplementedError("Implement Library.get_available_copies")
    
    def loan_book(
        self,
        loan_id: str,
        copy: Copy,
        member: Member,
        loan_date: date | None = None
    ) -> Loan | None:
        """Create a loan for a copy.
        
        Args:
            loan_id: Unique loan ID
            copy: Copy to loan
            member: Member borrowing
            loan_date: Date of loan (defaults to today)
            
        Returns:
            Loan if successful, None otherwise
        """
        raise NotImplementedError("Implement Library.loan_book")
    
    def return_book(self, loan: Loan, return_date: date | None = None) -> bool:
        """Process book return.
        
        Args:
            loan: Loan to return
            return_date: Return date (defaults to today)
            
        Returns:
            True if successful
        """
        raise NotImplementedError("Implement Library.return_book")
    
    def get_member_loans(self, member: Member) -> list[Loan]:
        """Get all active loans for a member."""
        raise NotImplementedError("Implement Library.get_member_loans")
    
    def get_overdue_loans(self) -> list[Loan]:
        """Get all overdue loans."""
        raise NotImplementedError("Implement Library.get_overdue_loans")

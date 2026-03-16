"""Solution for Problem 06: Mini Library Design.

Demonstrates class design principles:
- Entity Identity: Copy has unique ID separate from Book
- Value Object: Book represents catalog information
- State Management: Loan tracks its lifecycle
- Repository Pattern: Library manages collections
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
        self._member_id = member_id
        self._name = name
        self._email = email
        self._phone = phone
        self._is_active = True
    
    @property
    def member_id(self) -> str:
        return self._member_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    def deactivate(self) -> None:
        """Deactivate membership."""
        self._is_active = False


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
        self._isbn = isbn
        self._title = title
        self._author = author
        self._genre = genre
        self._publication_year = publication_year
    
    @property
    def isbn(self) -> str:
        return self._isbn
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def author(self) -> str:
        return self._author
    
    @property
    def genre(self) -> Genre:
        return self._genre
    
    @property
    def publication_year(self) -> int:
        return self._publication_year
    
    def matches_search(self, query: str) -> bool:
        """Check if book matches search query.
        
        Args:
            query: Search string
            
        Returns:
            True if query in title or author (case-insensitive)
        """
        query_lower = query.lower()
        return query_lower in self._title.lower() or query_lower in self._author.lower()


class Copy:
    """Physical copy of a book.
    
    Attributes:
        copy_id: Unique copy identifier
        book: Book this is a copy of
        condition: Physical condition
        is_available: Whether copy is available for loan
    """
    
    def __init__(self, copy_id: str, book: Book, condition: BookCondition = BookCondition.GOOD) -> None:
        self._copy_id = copy_id
        self._book = book
        self._condition = condition
        self._is_available = True
    
    @property
    def copy_id(self) -> str:
        return self._copy_id
    
    @property
    def book(self) -> Book:
        return self._book
    
    @property
    def condition(self) -> BookCondition:
        return self._condition
    
    @property
    def is_available(self) -> bool:
        return self._is_available
    
    def mark_available(self) -> None:
        """Mark copy as available."""
        self._is_available = True
    
    def mark_unavailable(self) -> None:
        """Mark copy as unavailable (loaned)."""
        self._is_available = False


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
        self._loan_id = loan_id
        self._copy = copy
        self._member = member
        self._loan_date = loan_date
        self._due_date = loan_date + timedelta(days=loan_period_days)
        self._return_date: date | None = None
    
    @property
    def loan_id(self) -> str:
        return self._loan_id
    
    @property
    def copy(self) -> Copy:
        return self._copy
    
    @property
    def member(self) -> Member:
        return self._member
    
    @property
    def loan_date(self) -> date:
        return self._loan_date
    
    @property
    def due_date(self) -> date:
        return self._due_date
    
    @property
    def return_date(self) -> date | None:
        return self._return_date
    
    @property
    def is_returned(self) -> bool:
        """Check if book has been returned."""
        return self._return_date is not None
    
    @property
    def is_overdue(self) -> bool:
        """Check if loan is overdue."""
        if self.is_returned:
            return False
        return date.today() > self._due_date
    
    def return_book(self, return_date: date | None = None) -> None:
        """Process book return.
        
        Args:
            return_date: Date returned (defaults to today)
        """
        self._return_date = return_date or date.today()
        self._copy.mark_available()
    
    def days_remaining(self) -> int:
        """Days until due (negative if overdue)."""
        if self.is_returned:
            return 0
        return (self._due_date - date.today()).days


class Library:
    """Library managing books, copies, members, and loans.
    
    Attributes:
        name: Library name
    """
    
    def __init__(self, name: str) -> None:
        self._name = name
        self._books: dict[str, Book] = {}  # isbn -> Book
        self._copies: dict[str, Copy] = {}  # copy_id -> Copy
        self._members: dict[str, Member] = {}  # member_id -> Member
        self._loans: dict[str, Loan] = {}  # loan_id -> Loan
    
    @property
    def name(self) -> str:
        return self._name
    
    def add_book(self, book: Book) -> None:
        """Add a book to the library catalog."""
        self._books[book.isbn] = book
    
    def add_copy(self, copy: Copy) -> None:
        """Add a copy to the library."""
        self._copies[copy.copy_id] = copy
    
    def register_member(self, member: Member) -> None:
        """Register a new member."""
        self._members[member.member_id] = member
    
    def find_book(self, isbn: str) -> Book | None:
        """Find book by ISBN."""
        return self._books.get(isbn)
    
    def search_books(self, query: str) -> list[Book]:
        """Search books by title or author."""
        return [book for book in self._books.values() if book.matches_search(query)]
    
    def get_available_copies(self, book: Book) -> list[Copy]:
        """Get available copies of a book."""
        return [
            copy for copy in self._copies.values()
            if copy.book == book and copy.is_available
        ]
    
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
        if not member.is_active:
            return None
        if not copy.is_available:
            return None
        
        loan_date = loan_date or date.today()
        loan = Loan(loan_id, copy, member, loan_date)
        copy.mark_unavailable()
        self._loans[loan_id] = loan
        return loan
    
    def return_book(self, loan: Loan, return_date: date | None = None) -> bool:
        """Process book return.
        
        Args:
            loan: Loan to return
            return_date: Return date (defaults to today)
            
        Returns:
            True if successful
        """
        if loan.loan_id not in self._loans:
            return False
        if loan.is_returned:
            return False
        
        loan.return_book(return_date)
        return True
    
    def get_member_loans(self, member: Member) -> list[Loan]:
        """Get all active loans for a member."""
        return [
            loan for loan in self._loans.values()
            if loan.member == member and not loan.is_returned
        ]
    
    def get_overdue_loans(self) -> list[Loan]:
        """Get all overdue loans."""
        return [loan for loan in self._loans.values() if loan.is_overdue]

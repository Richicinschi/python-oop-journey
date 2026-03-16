"""Tests for Problem 06: Mini Library Design."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from week03_oop_basics.solutions.day06.problem_06_mini_library_design import (
    Book,
    BookCondition,
    Copy,
    Genre,
    Library,
    Loan,
    Member,
)


class TestMember:
    """Tests for Member class."""
    
    def test_member_creation(self) -> None:
        """Test member initialization."""
        member = Member("M001", "Alice Johnson", "alice@example.com", "555-0123")
        assert member.member_id == "M001"
        assert member.name == "Alice Johnson"
        assert member.email == "alice@example.com"
        assert member.phone == "555-0123"
        assert member.is_active is True
    
    def test_deactivate_member(self) -> None:
        """Test member deactivation."""
        member = Member("M001", "Alice Johnson", "alice@example.com")
        member.deactivate()
        assert member.is_active is False


class TestBook:
    """Tests for Book class."""
    
    def test_book_creation(self) -> None:
        """Test book initialization."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        assert book.isbn == "978-3-16-148410-0"
        assert book.title == "Python Programming"
        assert book.author == "John Doe"
        assert book.genre == Genre.TECHNOLOGY
        assert book.publication_year == 2023
    
    def test_matches_search_title(self) -> None:
        """Test searching by title."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        assert book.matches_search("python") is True
        assert book.matches_search("PROGRAMMING") is True
    
    def test_matches_search_author(self) -> None:
        """Test searching by author."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        assert book.matches_search("john") is True
        assert book.matches_search("DOE") is True
    
    def test_matches_search_no_match(self) -> None:
        """Test search with no match."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        assert book.matches_search("java") is False


class TestCopy:
    """Tests for Copy class."""
    
    def test_copy_creation(self) -> None:
        """Test copy initialization."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book, BookCondition.GOOD)
        
        assert copy.copy_id == "C001"
        assert copy.book == book
        assert copy.condition == BookCondition.GOOD
        assert copy.is_available is True
    
    def test_copy_default_condition(self) -> None:
        """Test copy with default condition."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        assert copy.condition == BookCondition.GOOD
    
    def test_mark_unavailable(self) -> None:
        """Test marking copy as unavailable."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        
        copy.mark_unavailable()
        assert copy.is_available is False
    
    def test_mark_available(self) -> None:
        """Test marking copy as available."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        
        copy.mark_unavailable()
        copy.mark_available()
        assert copy.is_available is True


class TestLoan:
    """Tests for Loan class."""
    
    def test_loan_creation(self) -> None:
        """Test loan initialization."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        loan_date = date(2024, 1, 1)
        loan = Loan("L001", copy, member, loan_date, 14)
        
        assert loan.loan_id == "L001"
        assert loan.copy == copy
        assert loan.member == member
        assert loan.loan_date == loan_date
        assert loan.due_date == date(2024, 1, 15)
        assert loan.is_returned is False
    
    def test_is_returned(self) -> None:
        """Test returned status."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        loan = Loan("L001", copy, member, date(2024, 1, 1))
        assert loan.is_returned is False
        
        loan.return_book()
        assert loan.is_returned is True
    
    def test_is_overdue(self) -> None:
        """Test overdue detection."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        # Loan due 10 days ago
        loan_date = date.today() - timedelta(days=24)
        loan = Loan("L001", copy, member, loan_date, 14)
        
        assert loan.is_overdue is True
    
    def test_is_not_overdue(self) -> None:
        """Test non-overdue loan."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        # Loan due tomorrow
        loan_date = date.today()
        loan = Loan("L001", copy, member, loan_date, 14)
        
        assert loan.is_overdue is False
    
    def test_returned_not_overdue(self) -> None:
        """Test returned loan is never overdue."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        loan_date = date.today() - timedelta(days=24)
        loan = Loan("L001", copy, member, loan_date, 14)
        
        loan.return_book()
        assert loan.is_overdue is False
    
    def test_return_book_marks_copy_available(self) -> None:
        """Test that returning book marks copy as available."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        loan = Loan("L001", copy, member, date(2024, 1, 1))
        copy.mark_unavailable()
        
        assert copy.is_available is False
        loan.return_book()
        assert copy.is_available is True
    
    def test_days_remaining(self) -> None:
        """Test days remaining calculation."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        loan = Loan("L001", copy, member, date.today(), 14)
        assert loan.days_remaining() == 14
    
    def test_days_remaining_negative(self) -> None:
        """Test days remaining when overdue."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        loan_date = date.today() - timedelta(days=20)
        loan = Loan("L001", copy, member, loan_date, 14)
        
        assert loan.days_remaining() < 0
    
    def test_days_remaining_returned(self) -> None:
        """Test days remaining when returned."""
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        loan = Loan("L001", copy, member, date(2024, 1, 1))
        loan.return_book()
        
        assert loan.days_remaining() == 0


class TestLibrary:
    """Tests for Library class."""
    
    def test_library_creation(self) -> None:
        """Test library initialization."""
        library = Library("City Library")
        assert library.name == "City Library"
    
    def test_add_book(self) -> None:
        """Test adding book to catalog."""
        library = Library("City Library")
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        
        library.add_book(book)
        assert library.find_book("978-3-16-148410-0") == book
    
    def test_add_copy(self) -> None:
        """Test adding copy to library."""
        library = Library("City Library")
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        
        library.add_copy(copy)
        available = library.get_available_copies(book)
        assert len(available) == 1
    
    def test_register_member(self) -> None:
        """Test registering member."""
        library = Library("City Library")
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        library.register_member(member)
    
    def test_find_book_not_found(self) -> None:
        """Test finding non-existent book."""
        library = Library("City Library")
        assert library.find_book("non-existent") is None
    
    def test_search_books(self) -> None:
        """Test searching books."""
        library = Library("City Library")
        
        book1 = Book("978-1", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        book2 = Book("978-2", "Java Programming", "Jane Doe", Genre.TECHNOLOGY, 2022)
        book3 = Book("978-3", "History of Art", "Bob Smith", Genre.HISTORY, 2020)
        
        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)
        
        results = library.search_books("programming")
        assert len(results) == 2
        
        results = library.search_books("doe")
        assert len(results) == 2
    
    def test_get_available_copies(self) -> None:
        """Test getting available copies."""
        library = Library("City Library")
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        
        copy1 = Copy("C001", book)
        copy2 = Copy("C002", book)
        copy2.mark_unavailable()
        
        library.add_copy(copy1)
        library.add_copy(copy2)
        
        available = library.get_available_copies(book)
        assert len(available) == 1
        assert available[0] == copy1
    
    def test_loan_book_success(self) -> None:
        """Test successful book loan."""
        library = Library("City Library")
        
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        library.add_copy(copy)
        library.register_member(member)
        
        loan = library.loan_book("L001", copy, member)
        
        assert loan is not None
        assert loan.loan_id == "L001"
        assert copy.is_available is False
    
    def test_loan_book_inactive_member(self) -> None:
        """Test loan to inactive member fails."""
        library = Library("City Library")
        
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        member.deactivate()
        
        library.add_copy(copy)
        library.register_member(member)
        
        loan = library.loan_book("L001", copy, member)
        assert loan is None
    
    def test_loan_book_unavailable(self) -> None:
        """Test loan when copy unavailable fails."""
        library = Library("City Library")
        
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        copy.mark_unavailable()
        
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        library.add_copy(copy)
        library.register_member(member)
        
        loan = library.loan_book("L001", copy, member)
        assert loan is None
    
    def test_return_book(self) -> None:
        """Test book return."""
        library = Library("City Library")
        
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        library.add_copy(copy)
        library.register_member(member)
        
        loan = library.loan_book("L001", copy, member)
        assert copy.is_available is False
        
        result = library.return_book(loan)
        assert result is True
        assert copy.is_available is True
        assert loan.is_returned is True
    
    def test_return_book_already_returned(self) -> None:
        """Test returning already returned book fails."""
        library = Library("City Library")
        
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        library.add_copy(copy)
        library.register_member(member)
        
        loan = library.loan_book("L001", copy, member)
        library.return_book(loan)
        
        # Second return should fail
        result = library.return_book(loan)
        assert result is False
    
    def test_get_member_loans(self) -> None:
        """Test getting member's active loans."""
        library = Library("City Library")
        
        book1 = Book("978-1", "Book One", "Author", Genre.FICTION, 2020)
        book2 = Book("978-2", "Book Two", "Author", Genre.FICTION, 2021)
        copy1 = Copy("C001", book1)
        copy2 = Copy("C002", book2)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        library.add_copy(copy1)
        library.add_copy(copy2)
        library.register_member(member)
        
        loan1 = library.loan_book("L001", copy1, member)
        loan2 = library.loan_book("L002", copy2, member)
        library.return_book(loan1)  # Return first loan
        
        active_loans = library.get_member_loans(member)
        assert len(active_loans) == 1
        assert active_loans[0] == loan2
    
    def test_get_overdue_loans(self) -> None:
        """Test getting overdue loans."""
        library = Library("City Library")
        
        book = Book("978-3-16-148410-0", "Python Programming", "John Doe", Genre.TECHNOLOGY, 2023)
        copy = Copy("C001", book)
        member = Member("M001", "Alice Johnson", "alice@example.com")
        
        library.add_copy(copy)
        library.register_member(member)
        
        # Create overdue loan
        loan_date = date.today() - timedelta(days=30)
        loan = library.loan_book("L001", copy, member, loan_date)
        
        overdue = library.get_overdue_loans()
        assert len(overdue) == 1
        assert overdue[0] == loan

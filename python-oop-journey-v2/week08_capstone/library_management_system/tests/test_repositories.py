"""Tests for repository implementations."""

from __future__ import annotations

from datetime import date

import pytest

from ..domain.book import Book, BookCopy
from ..domain.member import Member
from ..domain.loan import Loan
from ..domain.enums import CopyStatus, MembershipStatus, LoanStatus
from ..repositories.book_repository import (
    InMemoryBookRepository,
)
from ..repositories.member_repository import (
    InMemoryMemberRepository,
)
from ..repositories.loan_repository import (
    InMemoryLoanRepository,
)


class TestBookRepository:
    """Tests for BookRepository."""

    @pytest.fixture
    def repo(self) -> InMemoryBookRepository:
        """Create a fresh repository for each test."""
        return InMemoryBookRepository()

    @pytest.fixture
    def sample_book(self) -> Book:
        """Create a sample book."""
        return Book(
            isbn="978-0-13-110362-7",
            title="The C Programming Language",
            authors=("Brian Kernighan", "Dennis Ritchie"),
            publisher="Prentice Hall",
            publication_year=1988,
            genre="Programming",
        )

    def test_save_and_find_book_by_isbn(self, repo: InMemoryBookRepository, sample_book: Book) -> None:
        """Test saving a book and retrieving it by ISBN."""
        saved = repo.save_book(sample_book)
        assert saved.isbn == sample_book.isbn

        found = repo.find_book_by_isbn(saved.isbn)
        assert found is not None
        assert found.isbn == sample_book.isbn
        assert found.title == sample_book.title

    def test_find_book_by_isbn_not_found(self, repo: InMemoryBookRepository) -> None:
        """Test finding a non-existent ISBN."""
        found = repo.find_book_by_isbn("000-0-00-000000-0")
        assert found is None

    def test_find_books_by_title(self, repo: InMemoryBookRepository) -> None:
        """Test searching books by title."""
        book1 = Book(
            isbn="978-0-00-111001-1",
            title="Python Programming",
            authors=("Author A",),
            publisher="Pub",
            publication_year=2020,
            genre="Tech",
        )
        book2 = Book(
            isbn="978-0-00-222002-2",
            title="Java Programming",
            authors=("Author B",),
            publisher="Pub",
            publication_year=2021,
            genre="Tech",
        )
        repo.save_book(book1)
        repo.save_book(book2)

        results = repo.find_books_by_title("Python")
        assert len(results) == 1
        assert results[0].title == "Python Programming"

        # Case insensitive search
        results = repo.find_books_by_title("programming")
        assert len(results) == 2

    def test_find_books_by_author(self, repo: InMemoryBookRepository) -> None:
        """Test searching books by author."""
        book1 = Book(
            isbn="978-0-00-111001-1",
            title="Book One",
            authors=("Alice Smith", "Bob Jones"),
            publisher="Pub",
            publication_year=2020,
            genre="Fiction",
        )
        book2 = Book(
            isbn="978-0-00-222002-2",
            title="Book Two",
            authors=("Alice Smith",),
            publisher="Pub",
            publication_year=2021,
            genre="Non-fiction",
        )
        repo.save_book(book1)
        repo.save_book(book2)

        results = repo.find_books_by_author("Alice")
        assert len(results) == 2

        results = repo.find_books_by_author("Jones")
        assert len(results) == 1

    def test_delete_book(self, repo: InMemoryBookRepository, sample_book: Book) -> None:
        """Test deleting a book."""
        repo.save_book(sample_book)

        # Add a copy
        copy = BookCopy(barcode="CP001", book_isbn=sample_book.isbn)
        repo.save_copy(copy)

        deleted = repo.delete_book(sample_book.isbn)
        assert deleted is True

        found = repo.find_book_by_isbn(sample_book.isbn)
        assert found is None

    def test_save_and_find_copy(self, repo: InMemoryBookRepository, sample_book: Book) -> None:
        """Test saving and finding a book copy."""
        repo.save_book(sample_book)
        copy = BookCopy(barcode="CP001", book_isbn=sample_book.isbn)
        saved_copy = repo.save_copy(copy)

        found = repo.find_copy_by_barcode(saved_copy.barcode)
        assert found is not None
        assert found.book_isbn == sample_book.isbn

    def test_find_copies_by_isbn(self, repo: InMemoryBookRepository, sample_book: Book) -> None:
        """Test finding all copies of a book."""
        repo.save_book(sample_book)

        copy1 = BookCopy(barcode="CP001", book_isbn=sample_book.isbn)
        copy2 = BookCopy(barcode="CP002", book_isbn=sample_book.isbn)
        sample_book.add_copy(copy1)
        sample_book.add_copy(copy2)
        repo.save_copy(copy1)
        repo.save_copy(copy2)

        copies = repo.find_copies_by_isbn(sample_book.isbn)
        assert len(copies) == 2

    def test_find_available_copies(self, repo: InMemoryBookRepository, sample_book: Book) -> None:
        """Test finding available copies."""
        repo.save_book(sample_book)

        copy1 = BookCopy(barcode="CP001", book_isbn=sample_book.isbn)
        copy2 = BookCopy(barcode="CP002", book_isbn=sample_book.isbn, status=CopyStatus.BORROWED)
        sample_book.add_copy(copy1)
        sample_book.add_copy(copy2)
        repo.save_copy(copy1)
        repo.save_copy(copy2)

        available = repo.find_available_copies_by_isbn(sample_book.isbn)
        assert len(available) == 1
        assert available[0].status == CopyStatus.AVAILABLE


class TestMemberRepository:
    """Tests for MemberRepository."""

    @pytest.fixture
    def repo(self) -> InMemoryMemberRepository:
        """Create a fresh repository."""
        return InMemoryMemberRepository()

    @pytest.fixture
    def sample_member(self) -> Member:
        """Create a sample member."""
        return Member(
            member_id="MEM001",
            name="Alice Smith",
            email="alice@example.com",
            phone="555-0101",
            address="123 Main St",
        )

    def test_save_and_find_by_id(self, repo: InMemoryMemberRepository, sample_member: Member) -> None:
        """Test saving and finding a member by ID."""
        saved = repo.save(sample_member)

        found = repo.find_by_id(saved.member_id)
        assert found is not None
        assert found.name == "Alice Smith"
        assert found.email == "alice@example.com"

    def test_find_by_email(self, repo: InMemoryMemberRepository, sample_member: Member) -> None:
        """Test finding by email."""
        repo.save(sample_member)

        found = repo.find_by_email("alice@example.com")
        assert found is not None
        assert found.name == "Alice Smith"

    def test_find_by_name(self, repo: InMemoryMemberRepository) -> None:
        """Test searching by name."""
        member1 = Member(
            member_id="MEM001",
            name="Alice Johnson",
            email="alice@example.com",
            phone="555-0101",
            address="123 Main St",
        )
        member2 = Member(
            member_id="MEM002",
            name="Bob Johnson",
            email="bob@example.com",
            phone="555-0102",
            address="456 Oak Ave",
        )
        member3 = Member(
            member_id="MEM003",
            name="Carol White",
            email="carol@example.com",
            phone="555-0103",
            address="789 Pine Rd",
        )
        repo.save(member1)
        repo.save(member2)
        repo.save(member3)

        results = repo.find_by_name("Johnson")
        assert len(results) == 2

        results = repo.find_by_name("alice")
        assert len(results) == 1

    def test_find_by_status(self, repo: InMemoryMemberRepository) -> None:
        """Test finding by status."""
        active = Member(
            member_id="MEM001",
            name="Active Member",
            email="active@example.com",
            status=MembershipStatus.ACTIVE,
        )
        suspended = Member(
            member_id="MEM002",
            name="Suspended Member",
            email="suspended@example.com",
            status=MembershipStatus.SUSPENDED,
        )
        repo.save(active)
        repo.save(suspended)

        active_members = repo.find_by_status(MembershipStatus.ACTIVE)
        assert len(active_members) == 1

        suspended_members = repo.find_by_status(MembershipStatus.SUSPENDED)
        assert len(suspended_members) == 1

    def test_delete(self, repo: InMemoryMemberRepository, sample_member: Member) -> None:
        """Test deleting a member."""
        saved = repo.save(sample_member)

        deleted = repo.delete(saved.member_id)
        assert deleted is True

        found = repo.find_by_id(saved.member_id)
        assert found is None

        # Should also not be findable by email
        assert repo.find_by_email(saved.email) is None


class TestLoanRepository:
    """Tests for LoanRepository."""

    @pytest.fixture
    def repo(self) -> InMemoryLoanRepository:
        """Create a fresh repository."""
        return InMemoryLoanRepository()

    @pytest.fixture
    def sample_loan(self) -> Loan:
        """Create a sample loan."""
        return Loan.create(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
        )

    def test_save_and_find_by_id(self, repo: InMemoryLoanRepository, sample_loan: Loan) -> None:
        """Test saving and finding a loan by ID."""
        saved = repo.save(sample_loan)

        found = repo.find_by_id(saved.loan_id)
        assert found is not None
        assert found.copy_barcode == "CP001"
        assert found.member_id == "MEM001"

    def test_find_by_member(self, repo: InMemoryLoanRepository) -> None:
        """Test finding loans by member."""
        loan1 = Loan.create(loan_id="LOAN001", copy_barcode="CP001", member_id="MEM001")
        loan2 = Loan.create(loan_id="LOAN002", copy_barcode="CP002", member_id="MEM001")
        loan3 = Loan.create(loan_id="LOAN003", copy_barcode="CP003", member_id="MEM002")

        repo.save(loan1)
        repo.save(loan2)
        repo.save(loan3)

        member_a_loans = repo.find_by_member("MEM001")
        assert len(member_a_loans) == 2

        member_b_loans = repo.find_by_member("MEM002")
        assert len(member_b_loans) == 1

    def test_find_active_by_member(self, repo: InMemoryLoanRepository) -> None:
        """Test finding active loans for a member."""
        loan1 = Loan.create(loan_id="LOAN001", copy_barcode="CP001", member_id="MEM001")
        loan2 = Loan.create(loan_id="LOAN002", copy_barcode="CP002", member_id="MEM001")
        loan2.return_book()  # Return this loan

        repo.save(loan1)
        repo.save(loan2)

        active = repo.find_active_by_member("MEM001")
        assert len(active) == 1

    def test_find_active_by_copy(self, repo: InMemoryLoanRepository) -> None:
        """Test finding active loan for a specific copy."""
        loan = Loan.create(loan_id="LOAN001", copy_barcode="CP001", member_id="MEM001")
        repo.save(loan)

        found = repo.find_active_by_copy("CP001")
        assert found is not None
        assert found.loan_id == loan.loan_id

        # No active loan for different copy
        not_found = repo.find_active_by_copy("CP002")
        assert not_found is None

    def test_find_by_status(self, repo: InMemoryLoanRepository) -> None:
        """Test finding loans by status."""
        loan1 = Loan.create(loan_id="LOAN001", copy_barcode="CP001", member_id="MEM001")
        loan2 = Loan.create(loan_id="LOAN002", copy_barcode="CP002", member_id="MEM002")
        loan2.return_book()

        repo.save(loan1)
        repo.save(loan2)

        active_loans = repo.find_by_status(LoanStatus.ACTIVE)
        assert len(active_loans) == 1

        returned_loans = repo.find_by_status(LoanStatus.RETURNED)
        assert len(returned_loans) == 1

    def test_delete(self, repo: InMemoryLoanRepository, sample_loan: Loan) -> None:
        """Test deleting a loan."""
        saved = repo.save(sample_loan)

        deleted = repo.delete(saved.loan_id)
        assert deleted is True

        found = repo.find_by_id(saved.loan_id)
        assert found is None

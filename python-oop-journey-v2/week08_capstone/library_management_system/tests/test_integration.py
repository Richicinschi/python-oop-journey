"""Integration tests for the Library Management System.

These tests verify that all components work together correctly,
including repositories, services, and the CLI.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from ..domain.book import Book, BookCopy
from ..domain.member import Member
from ..domain.loan import Loan
from ..domain.enums import CopyStatus, MembershipStatus, LoanStatus
from ..repositories.book_repository import InMemoryBookRepository
from ..repositories.member_repository import InMemoryMemberRepository
from ..repositories.loan_repository import InMemoryLoanRepository
from ..services.catalog_service import CatalogService
from ..services.circulation_service import CirculationService
from ..services.reservation_service import ReservationService
from ..services.fine_service import FineService


class TestLibraryWorkflows:
    """End-to-end workflow integration tests."""

    @pytest.fixture
    def library(self) -> dict:
        """Create a fully configured library system."""
        book_repo = InMemoryBookRepository()
        member_repo = InMemoryMemberRepository()
        loan_repo = InMemoryLoanRepository()

        catalog = CatalogService(book_repo)
        circulation = CirculationService(book_repo, member_repo, loan_repo)
        reservations = ReservationService(book_repo, member_repo, loan_repo)
        fines = FineService(member_repo, loan_repo)

        return {
            "book_repo": book_repo,
            "member_repo": member_repo,
            "loan_repo": loan_repo,
            "catalog": catalog,
            "circulation": circulation,
            "reservations": reservations,
            "fines": fines,
        }

    @pytest.fixture
    def sample_library_data(self, library: dict) -> dict:
        """Create sample data for integration tests."""
        # Create books with copies
        book1 = Book(
            isbn="978-0-13-110362-7",
            title="The C Programming Language",
            authors=("Brian Kernighan", "Dennis Ritchie"),
            publisher="Prentice Hall",
            publication_year=1988,
            genre="Programming",
        )
        book2 = Book(
            isbn="978-0-13-468599-1",
            title="Clean Code",
            authors=("Robert C. Martin",),
            publisher="Prentice Hall",
            publication_year=2008,
            genre="Programming",
        )

        saved_book1 = library["catalog"].add_book(book1)
        saved_book2 = library["catalog"].add_book(book2)

        # Add copies
        copy1 = BookCopy(barcode="CP001", book_isbn=saved_book1.isbn)
        copy2 = BookCopy(barcode="CP002", book_isbn=saved_book1.isbn)
        copy3 = BookCopy(barcode="CP003", book_isbn=saved_book2.isbn)
        library["catalog"].add_copy(saved_book1.isbn, copy1)
        library["catalog"].add_copy(saved_book1.isbn, copy2)
        library["catalog"].add_copy(saved_book2.isbn, copy3)

        # Create members
        member1 = Member(
            member_id="MEM001",
            name="Alice Johnson",
            email="alice@example.com",
            phone="555-0101",
            address="123 Main St",
        )
        member2 = Member(
            member_id="MEM002",
            name="Bob Smith",
            email="bob@example.com",
            phone="555-0102",
            address="456 Oak Ave",
        )

        saved_member1 = library["member_repo"].save(member1)
        saved_member2 = library["member_repo"].save(member2)

        return {
            "books": [saved_book1, saved_book2],
            "copies": [copy1, copy2, copy3],
            "members": [saved_member1, saved_member2],
        }

    def test_complete_checkout_and_return_workflow(
        self, library: dict, sample_library_data: dict
    ) -> None:
        """Test a complete checkout and return workflow."""
        copy_barcode = sample_library_data["copies"][0].barcode
        member_id = sample_library_data["members"][0].member_id

        # Checkout
        success, message, loan = library["circulation"].checkout(
            copy_barcode, member_id, loan_id="LOAN001"
        )
        assert success is True
        assert loan is not None

        # Verify member has active loan
        active_loans = library["circulation"].get_active_loans(member_id)
        assert len(active_loans) == 1

        # Verify book copy is checked out
        copy = library["book_repo"].find_copy_by_barcode(copy_barcode)
        assert copy.status == CopyStatus.BORROWED

        # Return
        success, message, returned_loan = library["circulation"].return_book(copy_barcode)

        assert success is True
        assert returned_loan.status == LoanStatus.RETURNED

        # Verify copy is available again
        copy = library["book_repo"].find_copy_by_barcode(copy_barcode)
        assert copy.status == CopyStatus.AVAILABLE

        # Verify member has no active loans
        active_loans = library["circulation"].get_active_loans(member_id)
        assert len(active_loans) == 0

    def test_member_borrowing_limits(
        self, library: dict, sample_library_data: dict
    ) -> None:
        """Test that member borrowing limits are enforced."""
        member = sample_library_data["members"][0]
        copies = sample_library_data["copies"]

        # Member can borrow up to MAX_ACTIVE_LOANS (5 by default)
        # Checkout first book
        success, _, loan1 = library["circulation"].checkout(
            copies[0].barcode, member.member_id, loan_id="LOAN001"
        )
        assert success is True

        # Checkout second book
        success, _, loan2 = library["circulation"].checkout(
            copies[1].barcode, member.member_id, loan_id="LOAN002"
        )
        assert success is True

        # Verify member's active loan count
        member = library["member_repo"].find_by_id(member.member_id)
        assert member.active_loan_count == 2

    def test_catalog_search_and_availability(
        self, library: dict, sample_library_data: dict
    ) -> None:
        """Test catalog search and availability tracking."""
        # Search by title
        results = library["catalog"].search_by_title("Clean")
        assert len(results) == 1
        assert results[0].title == "Clean Code"

        # Search by author
        results = library["catalog"].search_by_author("Robert")
        assert len(results) == 1

        # Check availability
        book_isbn = sample_library_data["books"][1].isbn  # Clean Code
        assert library["catalog"].is_book_available(book_isbn) is True

        # Checkout the only copy
        copy_barcode = sample_library_data["copies"][2].barcode
        member_id = sample_library_data["members"][0].member_id
        library["circulation"].checkout(copy_barcode, member_id, loan_id="LOAN001")

        # Verify no longer available
        assert library["catalog"].is_book_available(book_isbn) is False

    def test_renewal_limit_enforcement(
        self, library: dict, sample_library_data: dict
    ) -> None:
        """Test that renewal limits are enforced."""
        copy_barcode = sample_library_data["copies"][0].barcode
        member_id = sample_library_data["members"][0].member_id

        # Checkout
        success, _, loan = library["circulation"].checkout(
            copy_barcode, member_id, loan_id="LOAN001"
        )

        # Renew twice (most policies allow 2 renewals)
        success, _ = library["circulation"].renew(loan.loan_id)
        assert success is True

        success, _ = library["circulation"].renew(loan.loan_id)
        assert success is True

        # Third renewal should fail
        success, message = library["circulation"].renew(loan.loan_id)
        assert success is False

    def test_statistics_reporting(self, library: dict, sample_library_data: dict) -> None:
        """Test that statistics are accurately reported."""
        copy_barcode1 = sample_library_data["copies"][0].barcode
        member_id = sample_library_data["members"][0].member_id

        # Checkout one book
        library["circulation"].checkout(copy_barcode1, member_id, loan_id="LOAN001")

        # Get catalog stats
        catalog_stats = library["catalog"].get_catalog_statistics()
        assert catalog_stats["total_books"] == 2
        assert catalog_stats["total_copies"] == 3

        # Get fine stats (should be zero)
        fine_stats = library["fines"].get_fine_statistics()
        assert fine_stats["members_with_fines"] == 0

        # Get reservation stats
        res_stats = library["reservations"].get_reservation_statistics()
        assert res_stats["total"] == 0


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    @pytest.fixture
    def library(self) -> dict:
        """Create a fully configured library system."""
        book_repo = InMemoryBookRepository()
        member_repo = InMemoryMemberRepository()
        loan_repo = InMemoryLoanRepository()

        return {
            "book_repo": book_repo,
            "member_repo": member_repo,
            "loan_repo": loan_repo,
            "catalog": CatalogService(book_repo),
            "circulation": CirculationService(book_repo, member_repo, loan_repo),
            "reservations": ReservationService(book_repo, member_repo, loan_repo),
            "fines": FineService(member_repo, loan_repo),
        }

    def test_checkout_nonexistent_book(self, library: dict) -> None:
        """Test checkout of non-existent book fails gracefully."""
        success, message, loan = library["circulation"].checkout(
            "nonexistent-barcode", "nonexistent-member-id"
        )
        assert success is False
        assert loan is None

    def test_checkout_nonexistent_member(self, library: dict) -> None:
        """Test checkout by non-existent member fails gracefully."""
        book = Book(
            isbn="978-0-00-111001-1",
            title="Test",
            authors=("Author",),
            publisher="Pub",
            publication_year=2020,
            genre="Fiction",
        )
        saved = library["catalog"].add_book(book)
        copy = BookCopy(barcode="CP001", book_isbn=saved.isbn)
        library["catalog"].add_copy(saved.isbn, copy)

        success, message, loan = library["circulation"].checkout(
            copy.barcode, "nonexistent-member-id"
        )
        assert success is False
        assert loan is None

    def test_return_non_loaned_book(self, library: dict) -> None:
        """Test return of book that was never loaned fails gracefully."""
        success, message, loan = library["circulation"].return_book("nonexistent-barcode")
        assert success is False
        assert loan is None

    def test_renew_nonexistent_loan(self, library: dict) -> None:
        """Test renew of non-existent loan fails gracefully."""
        success, message = library["circulation"].renew("nonexistent-loan-id")
        assert success is False

    def test_cancel_nonexistent_reservation(self, library: dict) -> None:
        """Test cancel of non-existent reservation fails gracefully."""
        success, message = library["reservations"].cancel_reservation(
            "nonexistent-reservation-id"
        )
        assert success is False

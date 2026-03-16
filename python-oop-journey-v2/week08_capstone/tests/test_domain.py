"""Tests for the domain layer.

This module contains comprehensive tests for:
- Book and BookCopy entities
- Member and Librarian entities
- Loan and Reservation entities
- Fine value objects
- Domain enumerations

All tests use in-memory storage and frozen time where applicable.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal

import pytest

from library_management_system.domain import (
    Book,
    BookCopy,
    Condition,
    CopyStatus,
    Fine,
    FineStatus,
    Librarian,
    Loan,
    LoanStatus,
    Member,
    MembershipStatus,
    Reservation,
    ReservationStatus,
    StaffRole,
)
from library_management_system.domain.book import ValidationError as BookValidationError
from library_management_system.domain.fine import (
    BusinessRuleError as FineBusinessError,
)
from library_management_system.domain.fine import (
    ValidationError as FineValidationError,
)
from library_management_system.domain.loan import (
    BusinessRuleError as LoanBusinessError,
)
from library_management_system.domain.loan import (
    ValidationError as LoanValidationError,
)
from library_management_system.domain.member import (
    BusinessRuleError as MemberBusinessError,
)
from library_management_system.domain.member import (
    ValidationError as MemberValidationError,
)


# =============================================================================
# Book and BookCopy Tests
# =============================================================================


class TestBookCopy:
    """Tests for the BookCopy entity."""

    def test_create_book_copy_with_valid_data(self) -> None:
        """Book copy can be created with valid data."""
        copy = BookCopy(
            barcode="CP001",
            book_isbn="978-0-123456-78-9",
            branch_id="MAIN",
        )
        assert copy.barcode == "CP001"
        assert copy.book_isbn == "978-0-123456-78-9"
        assert copy.branch_id == "MAIN"
        assert copy.status == CopyStatus.AVAILABLE
        assert copy.condition == Condition.GOOD

    def test_book_copy_default_status_is_available(self) -> None:
        """Default status for new copy is AVAILABLE."""
        copy = BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9")
        assert copy.status == CopyStatus.AVAILABLE

    def test_book_copy_is_available_check(self) -> None:
        """is_available returns True only when status is AVAILABLE."""
        copy = BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9")
        assert copy.is_available() is True

        copy.status = CopyStatus.BORROWED
        assert copy.is_available() is False

    def test_valid_status_transitions(self) -> None:
        """Valid status transitions are allowed."""
        copy = BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9")

        # AVAILABLE -> BORROWED
        assert copy.can_transition_to(CopyStatus.BORROWED) is True
        # AVAILABLE -> RESERVED
        assert copy.can_transition_to(CopyStatus.RESERVED) is True
        # AVAILABLE -> MAINTENANCE
        assert copy.can_transition_to(CopyStatus.MAINTENANCE) is True

    def test_invalid_status_transitions(self) -> None:
        """Invalid status transitions are rejected."""
        copy = BookCopy(
            barcode="CP001", book_isbn="978-0-123456-78-9", status=CopyStatus.BORROWED
        )

        # BORROWED -> MAINTENANCE is invalid
        assert copy.can_transition_to(CopyStatus.MAINTENANCE) is False

    def test_update_status_valid_transition(self) -> None:
        """update_status changes status for valid transitions."""
        copy = BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9")
        copy.update_status(CopyStatus.BORROWED)
        assert copy.status == CopyStatus.BORROWED

    def test_update_status_invalid_transition_raises(self) -> None:
        """update_status raises for invalid transitions."""
        copy = BookCopy(
            barcode="CP001", book_isbn="978-0-123456-78-9", status=CopyStatus.LOST
        )
        with pytest.raises(BookValidationError):
            copy.update_status(CopyStatus.BORROWED)

    def test_mark_as_borrowed(self) -> None:
        """mark_as_borrowed changes status to BORROWED."""
        copy = BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9")
        copy.mark_as_borrowed()
        assert copy.status == CopyStatus.BORROWED

    def test_mark_as_returned(self) -> None:
        """mark_as_returned changes status to AVAILABLE."""
        copy = BookCopy(
            barcode="CP001", book_isbn="978-0-123456-78-9", status=CopyStatus.BORROWED
        )
        copy.mark_as_returned()
        assert copy.status == CopyStatus.AVAILABLE

    def test_validation_rejects_empty_barcode(self) -> None:
        """Empty barcode raises ValidationError."""
        with pytest.raises(BookValidationError):
            BookCopy(barcode="", book_isbn="978-0-123456-78-9")

    def test_validation_rejects_empty_isbn(self) -> None:
        """Empty ISBN raises ValidationError."""
        with pytest.raises(BookValidationError):
            BookCopy(barcode="CP001", book_isbn="")


class TestBook:
    """Tests for the Book entity."""

    def test_create_book_with_valid_data(self) -> None:
        """Book can be created with valid data."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Clean Code",
            authors=("Robert C. Martin",),
            publisher="Prentice Hall",
            publication_year=2008,
            genre="Technology",
        )
        assert book.isbn == "978-0-123456-78-9"
        assert book.title == "Clean Code"
        assert book.authors == ("Robert C. Martin",)
        assert book.publisher == "Prentice Hall"
        assert book.publication_year == 2008
        assert book.genre == "Technology"
        assert book.copies == []

    def test_valid_isbn_10_format(self) -> None:
        """ISBN-10 format is validated."""
        book = Book(
            isbn="0132350884",
            title="Clean Code",
            authors=("Robert C. Martin",),
            publisher="Prentice Hall",
            publication_year=2008,
            genre="Technology",
        )
        assert book.isbn == "0132350884"

    def test_valid_isbn_13_format_with_hyphens(self) -> None:
        """ISBN-13 format with hyphens is validated."""
        book = Book(
            isbn="978-0-132-35088-4",
            title="Clean Code",
            authors=("Robert C. Martin",),
            publisher="Prentice Hall",
            publication_year=2008,
            genre="Technology",
        )
        assert "978" in book.isbn

    def test_invalid_isbn_raises_validation_error(self) -> None:
        """Invalid ISBN format raises ValidationError."""
        with pytest.raises(BookValidationError):
            Book(
                isbn="not-an-isbn",
                title="Invalid Book",
                authors=("Author",),
                publisher="Publisher",
                publication_year=2024,
                genre="Fiction",
            )

    def test_empty_title_raises_validation_error(self) -> None:
        """Empty title raises ValidationError."""
        with pytest.raises(BookValidationError):
            Book(
                isbn="978-0-123456-78-9",
                title="",
                authors=("Author",),
                publisher="Publisher",
                publication_year=2024,
                genre="Fiction",
            )

    def test_empty_authors_raises_validation_error(self) -> None:
        """Empty authors tuple raises ValidationError."""
        with pytest.raises(BookValidationError):
            Book(
                isbn="978-0-123456-78-9",
                title="Title",
                authors=(),
                publisher="Publisher",
                publication_year=2024,
                genre="Fiction",
            )

    def test_future_publication_year_raises_validation_error(self) -> None:
        """Future publication year raises ValidationError."""
        with pytest.raises(BookValidationError):
            Book(
                isbn="978-0-123456-78-9",
                title="Title",
                authors=("Author",),
                publisher="Publisher",
                publication_year=9999,
                genre="Fiction",
            )

    def test_add_copy_to_book(self) -> None:
        """Copies can be added to a book."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author",),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        copy = BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9")
        book.add_copy(copy)
        assert len(book.copies) == 1
        assert book.copies[0].barcode == "CP001"

    def test_add_copy_with_wrong_isbn_raises(self) -> None:
        """Adding copy with mismatched ISBN raises ValidationError."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author",),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        copy = BookCopy(barcode="CP001", book_isbn="978-0-999999-99-9")
        with pytest.raises(BookValidationError):
            book.add_copy(copy)

    def test_add_duplicate_barcode_raises(self) -> None:
        """Adding copy with duplicate barcode raises ValidationError."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author",),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        copy1 = BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9")
        copy2 = BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9")
        book.add_copy(copy1)
        with pytest.raises(BookValidationError):
            book.add_copy(copy2)

    def test_get_copy_by_barcode(self) -> None:
        """get_copy returns the correct copy by barcode."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author",),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        copy = BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9")
        book.add_copy(copy)
        found = book.get_copy("CP001")
        assert found is not None
        assert found.barcode == "CP001"

    def test_get_copy_not_found_returns_none(self) -> None:
        """get_copy returns None for non-existent barcode."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author",),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        assert book.get_copy("NONEXISTENT") is None

    def test_get_available_copies(self) -> None:
        """get_available_copies returns only available copies."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author",),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        copy1 = BookCopy(
            barcode="CP001", book_isbn="978-0-123456-78-9", status=CopyStatus.AVAILABLE
        )
        copy2 = BookCopy(
            barcode="CP002", book_isbn="978-0-123456-78-9", status=CopyStatus.BORROWED
        )
        book.add_copy(copy1)
        book.add_copy(copy2)
        available = book.get_available_copies()
        assert len(available) == 1
        assert available[0].barcode == "CP001"

    def test_has_available_copies(self) -> None:
        """has_available_copies returns True when copies available."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author",),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        copy = BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9")
        book.add_copy(copy)
        assert book.has_available_copies() is True

    def test_remove_copy(self) -> None:
        """remove_copy removes the copy by barcode."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author",),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        copy = BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9")
        book.add_copy(copy)
        removed = book.remove_copy("CP001")
        assert removed.barcode == "CP001"
        assert len(book.copies) == 0

    def test_remove_borrowed_copy_raises(self) -> None:
        """remove_copy raises for borrowed copies."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author",),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        copy = BookCopy(
            barcode="CP001",
            book_isbn="978-0-123456-78-9",
            status=CopyStatus.BORROWED,
        )
        book.add_copy(copy)
        with pytest.raises(BookValidationError):
            book.remove_copy("CP001")

    def test_author_string_property(self) -> None:
        """author_string returns comma-separated authors."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author One", "Author Two"),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        assert book.author_string == "Author One, Author Two"

    def test_copy_count_property(self) -> None:
        """copy_count returns total number of copies."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author",),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        assert book.copy_count == 0
        book.add_copy(BookCopy(barcode="CP001", book_isbn="978-0-123456-78-9"))
        assert book.copy_count == 1

    def test_available_copy_count_property(self) -> None:
        """available_copy_count returns number of available copies."""
        book = Book(
            isbn="978-0-123456-78-9",
            title="Title",
            authors=("Author",),
            publisher="Publisher",
            publication_year=2024,
            genre="Fiction",
        )
        assert book.available_copy_count == 0
        book.add_copy(
            BookCopy(
                barcode="CP001",
                book_isbn="978-0-123456-78-9",
                status=CopyStatus.AVAILABLE,
            )
        )
        book.add_copy(
            BookCopy(
                barcode="CP002",
                book_isbn="978-0-123456-78-9",
                status=CopyStatus.BORROWED,
            )
        )
        assert book.available_copy_count == 1


# =============================================================================
# Member and Librarian Tests
# =============================================================================


class TestMember:
    """Tests for the Member entity."""

    def test_create_member_with_valid_data(self) -> None:
        """Member can be created with valid data."""
        member = Member(
            member_id="MEM001",
            name="Alice Johnson",
            email="alice@example.com",
            phone="555-1234",
            address="123 Main St",
        )
        assert member.member_id == "MEM001"
        assert member.name == "Alice Johnson"
        assert member.email == "alice@example.com"
        assert member.phone == "555-1234"
        assert member.address == "123 Main St"
        assert member.status == MembershipStatus.ACTIVE

    def test_default_status_is_active(self) -> None:
        """Default membership status is ACTIVE."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
        )
        assert member.status == MembershipStatus.ACTIVE

    def test_invalid_email_raises_validation_error(self) -> None:
        """Invalid email format raises ValidationError."""
        with pytest.raises(MemberValidationError):
            Member(
                member_id="MEM001",
                name="Alice",
                email="not-an-email",
            )

    def test_empty_name_raises_validation_error(self) -> None:
        """Empty name raises ValidationError."""
        with pytest.raises(MemberValidationError):
            Member(
                member_id="MEM001",
                name="",
                email="alice@example.com",
            )

    def test_can_borrow_when_active_and_no_issues(self) -> None:
        """Active member with no issues can borrow."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
            status=MembershipStatus.ACTIVE,
        )
        assert member.can_borrow() is True

    def test_cannot_borrow_when_suspended(self) -> None:
        """Suspended member cannot borrow."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
            status=MembershipStatus.SUSPENDED,
        )
        assert member.can_borrow() is False

    def test_cannot_borrow_when_expired(self) -> None:
        """Expired member cannot borrow."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
            status=MembershipStatus.EXPIRED,
        )
        assert member.can_borrow() is False

    def test_cannot_borrow_with_high_fines(self) -> None:
        """Member with fines over threshold cannot borrow."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
            status=MembershipStatus.ACTIVE,
        )
        # Add multiple fines to exceed the $20 threshold
        member.add_fine(
            Fine(
                fine_id="F001",
                loan_id="L001",
                member_id="MEM001",
                amount=Decimal("15.00"),
                reason="Overdue",
            )
        )
        member.add_fine(
            Fine(
                fine_id="F002",
                loan_id="L002",
                member_id="MEM001",
                amount=Decimal("6.00"),
                reason="Overdue",
            )
        )
        # Total is $21.00, over the $20 threshold
        assert member.total_outstanding_fines == Decimal("21.00")
        assert member.can_borrow() is False

    def test_active_loan_count_property(self) -> None:
        """active_loan_count tracks active loans."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
        )
        assert member.active_loan_count == 0

        # Add a mock loan
        loan = Loan(
            loan_id="L001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status=LoanStatus.ACTIVE,
        )
        member.add_loan(loan)
        assert member.active_loan_count == 1

    def test_outstanding_fines_property(self) -> None:
        """outstanding_fines returns only outstanding fines."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
        )
        fine1 = Fine(
            fine_id="F001",
            loan_id="L001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue",
            status=FineStatus.OUTSTANDING,
        )
        fine2 = Fine(
            fine_id="F002",
            loan_id="L002",
            member_id="MEM001",
            amount=Decimal("3.00"),
            reason="Overdue",
            status=FineStatus.PAID,
        )
        member.add_fine(fine1)
        member.add_fine(fine2)
        assert len(member.outstanding_fines) == 1
        assert member.outstanding_fines[0].fine_id == "F001"

    def test_total_outstanding_fines_property(self) -> None:
        """total_outstanding_fines sums outstanding fine amounts."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
        )
        fine1 = Fine(
            fine_id="F001",
            loan_id="L001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue",
            status=FineStatus.OUTSTANDING,
        )
        fine2 = Fine(
            fine_id="F002",
            loan_id="L002",
            member_id="MEM001",
            amount=Decimal("3.00"),
            reason="Overdue",
            status=FineStatus.OUTSTANDING,
        )
        member.add_fine(fine1)
        member.add_fine(fine2)
        assert member.total_outstanding_fines == Decimal("8.00")

    def test_add_fine_suspends_member_over_threshold(self) -> None:
        """Adding fine over threshold suspends member."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
            status=MembershipStatus.ACTIVE,
        )
        # Add multiple fines to exceed the $20 threshold
        member.add_fine(
            Fine(
                fine_id="F001",
                loan_id="L001",
                member_id="MEM001",
                amount=Decimal("15.00"),
                reason="Overdue",
            )
        )
        member.add_fine(
            Fine(
                fine_id="F002",
                loan_id="L002",
                member_id="MEM001",
                amount=Decimal("6.00"),
                reason="Overdue",
            )
        )
        assert member.total_outstanding_fines == Decimal("21.00")
        assert member.status == MembershipStatus.SUSPENDED

    def test_suspend_and_activate(self) -> None:
        """Member can be suspended and activated."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
            status=MembershipStatus.ACTIVE,
        )
        member.suspend()
        assert member.status == MembershipStatus.SUSPENDED

        # Cannot activate if conditions not met
        member._fines = []  # Clear fines for test
        member.activate()
        assert member.status == MembershipStatus.ACTIVE

    def test_activate_raises_with_overdue_loans(self) -> None:
        """activate raises if member has overdue loans."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
            status=MembershipStatus.SUSPENDED,
        )
        # Add an overdue loan
        loan = Loan(
            loan_id="L001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date.today() - timedelta(days=30),
            due_date=date.today() - timedelta(days=16),
            status=LoanStatus.OVERDUE,
        )
        member._active_loans.append(loan)
        with pytest.raises(MemberBusinessError):
            member.activate()

    def test_get_active_loan(self) -> None:
        """get_active_loan returns loan by ID."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
        )
        loan = Loan(
            loan_id="L001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date.today(),
            due_date=date.today() + timedelta(days=14),
        )
        member.add_loan(loan)
        found = member.get_active_loan("L001")
        assert found is not None
        assert found.loan_id == "L001"

    def test_remove_loan(self) -> None:
        """remove_loan removes loan by ID."""
        member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
        )
        loan = Loan(
            loan_id="L001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date.today(),
            due_date=date.today() + timedelta(days=14),
        )
        member.add_loan(loan)
        removed = member.remove_loan("L001")
        assert removed.loan_id == "L001"
        assert member.active_loan_count == 0

    def test_can_reserve_only_when_active(self) -> None:
        """can_reserve returns True only for active members."""
        active_member = Member(
            member_id="MEM001",
            name="Alice",
            email="alice@example.com",
            status=MembershipStatus.ACTIVE,
        )
        suspended_member = Member(
            member_id="MEM002",
            name="Bob",
            email="bob@example.com",
            status=MembershipStatus.SUSPENDED,
        )
        assert active_member.can_reserve() is True
        assert suspended_member.can_reserve() is False


class TestLibrarian:
    """Tests for the Librarian entity."""

    def test_create_librarian_with_valid_data(self) -> None:
        """Librarian can be created with valid data."""
        librarian = Librarian(
            staff_id="LIB001",
            name="Bob Smith",
            email="bob@library.org",
            role=StaffRole.LIBRARIAN,
        )
        assert librarian.staff_id == "LIB001"
        assert librarian.name == "Bob Smith"
        assert librarian.email == "bob@library.org"
        assert librarian.role == StaffRole.LIBRARIAN

    def test_default_role_is_assistant(self) -> None:
        """Default role is ASSISTANT."""
        librarian = Librarian(
            staff_id="LIB001",
            name="Bob",
            email="bob@library.org",
        )
        assert librarian.role == StaffRole.ASSISTANT

    def test_role_permissions_assigned_correctly(self) -> None:
        """Permissions are assigned based on role."""
        assistant = Librarian(
            staff_id="LIB001",
            name="Assistant",
            email="a@library.org",
            role=StaffRole.ASSISTANT,
        )
        assert assistant.can_checkout() is True
        assert assistant.can_manage_members() is False

        librarian = Librarian(
            staff_id="LIB002",
            name="Librarian",
            email="l@library.org",
            role=StaffRole.LIBRARIAN,
        )
        assert librarian.can_checkout() is True
        assert librarian.can_manage_members() is True

        manager = Librarian(
            staff_id="LIB003",
            name="Manager",
            email="m@library.org",
            role=StaffRole.MANAGER,
        )
        assert manager.can_checkout() is True
        assert manager.can_generate_reports() is True

    def test_has_permission(self) -> None:
        """has_permission checks specific permission."""
        librarian = Librarian(
            staff_id="LIB001",
            name="Bob",
            email="bob@library.org",
        )
        assert librarian.has_permission("checkout") is True
        assert librarian.has_permission("nonexistent") is False

    def test_grant_permission(self) -> None:
        """grant_permission adds a permission."""
        librarian = Librarian(
            staff_id="LIB001",
            name="Bob",
            email="bob@library.org",
            role=StaffRole.ASSISTANT,
        )
        assert librarian.can_waive_fines() is False
        librarian.grant_permission("waive_fine")
        assert librarian.can_waive_fines() is True

    def test_revoke_permission(self) -> None:
        """revoke_permission removes a permission."""
        librarian = Librarian(
            staff_id="LIB001",
            name="Bob",
            email="bob@library.org",
            role=StaffRole.LIBRARIAN,
        )
        assert librarian.can_waive_fines() is True
        librarian.revoke_permission("waive_fine")
        assert librarian.can_waive_fines() is False

    def test_promote_changes_role_and_permissions(self) -> None:
        """promote updates role and permissions."""
        librarian = Librarian(
            staff_id="LIB001",
            name="Bob",
            email="bob@library.org",
            role=StaffRole.ASSISTANT,
        )
        assert librarian.can_manage_members() is False
        librarian.promote(StaffRole.LIBRARIAN)
        assert librarian.role == StaffRole.LIBRARIAN
        assert librarian.can_manage_members() is True

    def test_invalid_email_raises_validation_error(self) -> None:
        """Invalid email raises ValidationError."""
        with pytest.raises(MemberValidationError):
            Librarian(
                staff_id="LIB001",
                name="Bob",
                email="not-an-email",
            )


# =============================================================================
# Loan and Reservation Tests
# =============================================================================


class TestLoan:
    """Tests for the Loan entity."""

    def test_create_loan_with_valid_data(self) -> None:
        """Loan can be created with valid data."""
        checkout = date(2024, 1, 1)
        due = date(2024, 1, 15)
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=checkout,
            due_date=due,
        )
        assert loan.loan_id == "LOAN001"
        assert loan.copy_barcode == "CP001"
        assert loan.member_id == "MEM001"
        assert loan.checkout_date == checkout
        assert loan.due_date == due
        assert loan.status == LoanStatus.ACTIVE
        assert loan.renewal_count == 0

    def test_factory_create_calculates_due_date(self) -> None:
        """create factory method calculates due date."""
        checkout = date(2024, 1, 1)
        loan = Loan.create(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=checkout,
        )
        assert loan.due_date == checkout + timedelta(days=14)

    def test_due_date_must_be_after_checkout(self) -> None:
        """Due date before checkout raises ValidationError."""
        with pytest.raises(LoanValidationError):
            Loan(
                loan_id="LOAN001",
                copy_barcode="CP001",
                member_id="MEM001",
                checkout_date=date(2024, 1, 15),
                due_date=date(2024, 1, 1),
            )

    def test_is_overdue_true_when_past_due(self) -> None:
        """is_overdue returns True when past due date."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
        )
        assert loan.is_overdue(today=date(2024, 1, 20)) is True

    def test_is_overdue_false_when_not_due(self) -> None:
        """is_overdue returns False when not past due."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
        )
        assert loan.is_overdue(today=date(2024, 1, 10)) is False

    def test_is_overdue_false_for_returned_loans(self) -> None:
        """is_overdue returns False for returned loans."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
            return_date=date(2024, 1, 10),
            status=LoanStatus.RETURNED,
        )
        assert loan.is_overdue(today=date(2024, 1, 20)) is False

    def test_days_overdue_calculation(self) -> None:
        """days_overdue returns correct number of days."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
        )
        assert loan.days_overdue(today=date(2024, 1, 20)) == 5

    def test_days_overdue_zero_when_not_overdue(self) -> None:
        """days_overdue returns 0 when not overdue."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
        )
        assert loan.days_overdue(today=date(2024, 1, 10)) == 0

    def test_can_renew_when_eligible(self) -> None:
        """can_renew returns True when conditions met."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
            status=LoanStatus.ACTIVE,
            renewal_count=0,
        )
        assert loan.can_renew(has_reservation=False) is True

    def test_cannot_renew_when_max_renewals_reached(self) -> None:
        """can_renew returns False when max renewals reached."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
            status=LoanStatus.ACTIVE,
            renewal_count=2,
        )
        assert loan.can_renew(has_reservation=False) is False

    def test_cannot_renew_when_has_reservation(self) -> None:
        """can_renew returns False when book has reservation."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
            status=LoanStatus.ACTIVE,
            renewal_count=0,
        )
        assert loan.can_renew(has_reservation=True) is False

    def test_renew_extends_due_date(self) -> None:
        """renew extends due date by 14 days."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
            status=LoanStatus.ACTIVE,
            renewal_count=0,
        )
        original_due = loan.due_date
        loan.renew(has_reservation=False)
        assert loan.due_date == original_due + timedelta(days=14)
        assert loan.renewal_count == 1

    def test_renew_raises_when_not_eligible(self) -> None:
        """renew raises when renewal not allowed."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
            status=LoanStatus.ACTIVE,
            renewal_count=2,
        )
        with pytest.raises(LoanBusinessError):
            loan.renew(has_reservation=False)

    def test_return_book_sets_return_date_and_status(self) -> None:
        """return_book sets return date and changes status."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
            status=LoanStatus.ACTIVE,
        )
        loan.return_book(return_date=date(2024, 1, 14))
        assert loan.return_date == date(2024, 1, 14)
        assert loan.status == LoanStatus.RETURNED

    def test_return_book_raises_for_non_active_loan(self) -> None:
        """return_book raises for already returned loan."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
            return_date=date(2024, 1, 14),
            status=LoanStatus.RETURNED,
        )
        with pytest.raises(LoanBusinessError):
            loan.return_book()

    def test_mark_as_lost_changes_status(self) -> None:
        """mark_as_lost changes status to LOST."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
            status=LoanStatus.ACTIVE,
        )
        loan.mark_as_lost()
        assert loan.status == LoanStatus.LOST

    def test_update_status_transitions_active_to_overdue(self) -> None:
        """update_status transitions ACTIVE to OVERDUE when appropriate."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
            status=LoanStatus.ACTIVE,
        )
        loan.update_status(today=date(2024, 1, 20))
        assert loan.status == LoanStatus.OVERDUE

    def test_days_remaining_positive_when_not_due(self) -> None:
        """days_remaining returns positive days until due."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
        )
        assert loan.days_remaining(today=date(2024, 1, 10)) == 5

    def test_days_remaining_negative_when_overdue(self) -> None:
        """days_remaining returns negative when overdue."""
        loan = Loan(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
        )
        assert loan.days_remaining(today=date(2024, 1, 20)) == -5


class TestReservation:
    """Tests for the Reservation entity."""

    def test_create_reservation_with_valid_data(self) -> None:
        """Reservation can be created with valid data."""
        now = datetime.now()
        reservation = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=now,
            queue_position=1,
        )
        assert reservation.reservation_id == "RES001"
        assert reservation.book_isbn == "978-0-123456-78-9"
        assert reservation.member_id == "MEM001"
        assert reservation.reservation_date == now
        assert reservation.status == ReservationStatus.PENDING
        assert reservation.queue_position == 1

    def test_factory_create_sets_defaults(self) -> None:
        """create factory method sets appropriate defaults."""
        reservation = Reservation.create(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            queue_position=1,
        )
        assert reservation.status == ReservationStatus.PENDING
        assert reservation.queue_position == 1

    def test_fulfill_changes_status_and_clears_queue_position(self) -> None:
        """fulfill changes status to FULFILLED and clears queue position."""
        reservation = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=datetime.now(),
            queue_position=1,
        )
        reservation.fulfill(hold_until=date(2024, 1, 20))
        assert reservation.status == ReservationStatus.FULFILLED
        assert reservation.queue_position is None
        assert reservation.expiry_date == date(2024, 1, 20)

    def test_fulfill_raises_when_not_pending(self) -> None:
        """fulfill raises when reservation not in PENDING status."""
        reservation = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=datetime.now(),
            status=ReservationStatus.FULFILLED,
        )
        with pytest.raises(LoanBusinessError):
            reservation.fulfill()

    def test_cancel_changes_status(self) -> None:
        """cancel changes status to CANCELLED."""
        reservation = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=datetime.now(),
            queue_position=1,
        )
        reservation.cancel()
        assert reservation.status == ReservationStatus.CANCELLED
        assert reservation.queue_position is None

    def test_cancel_raises_when_fulfilled(self) -> None:
        """cancel raises when reservation already fulfilled."""
        reservation = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=datetime.now(),
            status=ReservationStatus.FULFILLED,
        )
        with pytest.raises(LoanBusinessError):
            reservation.cancel()

    def test_expire_changes_status(self) -> None:
        """expire changes status to EXPIRED."""
        reservation = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=datetime.now(),
            status=ReservationStatus.FULFILLED,
        )
        reservation.expire()
        assert reservation.status == ReservationStatus.EXPIRED

    def test_is_expired_true_when_past_expiry(self) -> None:
        """is_expired returns True when past expiry date."""
        reservation = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=datetime.now(),
            status=ReservationStatus.FULFILLED,
            expiry_date=date(2024, 1, 15),
        )
        assert reservation.is_expired(today=date(2024, 1, 20)) is True

    def test_is_expired_false_for_pending(self) -> None:
        """is_expired returns False for pending reservations."""
        reservation = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=datetime.now(),
            status=ReservationStatus.PENDING,
        )
        assert reservation.is_expired() is False

    def test_update_queue_position(self) -> None:
        """update_queue_position changes queue position."""
        reservation = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=datetime.now(),
            queue_position=1,
        )
        reservation.update_queue_position(2)
        assert reservation.queue_position == 2

    def test_is_pending_property(self) -> None:
        """is_pending returns True only for PENDING status."""
        pending = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=datetime.now(),
            status=ReservationStatus.PENDING,
        )
        fulfilled = Reservation(
            reservation_id="RES002",
            book_isbn="978-0-123456-78-9",
            member_id="MEM002",
            reservation_date=datetime.now(),
            status=ReservationStatus.FULFILLED,
        )
        assert pending.is_pending is True
        assert fulfilled.is_pending is False

    def test_is_fulfilled_property(self) -> None:
        """is_fulfilled returns True only for FULFILLED status."""
        fulfilled = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=datetime.now(),
            status=ReservationStatus.FULFILLED,
        )
        pending = Reservation(
            reservation_id="RES002",
            book_isbn="978-0-123456-78-9",
            member_id="MEM002",
            reservation_date=datetime.now(),
            status=ReservationStatus.PENDING,
        )
        assert fulfilled.is_fulfilled is True
        assert pending.is_fulfilled is False

    def test_wait_time_days_calculation(self) -> None:
        """wait_time_days calculates days since reservation."""
        reservation_date = datetime(2024, 1, 1, 12, 0, 0)
        reservation = Reservation(
            reservation_id="RES001",
            book_isbn="978-0-123456-78-9",
            member_id="MEM001",
            reservation_date=reservation_date,
        )
        assert reservation.wait_time_days(today=date(2024, 1, 10)) == 9


# =============================================================================
# Fine Tests
# =============================================================================


class TestFine:
    """Tests for the Fine value object."""

    def test_create_fine_with_valid_data(self) -> None:
        """Fine can be created with valid data."""
        fine = Fine(
            fine_id="FINE001",
            loan_id="LOAN001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue by 10 days",
        )
        assert fine.fine_id == "FINE001"
        assert fine.loan_id == "LOAN001"
        assert fine.member_id == "MEM001"
        assert fine.amount == Decimal("5.00")
        assert fine.reason == "Overdue by 10 days"
        assert fine.status == FineStatus.OUTSTANDING

    def test_factory_create_calculates_amount(self) -> None:
        """create factory method calculates amount based on days and rate."""
        fine = Fine.create(
            fine_id="FINE001",
            loan_id="LOAN001",
            member_id="MEM001",
            days_overdue=10,
            daily_rate=Decimal("0.50"),
        )
        assert fine.amount == Decimal("5.00")
        assert "10 days" in fine.reason

    def test_create_respects_maximum_amount(self) -> None:
        """create caps amount at MAX_FINE_PER_BOOK."""
        fine = Fine.create(
            fine_id="FINE001",
            loan_id="LOAN001",
            member_id="MEM001",
            days_overdue=100,  # Would be $50 at $0.50/day
            daily_rate=Decimal("0.50"),
        )
        assert fine.amount == Fine.MAX_FINE_PER_BOOK  # $20.00

    def test_negative_amount_raises_validation_error(self) -> None:
        """Negative amount raises ValidationError."""
        with pytest.raises(FineValidationError):
            Fine(
                fine_id="FINE001",
                loan_id="LOAN001",
                member_id="MEM001",
                amount=Decimal("-5.00"),
                reason="Overdue",
            )

    def test_amount_over_maximum_raises_validation_error(self) -> None:
        """Amount over maximum raises ValidationError."""
        with pytest.raises(FineValidationError):
            Fine(
                fine_id="FINE001",
                loan_id="LOAN001",
                member_id="MEM001",
                amount=Decimal("25.00"),
                reason="Overdue",
            )

    def test_mark_as_paid_changes_status(self) -> None:
        """mark_as_paid returns new Fine with PAID status."""
        fine = Fine(
            fine_id="FINE001",
            loan_id="LOAN001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue",
            issued_date=date(2024, 1, 15),
        )
        paid_fine = fine.mark_as_paid(paid_date=date(2024, 1, 20))
        assert paid_fine.status == FineStatus.PAID
        assert paid_fine.paid_date == date(2024, 1, 20)
        # Original fine unchanged (immutable)
        assert fine.status == FineStatus.OUTSTANDING

    def test_mark_as_paid_raises_when_already_paid(self) -> None:
        """mark_as_paid raises when fine already paid."""
        fine = Fine(
            fine_id="FINE001",
            loan_id="LOAN001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue",
            status=FineStatus.PAID,
            issued_date=date(2024, 1, 10),
            paid_date=date(2024, 1, 15),
        )
        with pytest.raises(FineBusinessError):
            fine.mark_as_paid()

    def test_waive_changes_status(self) -> None:
        """waive returns new Fine with WAIVED status."""
        fine = Fine(
            fine_id="FINE001",
            loan_id="LOAN001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue",
        )
        waived_fine = fine.waive(waived_by="LIB001")
        assert waived_fine.status == FineStatus.WAIVED
        assert "waived by LIB001" in waived_fine.reason

    def test_is_outstanding_property(self) -> None:
        """is_outstanding returns True only for OUTSTANDING status."""
        outstanding = Fine(
            fine_id="F001",
            loan_id="L001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue",
            status=FineStatus.OUTSTANDING,
        )
        paid = Fine(
            fine_id="F002",
            loan_id="L002",
            member_id="MEM001",
            amount=Decimal("3.00"),
            reason="Overdue",
            status=FineStatus.PAID,
        )
        assert outstanding.is_outstanding is True
        assert paid.is_outstanding is False

    def test_is_paid_property(self) -> None:
        """is_paid returns True only for PAID status."""
        paid = Fine(
            fine_id="F001",
            loan_id="L001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue",
            status=FineStatus.PAID,
            issued_date=date(2024, 1, 10),
            paid_date=date(2024, 1, 15),
        )
        outstanding = Fine(
            fine_id="F002",
            loan_id="L002",
            member_id="MEM001",
            amount=Decimal("3.00"),
            reason="Overdue",
            status=FineStatus.OUTSTANDING,
        )
        assert paid.is_paid is True
        assert outstanding.is_paid is False

    def test_is_waived_property(self) -> None:
        """is_waived returns True only for WAIVED status."""
        waived = Fine(
            fine_id="F001",
            loan_id="L001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue",
            status=FineStatus.WAIVED,
        )
        outstanding = Fine(
            fine_id="F002",
            loan_id="L002",
            member_id="MEM001",
            amount=Decimal("3.00"),
            reason="Overdue",
            status=FineStatus.OUTSTANDING,
        )
        assert waived.is_waived is True
        assert outstanding.is_waived is False

    def test_fine_equality(self) -> None:
        """Fines are equal based on fine_id, amount, and status."""
        fine1 = Fine(
            fine_id="F001",
            loan_id="L001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue",
        )
        fine2 = Fine(
            fine_id="F001",
            loan_id="L002",  # Different loan
            member_id="MEM002",  # Different member
            amount=Decimal("5.00"),
            reason="Different reason",
        )
        fine3 = Fine(
            fine_id="F002",  # Different ID
            loan_id="L001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue",
        )
        assert fine1 == fine2  # Same fine_id and amount
        assert fine1 != fine3  # Different fine_id

    def test_fine_hash(self) -> None:
        """Fine hash is based on fine_id."""
        fine = Fine(
            fine_id="F001",
            loan_id="L001",
            member_id="MEM001",
            amount=Decimal("5.00"),
            reason="Overdue",
        )
        assert hash(fine) == hash("F001")


# =============================================================================
# Domain Enumeration Tests
# =============================================================================


class TestEnums:
    """Tests for domain enumerations."""

    def test_copy_status_values(self) -> None:
        """CopyStatus has expected values."""
        assert CopyStatus.AVAILABLE.value == "available"
        assert CopyStatus.BORROWED.value == "borrowed"
        assert CopyStatus.RESERVED.value == "reserved"
        assert CopyStatus.MAINTENANCE.value == "maintenance"
        assert CopyStatus.LOST.value == "lost"

    def test_loan_status_values(self) -> None:
        """LoanStatus has expected values."""
        assert LoanStatus.ACTIVE.value == "active"
        assert LoanStatus.RETURNED.value == "returned"
        assert LoanStatus.OVERDUE.value == "overdue"
        assert LoanStatus.LOST.value == "lost"

    def test_membership_status_values(self) -> None:
        """MembershipStatus has expected values."""
        assert MembershipStatus.ACTIVE.value == "active"
        assert MembershipStatus.SUSPENDED.value == "suspended"
        assert MembershipStatus.EXPIRED.value == "expired"

    def test_reservation_status_values(self) -> None:
        """ReservationStatus has expected values."""
        assert ReservationStatus.PENDING.value == "pending"
        assert ReservationStatus.FULFILLED.value == "fulfilled"
        assert ReservationStatus.CANCELLED.value == "cancelled"
        assert ReservationStatus.EXPIRED.value == "expired"

    def test_fine_status_values(self) -> None:
        """FineStatus has expected values."""
        assert FineStatus.OUTSTANDING.value == "outstanding"
        assert FineStatus.PAID.value == "paid"
        assert FineStatus.WAIVED.value == "waived"

    def test_staff_role_values(self) -> None:
        """StaffRole has expected values."""
        assert StaffRole.ASSISTANT.value == "assistant"
        assert StaffRole.LIBRARIAN.value == "librarian"
        assert StaffRole.MANAGER.value == "manager"

    def test_condition_values(self) -> None:
        """Condition has expected values."""
        assert Condition.EXCELLENT.value == "excellent"
        assert Condition.GOOD.value == "good"
        assert Condition.FAIR.value == "fair"
        assert Condition.POOR.value == "poor"
        assert Condition.DAMAGED.value == "damaged"

"""Tests for service layer implementations."""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

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
from ..services.catalog_service import (
    CatalogService,
    TitleSearchStrategy,
    AuthorSearchStrategy,
)
from ..services.circulation_service import (
    CirculationService,
    CirculationEvent,
    EventBus,
)
from ..services.reservation_service import ReservationService
from ..services.fine_service import (
    FineService,
    StandardFineStrategy,
    ForgivingFineStrategy,
)


class TestCatalogService:
    """Tests for CatalogService with Strategy pattern."""

    @pytest.fixture
    def service(self) -> CatalogService:
        """Create a catalog service with in-memory repository."""
        repo = InMemoryBookRepository()
        return CatalogService(repo)

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

    def test_add_book(self, service: CatalogService, sample_book: Book) -> None:
        """Test adding a book to the catalog."""
        added = service.add_book(sample_book)
        assert added.isbn is not None

        found = service.get_book(added.isbn)
        assert found is not None
        assert found.title == sample_book.title

    def test_add_copy(self, service: CatalogService, sample_book: Book) -> None:
        """Test adding a copy to a book."""
        added = service.add_book(sample_book)
        copy = BookCopy(barcode="CP001", book_isbn=added.isbn)
        saved_copy = service.add_copy(added.isbn, copy)

        assert saved_copy is not None
        assert saved_copy.book_isbn == added.isbn
        assert saved_copy.status == CopyStatus.AVAILABLE

    def test_search_by_title_strategy(self, service: CatalogService) -> None:
        """Test title search strategy."""
        # Add books
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
        service.add_book(book1)
        service.add_book(book2)

        # Use title strategy
        service.set_search_strategy(TitleSearchStrategy())
        results = service.search("Python")

        assert len(results) == 1
        assert results[0].book.title == "Python Programming"

    def test_search_by_author_strategy(self, service: CatalogService) -> None:
        """Test author search strategy."""
        book = Book(
            isbn="978-0-00-111001-1",
            title="Some Book",
            authors=("Alice Johnson", "Bob Smith"),
            publisher="Pub",
            publication_year=2020,
            genre="Fiction",
        )
        service.add_book(book)

        service.set_search_strategy(AuthorSearchStrategy())
        results = service.search("Alice")

        assert len(results) == 1

    def test_is_book_available(self, service: CatalogService, sample_book: Book) -> None:
        """Test checking book availability."""
        added = service.add_book(sample_book)
        assert not service.is_book_available(added.isbn)

        copy = BookCopy(barcode="CP001", book_isbn=added.isbn)
        service.add_copy(added.isbn, copy)
        assert service.is_book_available(added.isbn)

    def test_get_catalog_statistics(self, service: CatalogService) -> None:
        """Test catalog statistics."""
        book = Book(
            isbn="978-0-00-111001-1",
            title="Test Book",
            authors=("Author",),
            publisher="Pub",
            publication_year=2020,
            genre="Fiction",
        )
        added = service.add_book(book)
        copy1 = BookCopy(barcode="CP001", book_isbn=added.isbn)
        copy2 = BookCopy(barcode="CP002", book_isbn=added.isbn)
        service.add_copy(added.isbn, copy1)
        service.add_copy(added.isbn, copy2)

        stats = service.get_catalog_statistics()
        assert stats["total_books"] == 1
        assert stats["total_copies"] == 2
        assert stats["available_copies"] == 2


class TestCirculationService:
    """Tests for CirculationService with Observer pattern."""

    @pytest.fixture
    def service(self) -> CirculationService:
        """Create a circulation service with fresh repositories."""
        book_repo = InMemoryBookRepository()
        member_repo = InMemoryMemberRepository()
        loan_repo = InMemoryLoanRepository()
        return CirculationService(book_repo, member_repo, loan_repo)

    @pytest.fixture
    def setup_book_and_member(self, service: CirculationService) -> tuple[str, str]:
        """Create a book copy and member, return their IDs."""
        book = Book(
            isbn="978-0-00-111001-1",
            title="Test Book",
            authors=("Author",),
            publisher="Pub",
            publication_year=2020,
            genre="Fiction",
        )
        saved_book = service._book_repo.save_book(book)
        copy = BookCopy(barcode="CP001", book_isbn=saved_book.isbn)
        saved_book.add_copy(copy)
        service._book_repo.save_copy(copy)

        member = Member(
            member_id="MEM001",
            name="Test Member",
            email="test@example.com",
            phone="555-0101",
            address="123 Main St",
        )
        saved_member = service._member_repo.save(member)

        return copy.barcode, saved_member.member_id

    def test_successful_checkout(
        self, service: CirculationService, setup_book_and_member: tuple[str, str]
    ) -> None:
        """Test successful book checkout."""
        copy_barcode, member_id = setup_book_and_member

        success, message, loan = service.checkout(copy_barcode, member_id, loan_id="LOAN001")

        assert success is True
        assert loan is not None
        assert loan.copy_barcode == copy_barcode
        assert loan.member_id == member_id
        assert loan.status == LoanStatus.ACTIVE

    def test_checkout_unavailable_copy(
        self, service: CirculationService, setup_book_and_member: tuple[str, str]
    ) -> None:
        """Test checkout when copy is not available."""
        copy_barcode, member_id = setup_book_and_member

        # First checkout
        service.checkout(copy_barcode, member_id, loan_id="LOAN001")

        # Try second checkout of same copy
        member2 = Member(
            member_id="MEM002",
            name="Second Member",
            email="second@example.com",
            phone="555-0102",
            address="456 Oak Ave",
        )
        saved_member2 = service._member_repo.save(member2)

        success, message, loan = service.checkout(copy_barcode, saved_member2.member_id)

        assert success is False
        assert "not available" in message.lower()

    def test_successful_return(
        self, service: CirculationService, setup_book_and_member: tuple[str, str]
    ) -> None:
        """Test successful book return."""
        copy_barcode, member_id = setup_book_and_member

        # Checkout first
        service.checkout(copy_barcode, member_id, loan_id="LOAN001")

        # Return
        success, message, loan = service.return_book(copy_barcode)

        assert success is True
        assert loan.status == LoanStatus.RETURNED
        assert loan.return_date is not None

    def test_event_bus_emits_events(
        self, service: CirculationService, setup_book_and_member: tuple[str, str]
    ) -> None:
        """Test that event bus emits checkout events."""
        events = []

        def capture_event(event: CirculationEvent) -> None:
            events.append(event)

        service.event_bus.on("checkout", capture_event)

        copy_barcode, member_id = setup_book_and_member
        service.checkout(copy_barcode, member_id, loan_id="LOAN001")

        assert len(events) == 1
        assert events[0].event_type == "checkout"
        assert events[0].copy_barcode == copy_barcode
        assert events[0].member_id == member_id


class TestReservationService:
    """Tests for ReservationService."""

    @pytest.fixture
    def service(self) -> ReservationService:
        """Create a reservation service with fresh repositories."""
        book_repo = InMemoryBookRepository()
        member_repo = InMemoryMemberRepository()
        loan_repo = InMemoryLoanRepository()
        return ReservationService(book_repo, member_repo, loan_repo)

    @pytest.fixture
    def setup_book_and_member(self, service: ReservationService) -> tuple[str, str]:
        """Create a book and member, return their IDs."""
        book = Book(
            isbn="978-0-00-111001-1",
            title="Test Book",
            authors=("Author",),
            publisher="Pub",
            publication_year=2020,
            genre="Fiction",
        )
        book_repo = service._book_repo
        saved_book = book_repo.save_book(book)

        member = Member(
            member_id="MEM001",
            name="Test Member",
            email="test@example.com",
            phone="555-0101",
            address="123 Main St",
        )
        saved_member = service._member_repo.save(member)

        return saved_book.isbn, saved_member.member_id

    def test_create_reservation(
        self, service: ReservationService, setup_book_and_member: tuple[str, str]
    ) -> None:
        """Test creating a reservation."""
        book_isbn, member_id = setup_book_and_member

        success, message, reservation = service.create_reservation(
            book_isbn, member_id, reservation_id="RES001"
        )

        assert success is True
        assert reservation is not None
        assert reservation.book_isbn == book_isbn
        assert reservation.member_id == member_id


class TestFineService:
    """Tests for FineService with Strategy pattern."""

    @pytest.fixture
    def service(self) -> FineService:
        """Create a fine service with fresh repositories."""
        member_repo = InMemoryMemberRepository()
        loan_repo = InMemoryLoanRepository()
        return FineService(member_repo, loan_repo)

    def test_standard_fine_strategy(self) -> None:
        """Test standard fine calculation."""
        strategy = StandardFineStrategy()

        # Create an overdue loan
        loan = Loan.create(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date.today() - timedelta(days=20),
        )
        # Due date is 14 days after checkout

        breakdown = strategy.calculate(loan, current_date=date.today())

        assert breakdown.days_overdue > 0
        assert breakdown.total_amount > 0

    def test_forgiving_fine_strategy(self) -> None:
        """Test forgiving fine calculation with discount."""
        strategy = ForgivingFineStrategy(discount_percentage=0.5)

        loan = Loan.create(
            loan_id="LOAN001",
            copy_barcode="CP001",
            member_id="MEM001",
            checkout_date=date.today() - timedelta(days=20),
        )

        breakdown = strategy.calculate(loan, current_date=date.today())

        assert breakdown.processing_fee == Decimal("0.00")  # No processing fee

    def test_set_member_strategy(self, service: FineService) -> None:
        """Test setting a custom strategy for a member."""
        member = Member(
            member_id="MEM001",
            name="Test",
            email="test@example.com",
            phone="555-0101",
            address="123 Main St",
        )
        service._member_repo.save(member)

        success = service.set_member_strategy(member.member_id, "forgiving")
        assert success is True

        # Invalid strategy should fail
        success = service.set_member_strategy(member.member_id, "invalid")
        assert success is False

    def test_fine_statistics(self, service: FineService) -> None:
        """Test getting fine statistics."""
        # Create members
        member1 = Member(
            member_id="MEM001",
            name="Test 1",
            email="test1@example.com",
            phone="555-0101",
            address="123 Main St",
        )
        member2 = Member(
            member_id="MEM002",
            name="Test 2",
            email="test2@example.com",
            phone="555-0102",
            address="456 Oak Ave",
        )
        service._member_repo.save(member1)
        service._member_repo.save(member2)

        stats = service.get_fine_statistics()

        assert "total_outstanding_fines" in stats
        assert "members_with_fines" in stats

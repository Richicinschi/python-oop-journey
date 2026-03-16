"""Circulation service for checkout/return operations.

Uses Observer pattern for event notifications and Factory pattern
for loan creation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from typing import Callable, Optional

from ..domain.book import BookCopy
from ..domain.enums import CopyStatus, LoanStatus
from ..domain.loan import Loan
from ..repositories.book_repository import BookRepository
from ..repositories.loan_repository import LoanRepository
from ..repositories.member_repository import MemberRepository


@dataclass
class CirculationEvent:
    """Event data for circulation operations."""

    event_type: str  # 'checkout', 'return', 'renew', 'overdue'
    loan_id: Optional[str]
    copy_barcode: str
    member_id: str
    timestamp: datetime
    details: dict


class CirculationObserver(ABC):
    """Abstract observer for circulation events.

    Observer Pattern: Allows subscribers to react to circulation events.
    """

    @abstractmethod
    def on_event(self, event: CirculationEvent) -> None:
        """Handle a circulation event."""
        raise NotImplementedError


class EventBus:
    """Simple event bus for Observer pattern implementation.

    Manages subscriptions and event broadcasting.
    """

    def __init__(self) -> None:
        self._observers: list[CirculationObserver] = []
        self._handlers: dict[str, list[Callable[[CirculationEvent], None]]] = {}

    def subscribe(self, observer: CirculationObserver) -> None:
        """Subscribe an observer to all events."""
        self._observers.append(observer)

    def unsubscribe(self, observer: CirculationObserver) -> None:
        """Unsubscribe an observer."""
        if observer in self._observers:
            self._observers.remove(observer)

    def on(self, event_type: str, handler: Callable[[CirculationEvent], None]) -> None:
        """Register a handler for a specific event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def emit(self, event: CirculationEvent) -> None:
        """Emit an event to all observers and handlers."""
        # Notify registered observers
        for observer in self._observers:
            try:
                observer.on_event(event)
            except Exception:
                pass  # Don't let observers break the flow

        # Call specific handlers
        handlers = self._handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                pass


class CirculationService:
    """Service for book circulation operations.

    Coordinates checkout, return, and renewal operations.
    Uses Observer pattern for event notifications.
    """

    def __init__(
        self,
        book_repository: BookRepository,
        member_repository: MemberRepository,
        loan_repository: LoanRepository,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self._book_repo = book_repository
        self._member_repo = member_repository
        self._loan_repo = loan_repository
        self._event_bus = event_bus or EventBus()

    @property
    def event_bus(self) -> EventBus:
        """Access the event bus for subscribing to events."""
        return self._event_bus

    def checkout(
        self,
        copy_barcode: str,
        member_id: str,
        loan_id: Optional[str] = None,
    ) -> tuple[bool, str, Optional[Loan]]:
        """Check out a book copy to a member.

        Returns:
            Tuple of (success, message, loan)
        """
        # Validate book copy
        copy = self._book_repo.find_copy_by_barcode(copy_barcode)
        if not copy:
            return False, "Book copy not found", None

        if not copy.is_available():
            return False, f"Book copy is not available (status: {copy.status.value})", None

        # Check for existing active loan
        existing_loan = self._loan_repo.find_active_by_copy(copy_barcode)
        if existing_loan:
            return False, "Book copy is already checked out", None

        # Validate member
        member = self._member_repo.find_by_id(member_id)
        if not member:
            return False, "Member not found", None

        if not member.can_borrow():
            return False, "Member cannot borrow books at this time", None

        # Create loan using factory method
        new_loan = Loan.create(
            loan_id=loan_id or f"LOAN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            copy_barcode=copy_barcode,
            member_id=member_id,
        )

        # Update copy status
        copy.mark_as_borrowed()
        self._book_repo.save_copy(copy)

        # Add loan to member
        member.add_loan(new_loan)
        self._member_repo.save(member)

        # Save loan
        saved_loan = self._loan_repo.save(new_loan)

        # Emit event
        self._event_bus.emit(
            CirculationEvent(
                event_type="checkout",
                loan_id=saved_loan.loan_id,
                copy_barcode=copy_barcode,
                member_id=member_id,
                timestamp=datetime.now(),
                details={"due_date": saved_loan.due_date.isoformat()},
            )
        )

        return True, "Book checked out successfully", saved_loan

    def return_book(
        self,
        copy_barcode: str,
        return_date: Optional[date] = None,
    ) -> tuple[bool, str, Optional[Loan]]:
        """Return a checked out book copy.

        Returns:
            Tuple of (success, message, loan)
        """
        # Find active loan
        loan = self._loan_repo.find_active_by_copy(copy_barcode)
        if not loan:
            return False, "No active loan found for this book copy", None

        # Process return
        loan.return_book(return_date)
        self._loan_repo.save(loan)

        # Update copy status
        copy = self._book_repo.find_copy_by_barcode(copy_barcode)
        if copy:
            copy.mark_as_returned()
            self._book_repo.save_copy(copy)

        # Update member
        member = self._member_repo.find_by_id(loan.member_id)
        if member:
            member.remove_loan(loan.loan_id)
            self._member_repo.save(member)

        # Emit event
        self._event_bus.emit(
            CirculationEvent(
                event_type="return",
                loan_id=loan.loan_id,
                copy_barcode=copy_barcode,
                member_id=loan.member_id,
                timestamp=datetime.now(),
                details={"was_overdue": loan.status == LoanStatus.OVERDUE},
            )
        )

        return True, "Book returned successfully", loan

    def renew(self, loan_id: str, has_reservation: bool = False) -> tuple[bool, str]:
        """Renew a loan.

        Returns:
            Tuple of (success, message)
        """
        loan = self._loan_repo.find_by_id(loan_id)
        if not loan:
            return False, "Loan not found"

        try:
            loan.renew(has_reservation=has_reservation)
            self._loan_repo.save(loan)

            # Emit event
            self._event_bus.emit(
                CirculationEvent(
                    event_type="renew",
                    loan_id=loan.loan_id,
                    copy_barcode=loan.copy_barcode,
                    member_id=loan.member_id,
                    timestamp=datetime.now(),
                    details={
                        "new_due_date": loan.due_date.isoformat(),
                        "renewal_count": loan.renewal_count,
                    },
                )
            )

            return True, "Loan renewed successfully"
        except Exception as e:
            return False, str(e)

    def get_member_loans(self, member_id: str) -> list[Loan]:
        """Get all loans for a member."""
        return self._loan_repo.find_by_member(member_id)

    def get_active_loans(self, member_id: str) -> list[Loan]:
        """Get active loans for a member."""
        return self._loan_repo.find_active_by_member(member_id)

    def get_overdue_loans(self) -> list[Loan]:
        """Get all overdue loans."""
        return self._loan_repo.find_overdue_loans()

    def get_member_overdue_loans(self, member_id: str) -> list[Loan]:
        """Get overdue loans for a specific member."""
        return self._loan_repo.find_overdue_loans()

    def process_overdue_check(self) -> list[Loan]:
        """Check for newly overdue loans and emit events.

        Returns:
            List of loans that are now overdue
        """
        overdue_loans = []
        all_active = self._loan_repo.find_by_status(LoanStatus.ACTIVE)

        for loan in all_active:
            if loan.is_overdue():
                loan.update_status()
                self._loan_repo.save(loan)
                overdue_loans.append(loan)

                self._event_bus.emit(
                    CirculationEvent(
                        event_type="overdue",
                        loan_id=loan.loan_id,
                        copy_barcode=loan.copy_barcode,
                        member_id=loan.member_id,
                        timestamp=datetime.now(),
                        details={
                            "days_overdue": loan.days_overdue(),
                            "due_date": loan.due_date.isoformat(),
                        },
                    )
                )

        return overdue_loans

    def get_loan_history(self, copy_barcode: str) -> list[Loan]:
        """Get loan history for a specific book copy."""
        return self._loan_repo.find_by_copy_barcode(copy_barcode)

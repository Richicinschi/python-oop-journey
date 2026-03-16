"""Loan domain entities - Loan and Reservation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import ClassVar, Self

from .enums import (
    CopyStatus,
    LoanStatus,
    ReservationStatus,
)


class DomainError(Exception):
    """Base exception for domain errors."""
    pass


class ValidationError(DomainError):
    """Raised when validation fails."""
    pass


class BusinessRuleError(DomainError):
    """Raised when a business rule is violated."""
    pass


@dataclass
class Loan:
    """A record of a book being borrowed by a member.

    Tracks the lifecycle of a borrowing transaction from checkout through
    return. Handles renewals, overdue detection, and status transitions.

    Attributes:
        loan_id: Unique identifier for this loan
        copy_barcode: Barcode of the borrowed copy
        member_id: ID of the borrowing member
        checkout_date: Date the book was checked out
        due_date: Date the book is due for return
        return_date: Date the book was returned (None if active)
        renewal_count: Number of times the loan has been renewed
        status: Current status of the loan

    Example:
        >>> from datetime import date
        >>> loan = Loan(
        ...     loan_id="LOAN001",
        ...     copy_barcode="CP001",
        ...     member_id="MEM001",
        ...     checkout_date=date(2024, 1, 1),
        ...     due_date=date(2024, 1, 15)
        ... )
        >>> loan.is_overdue(today=date(2024, 1, 20))
        True
    """

    loan_id: str
    copy_barcode: str
    member_id: str
    checkout_date: date
    due_date: date
    return_date: date | None = None
    renewal_count: int = 0
    status: LoanStatus = LoanStatus.ACTIVE

    # Class constants (not dataclass fields)
    MAX_RENEWALS: ClassVar[int] = 2
    LOAN_PERIOD_DAYS: ClassVar[int] = 14

    def __post_init__(self) -> None:
        """Validate loan data after initialization."""
        if not self.loan_id or not isinstance(self.loan_id, str):
            raise ValidationError("Loan ID must be a non-empty string")
        if not self.copy_barcode or not isinstance(self.copy_barcode, str):
            raise ValidationError("Copy barcode must be a non-empty string")
        if not self.member_id or not isinstance(self.member_id, str):
            raise ValidationError("Member ID must be a non-empty string")
        if not isinstance(self.checkout_date, date):
            raise ValidationError("Checkout date must be a date")
        if not isinstance(self.due_date, date):
            raise ValidationError("Due date must be a date")
        if self.due_date <= self.checkout_date:
            raise ValidationError("Due date must be after checkout date")
        if self.return_date is not None:
            if not isinstance(self.return_date, date):
                raise ValidationError("Return date must be a date or None")
            if self.return_date < self.checkout_date:
                raise ValidationError("Return date cannot be before checkout date")
        if not isinstance(self.renewal_count, int) or self.renewal_count < 0:
            raise ValidationError("Renewal count must be a non-negative integer")
        if not isinstance(self.status, LoanStatus):
            raise ValidationError(f"Invalid loan status: {self.status}")

    @classmethod
    def create(
        cls,
        loan_id: str,
        copy_barcode: str,
        member_id: str,
        checkout_date: date | None = None,
    ) -> Loan:
        """Factory method to create a new loan with calculated due date.

        Args:
            loan_id: Unique identifier for the loan.
            copy_barcode: Barcode of the book copy.
            member_id: ID of the borrowing member.
            checkout_date: Date of checkout (defaults to today).

        Returns:
            A new Loan instance with calculated due date.
        """
        checkout = checkout_date or date.today()
        due = checkout + timedelta(days=cls.LOAN_PERIOD_DAYS)
        return cls(
            loan_id=loan_id,
            copy_barcode=copy_barcode,
            member_id=member_id,
            checkout_date=checkout,
            due_date=due,
        )

    def is_overdue(self, today: date | None = None) -> bool:
        """Check if the loan is overdue.

        Args:
            today: The date to check against (defaults to today).

        Returns:
            True if the loan is active and past due date.
        """
        if self.status not in (LoanStatus.ACTIVE, LoanStatus.OVERDUE):
            return False
        check_date = today or date.today()
        return check_date > self.due_date

    def days_overdue(self, today: date | None = None) -> int:
        """Calculate days overdue.

        Args:
            today: The date to calculate from (defaults to today).

        Returns:
            Number of days overdue (0 if not overdue).
        """
        if not self.is_overdue(today):
            return 0
        check_date = today or date.today()
        return (check_date - self.due_date).days

    def can_renew(self, has_reservation: bool = False) -> bool:
        """Check if the loan can be renewed.

        Args:
            has_reservation: Whether the book has pending reservations.

        Returns:
            True if renewal is allowed:
            - Loan is active (not already overdue)
            - Renewal count is below maximum
            - Book has no pending reservations
        """
        if self.status != LoanStatus.ACTIVE:
            return False
        if self.renewal_count >= self.MAX_RENEWALS:
            return False
        if has_reservation:
            return False
        return True

    def renew(self, has_reservation: bool = False) -> Self:
        """Renew the loan, extending the due date.

        Args:
            has_reservation: Whether the book has pending reservations.

        Returns:
            Self for method chaining.

        Raises:
            BusinessRuleError: If renewal is not allowed.
        """
        if not self.can_renew(has_reservation):
            if self.status != LoanStatus.ACTIVE:
                raise BusinessRuleError(f"Cannot renew loan with status {self.status.value}")
            if self.renewal_count >= self.MAX_RENEWALS:
                raise BusinessRuleError(
                    f"Maximum renewals ({self.MAX_RENEWALS}) reached"
                )
            if has_reservation:
                raise BusinessRuleError("Cannot renew: book has pending reservations")
            raise BusinessRuleError("Cannot renew loan")

        self.due_date = self.due_date + timedelta(days=self.LOAN_PERIOD_DAYS)
        self.renewal_count += 1
        return self

    def return_book(self, return_date: date | None = None) -> Self:
        """Process the return of the borrowed book.

        Args:
            return_date: Date of return (defaults to today).

        Returns:
            Self for method chaining.

        Raises:
            BusinessRuleError: If loan is not active.
        """
        if self.status not in (LoanStatus.ACTIVE, LoanStatus.OVERDUE):
            raise BusinessRuleError(f"Cannot return loan with status {self.status.value}")

        self.return_date = return_date or date.today()
        self.status = LoanStatus.RETURNED
        return self

    def mark_as_lost(self) -> Self:
        """Mark the loan as lost.

        Returns:
            Self for method chaining.

        Raises:
            BusinessRuleError: If loan is not active.
        """
        if self.status not in (LoanStatus.ACTIVE, LoanStatus.OVERDUE):
            raise BusinessRuleError(f"Cannot mark as lost: loan is {self.status.value}")

        self.status = LoanStatus.LOST
        return self

    def update_status(self, today: date | None = None) -> Self:
        """Update loan status based on current date.

        Transitions ACTIVE loans to OVERDUE if past due date.

        Args:
            today: The current date (defaults to today).

        Returns:
            Self for method chaining.
        """
        if self.status == LoanStatus.ACTIVE and self.is_overdue(today):
            self.status = LoanStatus.OVERDUE
        return self

    @property
    def is_active(self) -> bool:
        """Check if loan is currently active.

        Returns:
            True if status is ACTIVE or OVERDUE.
        """
        return self.status in (LoanStatus.ACTIVE, LoanStatus.OVERDUE)

    def days_remaining(self, today: date | None = None) -> int:
        """Calculate days remaining until due.

        Args:
            today: The date to calculate from (defaults to today).

        Returns:
            Days remaining (negative if overdue, 0 if returned).
        """
        if self.status == LoanStatus.RETURNED:
            return 0
        check_date = today or date.today()
        return (self.due_date - check_date).days


@dataclass
class Reservation:
    """A member's request to borrow a book when it becomes available.

    Reservations are placed on books (not specific copies) and are
    fulfilled in FIFO order when any copy becomes available.

    Attributes:
        reservation_id: Unique identifier for this reservation
        book_isbn: ISBN of the requested book
        member_id: ID of the requesting member
        reservation_date: Date and time the reservation was placed
        expiry_date: Date when the reservation expires (if fulfilled)
        status: Current status of the reservation
        queue_position: Position in the FIFO queue (None if fulfilled)

    Example:
        >>> from datetime import datetime
        >>> reservation = Reservation(
        ...     reservation_id="RES001",
        ...     book_isbn="978-0-123456-78-9",
        ...     member_id="MEM001",
        ...     reservation_date=datetime.now(),
        ...     queue_position=1
        ... )
    """

    reservation_id: str
    book_isbn: str
    member_id: str
    reservation_date: datetime
    expiry_date: date | None = None
    status: ReservationStatus = ReservationStatus.PENDING
    queue_position: int | None = None

    # Class constants (not dataclass fields)
    HOLD_PERIOD_DAYS: ClassVar[int] = 3

    def __post_init__(self) -> None:
        """Validate reservation data after initialization."""
        if not self.reservation_id or not isinstance(self.reservation_id, str):
            raise ValidationError("Reservation ID must be a non-empty string")
        if not self.book_isbn or not isinstance(self.book_isbn, str):
            raise ValidationError("Book ISBN must be a non-empty string")
        if not self.member_id or not isinstance(self.member_id, str):
            raise ValidationError("Member ID must be a non-empty string")
        if not isinstance(self.reservation_date, datetime):
            raise ValidationError("Reservation date must be a datetime")
        if self.expiry_date is not None and not isinstance(self.expiry_date, date):
            raise ValidationError("Expiry date must be a date or None")
        if not isinstance(self.status, ReservationStatus):
            raise ValidationError(f"Invalid reservation status: {self.status}")
        if self.queue_position is not None and (
            not isinstance(self.queue_position, int) or self.queue_position < 1
        ):
            raise ValidationError("Queue position must be a positive integer or None")

    @classmethod
    def create(
        cls,
        reservation_id: str,
        book_isbn: str,
        member_id: str,
        queue_position: int,
    ) -> Reservation:
        """Factory method to create a new reservation.

        Args:
            reservation_id: Unique identifier for the reservation.
            book_isbn: ISBN of the book to reserve.
            member_id: ID of the requesting member.
            queue_position: Position in the reservation queue.

        Returns:
            A new Reservation instance.
        """
        return cls(
            reservation_id=reservation_id,
            book_isbn=book_isbn,
            member_id=member_id,
            reservation_date=datetime.now(),
            queue_position=queue_position,
            status=ReservationStatus.PENDING,
        )

    def fulfill(self, hold_until: date | None = None) -> Self:
        """Mark the reservation as fulfilled.

        Called when a copy becomes available for this member.

        Args:
            hold_until: Date until which the book is held
                       (defaults to HOLD_PERIOD_DAYS from today).

        Returns:
            Self for method chaining.

        Raises:
            BusinessRuleError: If reservation is not pending.
        """
        if self.status != ReservationStatus.PENDING:
            raise BusinessRuleError(
                f"Cannot fulfill reservation with status {self.status.value}"
            )

        self.status = ReservationStatus.FULFILLED
        self.queue_position = None
        self.expiry_date = hold_until or (date.today() + timedelta(days=self.HOLD_PERIOD_DAYS))
        return self

    def cancel(self) -> Self:
        """Cancel the reservation.

        Returns:
            Self for method chaining.

        Raises:
            BusinessRuleError: If reservation is already fulfilled or expired.
        """
        if self.status in (ReservationStatus.FULFILLED, ReservationStatus.EXPIRED):
            raise BusinessRuleError(f"Cannot cancel {self.status.value} reservation")

        self.status = ReservationStatus.CANCELLED
        self.queue_position = None
        return self

    def expire(self) -> Self:
        """Mark the reservation as expired.

        Called when the hold period expires without pickup.

        Returns:
            Self for method chaining.
        """
        self.status = ReservationStatus.EXPIRED
        self.queue_position = None
        return self

    def is_expired(self, today: date | None = None) -> bool:
        """Check if the fulfilled reservation has expired.

        Args:
            today: The date to check against (defaults to today).

        Returns:
            True if fulfilled and past expiry date.
        """
        if self.status != ReservationStatus.FULFILLED:
            return False
        if self.expiry_date is None:
            return False
        check_date = today or date.today()
        return check_date > self.expiry_date

    def update_queue_position(self, new_position: int) -> Self:
        """Update the position in the reservation queue.

        Args:
            new_position: The new queue position.

        Returns:
            Self for method chaining.

        Raises:
            BusinessRuleError: If reservation is not pending.
        """
        if self.status != ReservationStatus.PENDING:
            raise BusinessRuleError("Cannot update queue position for non-pending reservation")
        if new_position < 1:
            raise ValidationError("Queue position must be positive")

        self.queue_position = new_position
        return self

    @property
    def is_pending(self) -> bool:
        """Check if reservation is pending.

        Returns:
            True if status is PENDING.
        """
        return self.status == ReservationStatus.PENDING

    @property
    def is_fulfilled(self) -> bool:
        """Check if reservation is fulfilled.

        Returns:
            True if status is FULFILLED.
        """
        return self.status == ReservationStatus.FULFILLED

    def wait_time_days(self, today: date | None = None) -> int:
        """Calculate days since reservation was placed.

        Args:
            today: The date to calculate from (defaults to today).

        Returns:
            Number of days waiting.
        """
        check_date = today or date.today()
        return (check_date - self.reservation_date.date()).days

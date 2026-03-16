"""Fine value object for the Library Management System."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import ClassVar, Self

from .enums import FineStatus


class DomainError(Exception):
    """Base exception for domain errors."""
    pass


class ValidationError(DomainError):
    """Raised when validation fails."""
    pass


class BusinessRuleError(DomainError):
    """Raised when a business rule is violated."""
    pass


@dataclass(frozen=True)
class Fine:
    """A monetary penalty for overdue books.

    Fine is a value object (immutable) representing a penalty assessed
    to a member for returning a book late. Once created, the amount
    cannot be changed, only the payment status.

    Attributes:
        fine_id: Unique identifier for this fine
        loan_id: ID of the associated loan
        member_id: ID of the member being fined
        amount: The fine amount (always non-negative)
        reason: Description of the violation
        issued_date: Date the fine was assessed
        paid_date: Date the fine was paid (None if outstanding)
        status: Current payment status

    Example:
        >>> from decimal import Decimal
        >>> fine = Fine(
        ...     fine_id="FINE001",
        ...     loan_id="LOAN001",
        ...     member_id="MEM001",
        ...     amount=Decimal("5.00"),
        ...     reason="Overdue by 10 days"
        ... )
        >>> fine.pay(Decimal("5.00"))
        Decimal('0.00')
    """

    fine_id: str
    loan_id: str
    member_id: str
    amount: Decimal
    reason: str
    issued_date: date = field(default_factory=date.today)
    paid_date: date | None = None
    status: FineStatus = FineStatus.OUTSTANDING

    # Class constants (not dataclass fields)
    MAX_FINE_PER_BOOK: ClassVar[Decimal] = Decimal("20.00")

    def __post_init__(self) -> None:
        """Validate fine data after initialization."""
        # Since the class is frozen, we need to use object.__setattr__ for validation
        if not self.fine_id or not isinstance(self.fine_id, str):
            object.__setattr__(
                self, "_validation_error", "Fine ID must be a non-empty string"
            )
            raise ValidationError("Fine ID must be a non-empty string")
        if not self.loan_id or not isinstance(self.loan_id, str):
            raise ValidationError("Loan ID must be a non-empty string")
        if not self.member_id or not isinstance(self.member_id, str):
            raise ValidationError("Member ID must be a non-empty string")
        if not isinstance(self.amount, Decimal):
            try:
                object.__setattr__(self, "amount", Decimal(str(self.amount)))
            except InvalidOperation:
                raise ValidationError("Amount must be a valid decimal number")
        if self.amount < Decimal("0"):
            raise ValidationError("Fine amount cannot be negative")
        if self.amount > self.MAX_FINE_PER_BOOK:
            raise ValidationError(
                f"Fine amount cannot exceed maximum of ${self.MAX_FINE_PER_BOOK}"
            )
        if not self.reason or not isinstance(self.reason, str):
            raise ValidationError("Reason must be a non-empty string")
        if not isinstance(self.issued_date, date):
            raise ValidationError("Issued date must be a date")
        if self.paid_date is not None:
            if not isinstance(self.paid_date, date):
                raise ValidationError("Paid date must be a date or None")
            if self.paid_date < self.issued_date:
                raise ValidationError("Paid date cannot be before issued date")
        if not isinstance(self.status, FineStatus):
            raise ValidationError(f"Invalid fine status: {self.status}")

    @classmethod
    def create(
        cls,
        fine_id: str,
        loan_id: str,
        member_id: str,
        days_overdue: int,
        daily_rate: Decimal = Decimal("0.50"),
        reason: str | None = None,
    ) -> Fine:
        """Factory method to create a fine with calculated amount.

        Args:
            fine_id: Unique identifier for the fine.
            loan_id: ID of the associated loan.
            member_id: ID of the member being fined.
            days_overdue: Number of days the book was overdue.
            daily_rate: Fine amount per day (default $0.50).
            reason: Optional custom reason message.

        Returns:
            A new Fine instance with calculated amount.
        """
        calculated_amount = min(
            Decimal(days_overdue) * daily_rate,
            cls.MAX_FINE_PER_BOOK,
        )
        default_reason = f"Overdue by {days_overdue} days"
        return cls(
            fine_id=fine_id,
            loan_id=loan_id,
            member_id=member_id,
            amount=calculated_amount,
            reason=reason or default_reason,
        )

    def pay(self, amount: Decimal) -> Decimal:
        """Record a payment towards this fine.

        This method returns a new Fine with updated status rather than
        modifying the current instance (value object immutability).

        Args:
            amount: The amount being paid.

        Returns:
            The remaining balance after payment.

        Raises:
            BusinessRuleError: If fine is already paid or waived.
            ValidationError: If payment amount is invalid.
        """
        if not isinstance(amount, Decimal):
            try:
                amount = Decimal(str(amount))
            except InvalidOperation:
                raise ValidationError("Payment amount must be a valid decimal")

        if amount <= Decimal("0"):
            raise ValidationError("Payment amount must be positive")

        if self.status == FineStatus.PAID:
            raise BusinessRuleError("Fine is already paid in full")
        if self.status == FineStatus.WAIVED:
            raise BusinessRuleError("Fine has been waived")

        if amount >= self.amount:
            # Full payment - return new paid fine
            return Decimal("0.00")
        else:
            # Partial payment - this would require mutable state or a new fine
            # For simplicity in this domain model, we only support full payment
            raise BusinessRuleError(
                f"Payment amount ${amount} is less than fine amount ${self.amount}. "
                "Full payment required."
            )

    def mark_as_paid(self, paid_date: date | None = None) -> Fine:
        """Create a new Fine marked as paid.

        Args:
            paid_date: Date of payment (defaults to today).

        Returns:
            A new Fine with PAID status.

        Raises:
            BusinessRuleError: If fine is already paid or waived.
        """
        if self.status != FineStatus.OUTSTANDING:
            raise BusinessRuleError(f"Cannot mark {self.status.value} fine as paid")

        # Create new Fine with updated status (immutable)
        return Fine(
            fine_id=self.fine_id,
            loan_id=self.loan_id,
            member_id=self.member_id,
            amount=self.amount,
            reason=self.reason,
            issued_date=self.issued_date,
            paid_date=paid_date or date.today(),
            status=FineStatus.PAID,
        )

    def waive(self, waived_by: str) -> Fine:
        """Create a new Fine marked as waived.

        Args:
            waived_by: Identifier of the librarian waiving the fine.

        Returns:
            A new Fine with WAIVED status.

        Raises:
            BusinessRuleError: If fine is already paid or waived.
        """
        if self.status != FineStatus.OUTSTANDING:
            raise BusinessRuleError(f"Cannot waive {self.status.value} fine")

        return Fine(
            fine_id=self.fine_id,
            loan_id=self.loan_id,
            member_id=self.member_id,
            amount=self.amount,
            reason=f"{self.reason} (waived by {waived_by})",
            issued_date=self.issued_date,
            paid_date=None,
            status=FineStatus.WAIVED,
        )

    @property
    def is_outstanding(self) -> bool:
        """Check if fine is outstanding.

        Returns:
            True if status is OUTSTANDING.
        """
        return self.status == FineStatus.OUTSTANDING

    @property
    def is_paid(self) -> bool:
        """Check if fine is paid.

        Returns:
            True if status is PAID.
        """
        return self.status == FineStatus.PAID

    @property
    def is_waived(self) -> bool:
        """Check if fine is waived.

        Returns:
            True if status is WAIVED.
        """
        return self.status == FineStatus.WAIVED

    def __eq__(self, other: object) -> bool:
        """Equality based on fine_id and amount.

        Args:
            other: The other object to compare.

        Returns:
            True if equal.
        """
        if not isinstance(other, Fine):
            return NotImplemented
        return (
            self.fine_id == other.fine_id
            and self.amount == other.amount
            and self.status == other.status
        )

    def __hash__(self) -> int:
        """Hash based on fine_id.

        Returns:
            Hash value.
        """
        return hash(self.fine_id)

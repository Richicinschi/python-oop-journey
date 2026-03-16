"""Member domain entities - Member and Librarian."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal
from typing import ClassVar, Self

from .enums import (
    Condition,
    CopyStatus,
    FineStatus,
    LoanStatus,
    MembershipStatus,
    StaffRole,
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
class Member:
    """A library member with borrowing privileges.

    Members can borrow books, place reservations, and pay fines. Their
    borrowing privileges depend on their membership status and current
    obligations.

    Attributes:
        member_id: Unique identifier for the member
        name: Full name of the member
        email: Contact email address (unique)
        phone: Contact phone number (optional)
        address: Physical address (optional)
        registration_date: Date of membership registration
        status: Current membership status
        _active_loans: List of currently active loans
        _fines: List of all fines (outstanding and paid)

    Example:
        >>> member = Member(
        ...     member_id="MEM001",
        ...     name="Alice Johnson",
        ...     email="alice@example.com"
        ... )
        >>> member.can_borrow()
        True
    """

    member_id: str
    name: str
    email: str
    phone: str | None = None
    address: str | None = None
    registration_date: date = field(default_factory=date.today)
    status: MembershipStatus = MembershipStatus.ACTIVE
    _active_loans: list = field(default_factory=list, repr=False)
    _fines: list = field(default_factory=list, repr=False)

    # Class constants (not dataclass fields)
    MAX_ACTIVE_LOANS: ClassVar[int] = 5
    FINE_THRESHOLD: ClassVar[Decimal] = Decimal("20.00")
    MEMBERSHIP_DURATION_DAYS: ClassVar[int] = 365

    def __post_init__(self) -> None:
        """Validate member data after initialization."""
        if not self.member_id or not isinstance(self.member_id, str):
            raise ValidationError("Member ID must be a non-empty string")
        if not self.name or not isinstance(self.name, str):
            raise ValidationError("Name must be a non-empty string")
        if not self.email or not isinstance(self.email, str):
            raise ValidationError("Email must be a non-empty string")
        if "@" not in self.email:
            raise ValidationError(f"Invalid email format: {self.email}")
        if not isinstance(self.status, MembershipStatus):
            raise ValidationError(f"Invalid membership status: {self.status}")

    @property
    def active_loan_count(self) -> int:
        """Get the number of active loans.

        Returns:
            Count of loans with ACTIVE or OVERDUE status.
        """
        return len(self._active_loans)

    @property
    def outstanding_fines(self) -> list:
        """Get all outstanding fines.

        Returns:
            List of fines with OUTSTANDING status.
        """
        return [f for f in self._fines if f.status == FineStatus.OUTSTANDING]

    @property
    def total_outstanding_fines(self) -> Decimal:
        """Get total amount of outstanding fines.

        Returns:
            Sum of all outstanding fine amounts.
        """
        return sum(
            (f.amount for f in self._fines if f.status == FineStatus.OUTSTANDING),
            Decimal("0.00"),
        )

    @property
    def has_overdue_loans(self) -> bool:
        """Check if member has any overdue loans.

        Returns:
            True if any loan is overdue.
        """
        from .loan import LoanStatus
        return any(
            loan.status == LoanStatus.OVERDUE for loan in self._active_loans
        )

    def can_borrow(self) -> bool:
        """Check if member is eligible to borrow books.

        Returns:
            True if all borrowing criteria are met:
            - Membership status is ACTIVE
            - Active loans below maximum
            - No outstanding fines above threshold
            - No overdue loans
        """
        if self.status != MembershipStatus.ACTIVE:
            return False
        if self.active_loan_count >= self.MAX_ACTIVE_LOANS:
            return False
        if self.total_outstanding_fines > self.FINE_THRESHOLD:
            return False
        if self.has_overdue_loans:
            return False
        return True

    def can_reserve(self) -> bool:
        """Check if member can place reservations.

        Returns:
            True if member status is not SUSPENDED or EXPIRED.
        """
        return self.status == MembershipStatus.ACTIVE

    def add_loan(self, loan) -> Self:
        """Add an active loan to this member.

        Args:
            loan: The Loan to add.

        Returns:
            Self for method chaining.

        Raises:
            BusinessRuleError: If member cannot borrow.
        """
        if not self.can_borrow():
            raise BusinessRuleError("Member cannot borrow books at this time")
        self._active_loans.append(loan)
        return self

    def remove_loan(self, loan_id: str):
        """Remove a loan by ID (when returned).

        Args:
            loan_id: The ID of the loan to remove.

        Returns:
            The removed loan.

        Raises:
            ValidationError: If loan not found.
        """
        for i, loan in enumerate(self._active_loans):
            if loan.loan_id == loan_id:
                return self._active_loans.pop(i)
        raise ValidationError(f"Loan {loan_id} not found")

    def add_fine(self, fine) -> Self:
        """Add a fine to this member's record.

        Args:
            fine: The Fine to add.

        Returns:
            Self for method chaining.
        """
        self._fines.append(fine)
        # Suspend member if fines exceed threshold
        if self.total_outstanding_fines > self.FINE_THRESHOLD:
            self.status = MembershipStatus.SUSPENDED
        return self

    def pay_fine(self, fine_id: str, amount: Decimal) -> Decimal:
        """Pay towards a fine.

        Args:
            fine_id: The ID of the fine to pay.
            amount: The amount to pay.

        Returns:
            The remaining balance on the fine.

        Raises:
            ValidationError: If fine not found or already paid.
        """
        for fine in self._fines:
            if fine.fine_id == fine_id:
                remaining = fine.pay(amount)
                # Reactivate member if no longer over threshold
                if (
                    self.status == MembershipStatus.SUSPENDED
                    and self.total_outstanding_fines <= self.FINE_THRESHOLD
                    and not self.has_overdue_loans
                ):
                    self.status = MembershipStatus.ACTIVE
                return remaining
        raise ValidationError(f"Fine {fine_id} not found")

    def get_active_loan(self, loan_id: str):
        """Get an active loan by ID.

        Args:
            loan_id: The loan ID to find.

        Returns:
            The loan if found, None otherwise.
        """
        for loan in self._active_loans:
            if loan.loan_id == loan_id:
                return loan
        return None

    def is_membership_expired(self) -> bool:
        """Check if membership has expired due to inactivity.

        Returns:
            True if membership has expired.
        """
        expiry_date = self.registration_date + timedelta(
            days=self.MEMBERSHIP_DURATION_DAYS
        )
        return date.today() > expiry_date

    def renew_membership(self) -> Self:
        """Renew the membership for another year.

        Returns:
            Self for method chaining.
        """
        self.registration_date = date.today()
        if self.status == MembershipStatus.EXPIRED:
            self.status = MembershipStatus.ACTIVE
        return self

    def suspend(self, reason: str = "") -> Self:
        """Suspend the member's borrowing privileges.

        Args:
            reason: Optional reason for suspension.

        Returns:
            Self for method chaining.
        """
        self.status = MembershipStatus.SUSPENDED
        return self

    def activate(self) -> Self:
        """Activate the member (if eligible).

        Returns:
            Self for method chaining.

        Raises:
            BusinessRuleError: If member has blocking conditions.
        """
        if self.has_overdue_loans:
            raise BusinessRuleError("Cannot activate: member has overdue loans")
        if self.total_outstanding_fines > self.FINE_THRESHOLD:
            raise BusinessRuleError("Cannot activate: member has excessive fines")
        self.status = MembershipStatus.ACTIVE
        return self


@dataclass
class Librarian:
    """A library staff member with administrative privileges.

    Librarians can check out and check in books, manage member accounts,
    and perform other administrative tasks based on their role.

    Attributes:
        staff_id: Unique identifier for the staff member
        name: Full name
        email: Contact email address
        role: Staff role level
        permissions: Set of granted permissions
        hire_date: Date of employment

    Example:
        >>> librarian = Librarian(
        ...     staff_id="LIB001",
        ...     name="Bob Smith",
        ...     email="bob@library.org",
        ...     role=StaffRole.LIBRARIAN
        ... )
        >>> librarian.can_checkout()
        True
    """

    staff_id: str
    name: str
    email: str
    role: StaffRole = StaffRole.ASSISTANT
    permissions: set[str] = field(default_factory=set)
    hire_date: date = field(default_factory=date.today)

    # Role-based default permissions
    ROLE_PERMISSIONS: dict[StaffRole, set[str]] = field(
        default_factory=lambda: {
            StaffRole.ASSISTANT: {"checkout", "checkin", "view_member"},
            StaffRole.LIBRARIAN: {
                "checkout",
                "checkin",
                "view_member",
                "edit_member",
                "manage_catalog",
                "waive_fine",
            },
            StaffRole.MANAGER: {
                "checkout",
                "checkin",
                "view_member",
                "edit_member",
                "manage_catalog",
                "waive_fine",
                "generate_reports",
                "manage_staff",
                "configure_system",
            },
        },
        repr=False,
    )

    def __post_init__(self) -> None:
        """Validate librarian data and set default permissions."""
        if not self.staff_id or not isinstance(self.staff_id, str):
            raise ValidationError("Staff ID must be a non-empty string")
        if not self.name or not isinstance(self.name, str):
            raise ValidationError("Name must be a non-empty string")
        if not self.email or not isinstance(self.email, str):
            raise ValidationError("Email must be a non-empty string")
        if "@" not in self.email:
            raise ValidationError(f"Invalid email format: {self.email}")
        if not isinstance(self.role, StaffRole):
            raise ValidationError(f"Invalid staff role: {self.role}")
        # Initialize permissions based on role if not explicitly set
        if not self.permissions:
            self.permissions = self.ROLE_PERMISSIONS.get(self.role, set()).copy()

    def has_permission(self, permission: str) -> bool:
        """Check if librarian has a specific permission.

        Args:
            permission: The permission to check.

        Returns:
            True if the permission is granted.
        """
        return permission in self.permissions

    def can_checkout(self) -> bool:
        """Check if librarian can check out books.

        Returns:
            True if has checkout permission.
        """
        return self.has_permission("checkout")

    def can_checkin(self) -> bool:
        """Check if librarian can check in books.

        Returns:
            True if has checkin permission.
        """
        return self.has_permission("checkin")

    def can_manage_members(self) -> bool:
        """Check if librarian can manage member accounts.

        Returns:
            True if has edit_member permission.
        """
        return self.has_permission("edit_member")

    def can_manage_catalog(self) -> bool:
        """Check if librarian can manage book catalog.

        Returns:
            True if has manage_catalog permission.
        """
        return self.has_permission("manage_catalog")

    def can_waive_fines(self) -> bool:
        """Check if librarian can waive fines.

        Returns:
            True if has waive_fine permission.
        """
        return self.has_permission("waive_fine")

    def can_generate_reports(self) -> bool:
        """Check if librarian can generate reports.

        Returns:
            True if has generate_reports permission.
        """
        return self.has_permission("generate_reports")

    def grant_permission(self, permission: str) -> Self:
        """Grant an additional permission.

        Args:
            permission: The permission to grant.

        Returns:
            Self for method chaining.
        """
        self.permissions.add(permission)
        return self

    def revoke_permission(self, permission: str) -> Self:
        """Revoke a permission.

        Args:
            permission: The permission to revoke.

        Returns:
            Self for method chaining.
        """
        self.permissions.discard(permission)
        return self

    def promote(self, new_role: StaffRole) -> Self:
        """Promote to a new role.

        Args:
            new_role: The new role to assign.

        Returns:
            Self for method chaining.
        """
        self.role = new_role
        self.permissions = self.ROLE_PERMISSIONS.get(new_role, set()).copy()
        return self

"""Fine service with Strategy pattern for fine calculation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from ..domain.loan import Loan
from ..domain.member import Member
from ..repositories.loan_repository import LoanRepository
from ..repositories.member_repository import MemberRepository


@dataclass
class FineBreakdown:
    """Detailed breakdown of a fine calculation."""

    base_amount: Decimal
    grace_period_discount: Decimal
    processing_fee: Decimal
    total_amount: Decimal
    days_overdue: int
    chargeable_days: int


class FineCalculationStrategy(ABC):
    """Abstract strategy for fine calculation.

    Strategy Pattern: Allows different fine calculation algorithms
    for different member types or book categories.
    """

    @abstractmethod
    def calculate(
        self,
        loan: Loan,
        daily_rate: Decimal = Decimal("1.00"),
        grace_period_days: int = 1,
        max_fine: Decimal = Decimal("50.00"),
        current_date: Optional[date] = None,
    ) -> FineBreakdown:
        """Calculate fine for a loan."""
        raise NotImplementedError


class StandardFineStrategy(FineCalculationStrategy):
    """Standard fine calculation with grace period and caps."""

    def calculate(
        self,
        loan: Loan,
        daily_rate: Decimal = Decimal("1.00"),
        grace_period_days: int = 1,
        max_fine: Decimal = Decimal("50.00"),
        current_date: Optional[date] = None,
    ) -> FineBreakdown:
        """Calculate fine using standard rules."""
        if current_date is None:
            current_date = date.today()

        days_overdue = loan.days_overdue(current_date)
        chargeable_days = max(0, days_overdue - grace_period_days)

        base_amount = Decimal(chargeable_days) * daily_rate
        grace_discount = (
            Decimal(grace_period_days) * daily_rate
            if days_overdue > 0
            else Decimal("0.00")
        )

        subtotal = base_amount
        processing_fee = Decimal("5.00") if days_overdue > 0 else Decimal("0.00")
        total = min(subtotal + processing_fee, max_fine)

        return FineBreakdown(
            base_amount=base_amount,
            grace_period_discount=grace_discount,
            processing_fee=processing_fee,
            total_amount=total,
            days_overdue=days_overdue,
            chargeable_days=chargeable_days,
        )


class ForgivingFineStrategy(FineCalculationStrategy):
    """More lenient fine calculation for students or special members."""

    def __init__(self, discount_percentage: float = 0.5) -> None:
        self.discount_percentage = discount_percentage

    def calculate(
        self,
        loan: Loan,
        daily_rate: Decimal = Decimal("1.00"),
        grace_period_days: int = 1,
        max_fine: Decimal = Decimal("50.00"),
        current_date: Optional[date] = None,
    ) -> FineBreakdown:
        """Calculate fine with discount applied."""
        if current_date is None:
            current_date = date.today()

        days_overdue = loan.days_overdue(current_date)
        # Longer grace period
        effective_grace = grace_period_days + 2
        chargeable_days = max(0, days_overdue - effective_grace)

        base_amount = Decimal(chargeable_days) * daily_rate * Decimal(1 - self.discount_percentage)

        return FineBreakdown(
            base_amount=base_amount,
            grace_period_discount=Decimal("0.00"),
            processing_fee=Decimal("0.00"),  # No processing fee for forgiving policy
            total_amount=base_amount,
            days_overdue=days_overdue,
            chargeable_days=chargeable_days,
        )


class FineService:
    """Service for managing fines and payments.

    Uses Strategy Pattern for flexible fine calculation.
    """

    def __init__(
        self,
        member_repository: MemberRepository,
        loan_repository: LoanRepository,
        default_strategy: Optional[FineCalculationStrategy] = None,
    ) -> None:
        self._member_repo = member_repository
        self._loan_repo = loan_repository
        self._default_strategy = default_strategy or StandardFineStrategy()
        self._strategies: dict[str, FineCalculationStrategy] = {
            "standard": StandardFineStrategy(),
            "forgiving": ForgivingFineStrategy(),
        }
        self._member_strategies: dict[str, str] = {}  # member_id -> strategy_name

    def set_member_strategy(self, member_id: str, strategy_name: str) -> bool:
        """Assign a fine calculation strategy to a member."""
        if strategy_name not in self._strategies:
            return False
        self._member_strategies[member_id] = strategy_name
        return True

    def calculate_fine(
        self,
        loan: Loan,
        strategy_name: Optional[str] = None,
        current_date: Optional[date] = None,
    ) -> FineBreakdown:
        """Calculate fine for a loan using appropriate strategy."""
        # Determine strategy
        if strategy_name is None:
            strategy_name = self._member_strategies.get(loan.member_id, "standard")

        strategy = self._strategies.get(strategy_name, StandardFineStrategy())

        return strategy.calculate(loan, current_date=current_date)

    def process_payment(
        self,
        member_id: str,
        fine_id: str,
        amount: Decimal,
    ) -> tuple[bool, str, Decimal]:
        """Process a fine payment from a member.

        Returns:
            Tuple of (success, message, remaining_balance)
        """
        member = self._member_repo.find_by_id(member_id)
        if not member:
            return False, "Member not found", Decimal("0.00")

        if amount <= 0:
            return False, "Payment amount must be positive", Decimal("0.00")

        try:
            remaining = member.pay_fine(fine_id, amount)
            self._member_repo.save(member)
            return (
                True,
                f"Payment processed. Remaining balance: ${remaining:.2f}",
                remaining,
            )
        except Exception as e:
            return False, str(e), Decimal("0.00")

    def get_member_fines(self, member_id: str) -> list:
        """Get all fines for a member.

        Returns:
            List of Fine objects
        """
        member = self._member_repo.find_by_id(member_id)
        if not member:
            return []
        return member.outstanding_fines

    def get_total_outstanding_fines(self, member_id: str) -> Decimal:
        """Get total outstanding fines for a member."""
        member = self._member_repo.find_by_id(member_id)
        if not member:
            return Decimal("0.00")
        return member.total_outstanding_fines

    def get_fine_statistics(self) -> dict:
        """Get statistics about fines in the system."""
        members = self._member_repo.get_all()

        total_outstanding = sum(m.total_outstanding_fines for m in members)
        members_with_fines = sum(1 for m in members if m.total_outstanding_fines > 0)

        return {
            "total_outstanding_fines": float(total_outstanding),
            "members_with_fines": members_with_fines,
            "average_fine_per_member": (
                float(total_outstanding) / members_with_fines
                if members_with_fines > 0
                else 0.0
            ),
        }

    def register_strategy(
        self, name: str, strategy: FineCalculationStrategy
    ) -> None:
        """Register a custom fine calculation strategy."""
        self._strategies[name] = strategy

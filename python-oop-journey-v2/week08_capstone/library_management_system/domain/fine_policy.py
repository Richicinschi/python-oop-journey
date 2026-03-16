"""Fine policy configuration."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class FinePolicy:
    """Configuration for fine calculation policies.

    Allows different fine rates for different member types or book categories.
    """

    name: str
    daily_rate: float = 1.0
    grace_period_days: int = 1
    max_fine_per_loan: float = 50.0
    lost_book_fee: float = 100.0
    damage_fee_light: float = 10.0
    damage_fee_severe: float = 50.0
    processing_fee: float = 5.0

    def calculate_overdue_fine(self, days_overdue: int) -> float:
        """Calculate fine for overdue book.

        Args:
            days_overdue: Number of days the book is overdue

        Returns:
            Calculated fine amount
        """
        if days_overdue <= self.grace_period_days:
            return 0.0

        chargeable_days = days_overdue - self.grace_period_days
        fine = chargeable_days * self.daily_rate
        return min(fine, self.max_fine_per_loan)

    def calculate_lost_book_fee(self, book_value: Optional[float] = None) -> float:
        """Calculate fee for lost book.

        Args:
            book_value: Optional replacement value of the book

        Returns:
            Calculated lost book fee
        """
        if book_value:
            return min(book_value + self.processing_fee, self.lost_book_fee * 2)
        return self.lost_book_fee

    def calculate_damage_fee(self, severity: str = "light") -> float:
        """Calculate fee for damaged book.

        Args:
            severity: Either 'light' or 'severe'

        Returns:
            Calculated damage fee
        """
        if severity == "severe":
            return self.damage_fee_severe
        return self.damage_fee_light

    @classmethod
    def standard_policy(cls) -> FinePolicy:
        """Create standard fine policy."""
        return cls(
            name="Standard",
            daily_rate=1.0,
            grace_period_days=1,
            max_fine_per_loan=50.0,
            lost_book_fee=100.0,
        )

    @classmethod
    def student_policy(cls) -> FinePolicy:
        """Create student-friendly fine policy with lower rates."""
        return cls(
            name="Student",
            daily_rate=0.5,
            grace_period_days=3,
            max_fine_per_loan=25.0,
            lost_book_fee=75.0,
        )

    @classmethod
    def premium_policy(cls) -> FinePolicy:
        """Create premium policy (for special collections)."""
        return cls(
            name="Premium",
            daily_rate=5.0,
            grace_period_days=0,
            max_fine_per_loan=200.0,
            lost_book_fee=500.0,
            damage_fee_light=25.0,
            damage_fee_severe=100.0,
        )

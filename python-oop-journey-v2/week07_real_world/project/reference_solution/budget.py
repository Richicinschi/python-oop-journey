"""Budget management module.

Domain model for tracking spending budgets by category.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum, auto
from typing import Optional
import calendar
import uuid


class BudgetPeriod(Enum):
    """Budget period types."""
    WEEKLY = auto()
    MONTHLY = auto()
    QUARTERLY = auto()
    YEARLY = auto()


@dataclass
class Budget:
    """Represents a spending budget for a category.
    
    A budget sets a spending limit for a specific category over
    a defined time period.
    
    Attributes:
        id: Unique budget identifier
        category_id: ID of the category being budgeted
        amount: Budget limit amount
        period: Time period for the budget
        start_date: When the budget period starts
        alert_threshold: Percentage (0-100) at which to alert
        is_active: Whether the budget is currently active
        created_at: Timestamp when budget was created
    """
    
    category_id: str
    amount: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    period: BudgetPeriod = BudgetPeriod.MONTHLY
    start_date: date = field(default_factory=date.today)
    alert_threshold: float = 80.0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """Validate budget after creation."""
        if self.amount <= 0:
            raise ValueError("Budget amount must be positive")
        if not 0 <= self.alert_threshold <= 100:
            raise ValueError("Alert threshold must be between 0 and 100")
        if not self.category_id:
            raise ValueError("Category ID is required")
    
    def get_period_dates(self) -> tuple[date, date]:
        """Calculate the start and end dates for the current period.
        
        Returns:
            Tuple of (period_start, period_end)
        """
        if self.period == BudgetPeriod.WEEKLY:
            days_since_start = (date.today() - self.start_date).days % 7
            period_start = date.today() - timedelta(days=days_since_start)
            period_end = period_start + timedelta(days=6)
        
        elif self.period == BudgetPeriod.MONTHLY:
            today = date.today()
            period_start = date(today.year, today.month, 1)
            last_day = calendar.monthrange(today.year, today.month)[1]
            period_end = date(today.year, today.month, last_day)
        
        elif self.period == BudgetPeriod.QUARTERLY:
            today = date.today()
            quarter = (today.month - 1) // 3
            period_start = date(today.year, quarter * 3 + 1, 1)
            if quarter == 3:
                period_end = date(today.year, 12, 31)
            else:
                period_end = date(today.year, (quarter + 1) * 3 + 1, 1) - timedelta(days=1)
        
        elif self.period == BudgetPeriod.YEARLY:
            today = date.today()
            period_start = date(today.year, 1, 1)
            period_end = date(today.year, 12, 31)
        
        else:
            period_start = self.start_date
            period_end = self.start_date + timedelta(days=30)
        
        return period_start, period_end
    
    def is_alert_triggered(self, spent_amount: float) -> bool:
        """Check if spending has exceeded the alert threshold.
        
        Args:
            spent_amount: Amount spent so far in the period
            
        Returns:
            True if alert should be triggered
        """
        if self.amount <= 0:
            return False
        utilization = (spent_amount / self.amount) * 100
        return utilization >= self.alert_threshold
    
    def get_remaining(self, spent_amount: float) -> float:
        """Calculate remaining budget.
        
        Args:
            spent_amount: Amount spent so far
            
        Returns:
            Remaining budget (can be negative if over budget)
        """
        return self.amount - spent_amount
    
    def get_utilization_percentage(self, spent_amount: float) -> float:
        """Calculate budget utilization percentage.
        
        Args:
            spent_amount: Amount spent so far
            
        Returns:
            Percentage of budget used (can exceed 100)
        """
        if self.amount <= 0:
            return 0.0
        return (spent_amount / self.amount) * 100
    
    def to_dict(self) -> dict:
        """Convert budget to dictionary for serialization."""
        return {
            "id": self.id,
            "category_id": self.category_id,
            "amount": self.amount,
            "period": self.period.name,
            "start_date": self.start_date.isoformat(),
            "alert_threshold": self.alert_threshold,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Budget:
        """Create budget from dictionary."""
        return cls(
            id=data["id"],
            category_id=data["category_id"],
            amount=data["amount"],
            period=BudgetPeriod[data["period"]],
            start_date=date.fromisoformat(data["start_date"]),
            alert_threshold=data["alert_threshold"],
            is_active=data.get("is_active", True),
            created_at=datetime.fromisoformat(data["created_at"])
        )


@dataclass
class BudgetAlert:
    """Represents a budget alert notification.
    
    Attributes:
        budget_id: ID of the budget that triggered the alert
        category_id: ID of the category
        category_name: Name of the category
        budget_amount: Total budget amount
        spent_amount: Amount spent
        remaining_amount: Amount remaining
        utilization_percentage: Percentage of budget used
        message: Human-readable alert message
        triggered_at: When the alert was triggered
    """
    
    budget_id: str
    category_id: str
    category_name: str
    budget_amount: float
    spent_amount: float
    remaining_amount: float
    utilization_percentage: float
    message: str
    triggered_at: datetime = field(default_factory=datetime.now)
    
    def is_critical(self) -> bool:
        """Check if this is a critical alert (over budget)."""
        return self.utilization_percentage >= 100


def create_budget(
    category_id: str,
    amount: float,
    period: BudgetPeriod = BudgetPeriod.MONTHLY,
    start_date: Optional[date] = None,
    alert_threshold: float = 80.0
) -> Budget:
    """Factory function to create a new budget.
    
    Args:
        category_id: Category to budget
        amount: Budget limit amount
        period: Budget period (default: monthly)
        start_date: Period start date (default: today)
        alert_threshold: Alert percentage 0-100 (default: 80)
        
    Returns:
        New Budget instance
        
    Raises:
        ValueError: If amount is not positive or threshold not in 0-100
    """
    if amount <= 0:
        raise ValueError("Budget amount must be positive")
    if not 0 <= alert_threshold <= 100:
        raise ValueError("Alert threshold must be between 0 and 100")
    if not category_id:
        raise ValueError("Category ID is required")
    
    return Budget(
        category_id=category_id,
        amount=amount,
        period=period,
        start_date=start_date or date.today(),
        alert_threshold=alert_threshold
    )

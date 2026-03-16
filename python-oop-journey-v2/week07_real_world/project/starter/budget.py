"""Budget management module.

Domain model for tracking spending budgets by category.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum, auto
from typing import Optional


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
    
    # TODO: Implement the Budget dataclass
    # - Define all attributes with proper types
    # - Set appropriate default values
    
    def get_period_dates(self) -> tuple[date, date]:
        """Calculate the start and end dates for the current period.
        
        Returns:
            Tuple of (period_start, period_end)
        """
        raise NotImplementedError("Implement get_period_dates method")
    
    def is_alert_triggered(self, spent_amount: float) -> bool:
        """Check if spending has exceeded the alert threshold.
        
        Args:
            spent_amount: Amount spent so far in the period
            
        Returns:
            True if alert should be triggered
        """
        raise NotImplementedError("Implement is_alert_triggered method")
    
    def get_remaining(self, spent_amount: float) -> float:
        """Calculate remaining budget.
        
        Args:
            spent_amount: Amount spent so far
            
        Returns:
            Remaining budget (can be negative if over budget)
        """
        raise NotImplementedError("Implement get_remaining method")
    
    def get_utilization_percentage(self, spent_amount: float) -> float:
        """Calculate budget utilization percentage.
        
        Args:
            spent_amount: Amount spent so far
            
        Returns:
            Percentage of budget used (can exceed 100)
        """
        raise NotImplementedError("Implement get_utilization_percentage method")
    
    def to_dict(self) -> dict:
        """Convert budget to dictionary for serialization."""
        raise NotImplementedError("Implement to_dict method")
    
    @classmethod
    def from_dict(cls, data: dict) -> Budget:
        """Create budget from dictionary."""
        raise NotImplementedError("Implement from_dict method")


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
    
    # TODO: Implement the BudgetAlert dataclass
    
    def is_critical(self) -> bool:
        """Check if this is a critical alert (over budget)."""
        raise NotImplementedError("Implement is_critical method")


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
    raise NotImplementedError("Implement create_budget function")

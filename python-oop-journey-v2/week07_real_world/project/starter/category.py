"""Transaction category management module.

Domain model for categorizing transactions (e.g., groceries, salary, utilities).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class CategoryType(Enum):
    """Types of categories - income or expense."""
    INCOME = auto()
    EXPENSE = auto()


@dataclass
class Category:
    """Represents a transaction category.
    
    Categories help organize transactions for budgeting and reporting.
    
    Attributes:
        id: Unique identifier for the category
        name: Category name (e.g., "Groceries", "Salary")
        type: Whether this is an income or expense category
        color: Hex color code for visual reports (e.g., "#FF5733")
        icon: Icon identifier for UI representation
        description: Optional description of the category
        is_active: Whether the category is available for use
    """
    
    # TODO: Implement the Category dataclass
    # - Define all attributes with proper types
    # - Set appropriate default values
    # - Consider adding a parent_id for hierarchical categories
    
    def is_income(self) -> bool:
        """Check if this is an income category."""
        raise NotImplementedError("Implement is_income method")
    
    def is_expense(self) -> bool:
        """Check if this is an expense category."""
        raise NotImplementedError("Implement is_expense method")
    
    def to_dict(self) -> dict:
        """Convert category to dictionary for serialization."""
        raise NotImplementedError("Implement to_dict method")
    
    @classmethod
    def from_dict(cls, data: dict) -> Category:
        """Create category from dictionary."""
        raise NotImplementedError("Implement from_dict method")


# Pre-defined common categories for convenience
DEFAULT_CATEGORIES: list[Category] = []
"""List of default categories to populate a new finance tracker."""


def get_default_categories() -> list[Category]:
    """Get a list of common default categories.
    
    Returns:
        List of pre-configured categories for typical use cases
    """
    raise NotImplementedError("Implement get_default_categories function")


def create_category(
    name: str,
    category_type: CategoryType,
    color: Optional[str] = None,
    icon: Optional[str] = None,
    description: Optional[str] = None
) -> Category:
    """Factory function to create a new category.
    
    Args:
        name: Category name
        category_type: INCOME or EXPENSE
        color: Optional hex color code
        icon: Optional icon identifier
        description: Optional description
        
    Returns:
        New Category instance
    """
    raise NotImplementedError("Implement create_category function")

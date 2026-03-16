"""Transaction category management module.

Domain model for categorizing transactions (e.g., groceries, salary, utilities).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
import uuid


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
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    type: CategoryType = CategoryType.EXPENSE
    color: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True
    
    def __post_init__(self) -> None:
        """Validate category after creation."""
        if not self.name:
            raise ValueError("Category name cannot be empty")
    
    def is_income(self) -> bool:
        """Check if this is an income category."""
        return self.type == CategoryType.INCOME
    
    def is_expense(self) -> bool:
        """Check if this is an expense category."""
        return self.type == CategoryType.EXPENSE
    
    def to_dict(self) -> dict:
        """Convert category to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.name,
            "color": self.color,
            "icon": self.icon,
            "description": self.description,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Category:
        """Create category from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            type=CategoryType[data["type"]],
            color=data.get("color"),
            icon=data.get("icon"),
            description=data.get("description"),
            is_active=data.get("is_active", True)
        )


# Pre-defined common categories for convenience
DEFAULT_CATEGORIES: list[Category] = []
"""List of default categories to populate a new finance tracker."""


def get_default_categories() -> list[Category]:
    """Get a list of common default categories.
    
    Returns:
        List of pre-configured categories for typical use cases
    """
    return [
        # Income categories
        Category(name="Salary", type=CategoryType.INCOME, color="#22C55E", icon="money-bag"),
        Category(name="Freelance", type=CategoryType.INCOME, color="#16A34A", icon="laptop"),
        Category(name="Investments", type=CategoryType.INCOME, color="#15803D", icon="trending-up"),
        Category(name="Gifts", type=CategoryType.INCOME, color="#166534", icon="gift"),
        
        # Expense categories
        Category(name="Housing", type=CategoryType.EXPENSE, color="#EF4444", icon="home"),
        Category(name="Food", type=CategoryType.EXPENSE, color="#F97316", icon="utensils"),
        Category(name="Groceries", type=CategoryType.EXPENSE, color="#FB923C", icon="shopping-cart"),
        Category(name="Dining Out", type=CategoryType.EXPENSE, color="#FDBA74", icon="restaurant"),
        Category(name="Transportation", type=CategoryType.EXPENSE, color="#3B82F6", icon="car"),
        Category(name="Utilities", type=CategoryType.EXPENSE, color="#06B6D4", icon="bolt"),
        Category(name="Entertainment", type=CategoryType.EXPENSE, color="#8B5CF6", icon="film"),
        Category(name="Healthcare", type=CategoryType.EXPENSE, color="#EC4899", icon="heart"),
        Category(name="Shopping", type=CategoryType.EXPENSE, color="#F43F5E", icon="shopping-bag"),
        Category(name="Education", type=CategoryType.EXPENSE, color="#6366F1", icon="book"),
        Category(name="Personal Care", type=CategoryType.EXPENSE, color="#14B8A6", icon="smile"),
        Category(name="Insurance", type=CategoryType.EXPENSE, color="#64748B", icon="shield"),
        Category(name="Savings", type=CategoryType.EXPENSE, color="#10B981", icon="piggy-bank"),
    ]


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
    if not name:
        raise ValueError("Category name cannot be empty")
    
    return Category(
        name=name,
        type=category_type,
        color=color,
        icon=icon,
        description=description
    )

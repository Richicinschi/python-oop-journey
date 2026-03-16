"""User Module - Starter.

TODO: Implement the User class for the e-commerce system.

WEEK 3 CONCEPT CONNECTIONS:
- Day 5 (Composition): User has-a ShoppingCart (created on init)
- Day 2 (Method Types): validate_email() staticmethod, set_email_whitelist() classmethod
- Day 3 (Encapsulation): Email validation in setter, _orders is private
- Day 6 (Design): User manages user data, delegates cart logic to Cart class

IMPLEMENT AFTER: cart.py (User composes ShoppingCart)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order


class User:
    """Represents a user/customer in the e-commerce system.
    
    A user has a unique ID, name, email, and maintains a shopping cart
    and order history. The email should be validated for proper format.
    
    Attributes:
        user_id: Unique identifier for the user.
        name: The user's full name.
        email: The user's email address.
        cart: The user's shopping cart.
        orders: List of user's past orders.
    
    Example:
        >>> user = User("U001", "Alice Smith", "alice@example.com")
        >>> user.name
        'Alice Smith'
        >>> user.email
        'alice@example.com'
    """
    
    _email_domain_whitelist: list[str] = []
    
    def __init__(self, user_id: str, name: str, email: str) -> None:
        """Initialize a User.
        
        Args:
            user_id: Unique identifier for the user.
            name: The user's full name.
            email: The user's email address.
        
        Raises:
            ValueError: If email format is invalid or if any string is empty.
        """
        # TODO: Implement initialization with email validation
        raise NotImplementedError("Implement __init__")
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        # TODO: Implement __repr__
        raise NotImplementedError("Implement __repr__")
    
    @property
    def user_id(self) -> str:
        """Get the user ID (read-only)."""
        # TODO: Implement user_id getter (read-only)
        raise NotImplementedError("Implement user_id getter")
    
    @property
    def name(self) -> str:
        """Get the user name."""
        # TODO: Implement name getter
        raise NotImplementedError("Implement name getter")
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the user name with validation."""
        # TODO: Implement name setter with validation
        raise NotImplementedError("Implement name setter")
    
    @property
    def email(self) -> str:
        """Get the user email."""
        # TODO: Implement email getter
        raise NotImplementedError("Implement email getter")
    
    @email.setter
    def email(self, value: str) -> None:
        """Set the user email with validation."""
        # TODO: Implement email setter with validation
        raise NotImplementedError("Implement email setter")
    
    @property
    def cart(self) -> "ShoppingCart":
        """Get the user's shopping cart."""
        # TODO: Implement cart property
        # Hint: Import ShoppingCart inside the property to avoid circular imports
        raise NotImplementedError("Implement cart getter")
    
    @property
    def orders(self) -> list["Order"]:
        """Get the user's order history (copy)."""
        # TODO: Implement orders getter returning a copy
        raise NotImplementedError("Implement orders getter")
    
    def add_order(self, order: "Order") -> None:
        """Add an order to the user's history.
        
        Args:
            order: The order to add.
        """
        # TODO: Implement add_order
        raise NotImplementedError("Implement add_order")
    
    def get_total_spent(self) -> float:
        """Calculate total amount spent by the user.
        
        Returns:
            Sum of all order totals.
        """
        # TODO: Implement total spent calculation
        raise NotImplementedError("Implement get_total_spent")
    
    def get_order_count(self) -> int:
        """Get the number of orders placed.
        
        Returns:
            Number of orders.
        """
        # TODO: Implement order count
        raise NotImplementedError("Implement get_order_count")
    
    @classmethod
    def set_email_whitelist(cls, domains: list[str]) -> None:
        """Set allowed email domains for registration.
        
        Args:
            domains: List of allowed domain strings (e.g., ["example.com"]).
        """
        # TODO: Implement email whitelist setter
        raise NotImplementedError("Implement set_email_whitelist")
    
    @classmethod
    def clear_email_whitelist(cls) -> None:
        """Clear the email domain whitelist (allow all valid emails)."""
        # TODO: Implement email whitelist clear
        raise NotImplementedError("Implement clear_email_whitelist")
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format.
        
        Basic validation: must contain @ and a domain after it.
        Local part and domain part must not be empty.
        
        Args:
            email: The email to validate.
        
        Returns:
            True if valid, False otherwise.
        """
        # TODO: Implement email validation
        raise NotImplementedError("Implement validate_email")

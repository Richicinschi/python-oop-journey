"""User Module - Reference Solution.

Implements the User class for the e-commerce system.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cart import ShoppingCart
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
        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string")
        if not self.validate_email(email):
            raise ValueError(f"Invalid email format: {email}")
        
        # Check whitelist if set
        if self._email_domain_whitelist:
            domain = email.split("@")[1]
            if domain not in self._email_domain_whitelist:
                raise ValueError(f"Email domain '{domain}' not in whitelist")
        
        self._user_id = user_id
        self._name = name
        self._email = email
        self._orders: list[Order] = []
        
        # Import here to avoid circular import
        from .cart import ShoppingCart
        self._cart = ShoppingCart()
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"User(user_id='{self._user_id}', name='{self._name}', email='{self._email}')"
    
    @property
    def user_id(self) -> str:
        """Get the user ID (read-only)."""
        return self._user_id
    
    @property
    def name(self) -> str:
        """Get the user name."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the user name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        self._name = value
    
    @property
    def email(self) -> str:
        """Get the user email."""
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        """Set the user email with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Email must be a non-empty string")
        if not self.validate_email(value):
            raise ValueError(f"Invalid email format: {value}")
        
        # Check whitelist if set
        if self._email_domain_whitelist:
            domain = value.split("@")[1]
            if domain not in self._email_domain_whitelist:
                raise ValueError(f"Email domain '{domain}' not in whitelist")
        
        self._email = value
    
    @property
    def cart(self) -> ShoppingCart:
        """Get the user's shopping cart."""
        return self._cart
    
    @property
    def orders(self) -> list[Order]:
        """Get the user's order history (copy)."""
        return self._orders.copy()
    
    def add_order(self, order: Order) -> None:
        """Add an order to the user's history.
        
        Args:
            order: The order to add.
        """
        self._orders.append(order)
    
    def get_total_spent(self) -> float:
        """Calculate total amount spent by the user.
        
        Returns:
            Sum of all order totals.
        """
        return sum(order.total for order in self._orders)
    
    def get_order_count(self) -> int:
        """Get the number of orders placed.
        
        Returns:
            Number of orders.
        """
        return len(self._orders)
    
    @classmethod
    def set_email_whitelist(cls, domains: list[str]) -> None:
        """Set allowed email domains for registration.
        
        Args:
            domains: List of allowed domain strings (e.g., ["example.com"]).
        """
        cls._email_domain_whitelist = list(domains)
    
    @classmethod
    def clear_email_whitelist(cls) -> None:
        """Clear the email domain whitelist (allow all valid emails)."""
        cls._email_domain_whitelist = []
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format.
        
        Basic validation: must contain @ and a domain after it.
        Local part and domain part must not be empty.
        No spaces allowed.
        
        Args:
            email: The email to validate.
        
        Returns:
            True if valid, False otherwise.
        """
        if not email or not isinstance(email, str):
            return False
        
        # Check for spaces
        if " " in email:
            return False
        
        if "@" not in email:
            return False
        
        parts = email.split("@")
        if len(parts) != 2:
            return False
        
        local, domain = parts
        if not local or not domain:
            return False
        
        # Domain should have at least one dot and something after it
        if "." not in domain:
            return False
        
        domain_parts = domain.split(".")
        if not all(part for part in domain_parts):
            return False
        
        return True

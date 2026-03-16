"""Solution for Problem 07: Email Address.

Demonstrates email validation with @property.setter.
"""

from __future__ import annotations

import re


class Contact:
    """A contact with validated email address.
    
    This class demonstrates email format validation using
    regular expressions within a property setter.
    
    Attributes:
        name: The contact's name.
        phone: The contact's phone number.
    
    Example:
        >>> contact = Contact("Alice", "alice@example.com")
        >>> contact.email
        'alice@example.com'
        >>> contact.email = "bob@test.org"
        >>> contact.email
        'bob@test.org'
    """
    
    # Basic email pattern (simplified for demonstration)
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    def __init__(self, name: str, email: str, phone: str = "") -> None:
        """Initialize a contact.
        
        Args:
            name: The contact's name.
            email: The contact's email address.
            phone: The contact's phone number (optional).
        
        Raises:
            TypeError: If types are incorrect.
            ValueError: If name is empty or email format is invalid.
        """
        self.name = name  # Use setter
        self._email: str = ""
        self.email = email  # Use setter for validation
        self.phone = phone  # Use setter
    
    @property
    def name(self) -> str:
        """Get the contact's name.
        
        Returns:
            The contact's name.
        """
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the contact's name.
        
        Args:
            value: The new name.
        
        Raises:
            TypeError: If value is not a string.
            ValueError: If name is empty.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def email(self) -> str:
        """Get the email address.
        
        Returns:
            The contact's email address.
        """
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        """Set the email address with validation.
        
        Args:
            value: The new email address.
        
        Raises:
            TypeError: If value is not a string.
            ValueError: If email format is invalid.
        """
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        
        email = value.strip().lower()
        if not email:
            raise ValueError("Email cannot be empty")
        
        if not self.EMAIL_PATTERN.match(email):
            raise ValueError(f"Invalid email format: {value}")
        
        self._email = email
    
    @property
    def phone(self) -> str:
        """Get the phone number.
        
        Returns:
            The contact's phone number.
        """
        return self._phone
    
    @phone.setter
    def phone(self, value: str) -> None:
        """Set the phone number.
        
        Args:
            value: The new phone number.
        
        Raises:
            TypeError: If value is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Phone must be a string")
        self._phone = value.strip()
    
    @property
    def domain(self) -> str:
        """Extract the domain from the email (read-only).
        
        Returns:
            The domain part of the email address.
        """
        if "@" in self._email:
            return self._email.split("@")[1]
        return ""
    
    @property
    def username(self) -> str:
        """Extract the username from the email (read-only).
        
        Returns:
            The username part of the email address.
        """
        if "@" in self._email:
            return self._email.split("@")[0]
        return ""
    
    def is_gmail(self) -> bool:
        """Check if email is a Gmail address.
        
        Returns:
            True if email domain is gmail.com, False otherwise.
        """
        return self.domain == "gmail.com"
    
    def get_display_info(self) -> str:
        """Get formatted contact information.
        
        Returns:
            A formatted string with contact details.
        """
        info = f"{self._name} <{self._email}>"
        if self._phone:
            info += f" (Tel: {self._phone})"
        return info

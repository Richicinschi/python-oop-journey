"""Exercise: Email Address.

Implement a Contact class with email validation.

TODO:
1. Implement @property for email with regex validation
2. Implement read-only properties: domain, username
3. Implement is_gmail method
4. Implement get_display_info method
"""

from __future__ import annotations

import re


class Contact:
    """A contact with validated email address.
    
    Attributes:
        name: The contact's name.
        phone: The contact's phone number.
    """
    
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def __init__(self, name: str, email: str, phone: str = "") -> None:
        """Initialize a contact."""
        self._name = name.strip()
        self._email: str = ""
        self.email = email  # Use setter for validation
        self._phone = phone.strip()
    
    @property
    def name(self) -> str:
        """Get the contact's name."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set the contact's name."""
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def email(self) -> str:
        """Get the email address."""
        # TODO: Return _email
        raise NotImplementedError("Return email")
    
    @email.setter
    def email(self, value: str) -> None:
        """Set the email address with validation."""
        # TODO: Strip whitespace and convert to lowercase
        # TODO: Validate using EMAIL_PATTERN regex
        # TODO: Raise ValueError if invalid format
        # TODO: Store in _email
        raise NotImplementedError("Validate and set email")
    
    @property
    def phone(self) -> str:
        """Get the phone number."""
        return self._phone
    
    @phone.setter
    def phone(self, value: str) -> None:
        """Set the phone number."""
        self._phone = value.strip()
    
    @property
    def domain(self) -> str:
        """Extract the domain from the email (read-only)."""
        # TODO: Split email by '@' and return the domain part
        raise NotImplementedError("Extract domain")
    
    @property
    def username(self) -> str:
        """Extract the username from the email (read-only)."""
        # TODO: Split email by '@' and return the username part
        raise NotImplementedError("Extract username")
    
    def is_gmail(self) -> bool:
        """Check if email is a Gmail address."""
        # TODO: Return True if domain is 'gmail.com'
        raise NotImplementedError("Check gmail")
    
    def get_display_info(self) -> str:
        """Get formatted contact information."""
        # TODO: Return formatted string like "Name <email> (Tel: phone)"
        # Note: Only include phone part if phone is not empty
        raise NotImplementedError("Format display info")

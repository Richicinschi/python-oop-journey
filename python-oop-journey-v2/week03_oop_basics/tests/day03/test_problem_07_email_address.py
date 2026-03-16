"""Tests for Problem 07: Email Address."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day03.problem_07_email_address import (
    Contact,
)


class TestContact:
    """Test suite for Contact class."""
    
    def test_initialization(self) -> None:
        """Test contact initialization."""
        contact = Contact("Alice", "alice@example.com")
        assert contact.name == "Alice"
        assert contact.email == "alice@example.com"
        assert contact.phone == ""
    
    def test_initialization_with_phone(self) -> None:
        """Test contact initialization with phone."""
        contact = Contact("Alice", "alice@example.com", "555-1234")
        assert contact.phone == "555-1234"
    
    def test_initialization_strips_strings(self) -> None:
        """Test that strings are stripped."""
        contact = Contact("  Alice  ", "  alice@example.com  ", "  555-1234  ")
        assert contact.name == "Alice"
        assert contact.email == "alice@example.com"
        assert contact.phone == "555-1234"
    
    def test_initialization_email_lowercase(self) -> None:
        """Test that email is converted to lowercase."""
        contact = Contact("Alice", "ALICE@EXAMPLE.COM")
        assert contact.email == "alice@example.com"
    
    def test_initialization_invalid_email_raises(self) -> None:
        """Test initialization with invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email"):
            Contact("Alice", "not-an-email")
    
    def test_initialization_empty_email_raises(self) -> None:
        """Test initialization with empty email raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            Contact("Alice", "")
    
    def test_name_setter_valid(self) -> None:
        """Test name setter with valid value."""
        contact = Contact("Alice", "alice@example.com")
        contact.name = "Bob"
        assert contact.name == "Bob"
    
    def test_name_setter_empty_raises(self) -> None:
        """Test name setter with empty value raises ValueError."""
        contact = Contact("Alice", "alice@example.com")
        with pytest.raises(ValueError, match="empty"):
            contact.name = ""
    
    def test_name_setter_non_string_raises(self) -> None:
        """Test name setter with non-string raises TypeError."""
        contact = Contact("Alice", "alice@example.com")
        with pytest.raises(TypeError, match="string"):
            contact.name = 123  # type: ignore
    
    def test_email_getter(self) -> None:
        """Test email getter."""
        contact = Contact("Alice", "alice@example.com")
        assert contact.email == "alice@example.com"
    
    def test_email_setter_valid(self) -> None:
        """Test email setter with valid value."""
        contact = Contact("Alice", "alice@example.com")
        contact.email = "bob@test.org"
        assert contact.email == "bob@test.org"
    
    def test_email_setter_invalid_raises(self) -> None:
        """Test email setter with invalid email raises ValueError."""
        contact = Contact("Alice", "alice@example.com")
        with pytest.raises(ValueError, match="Invalid email"):
            contact.email = "not-valid"
    
    def test_email_setter_non_string_raises(self) -> None:
        """Test email setter with non-string raises TypeError."""
        contact = Contact("Alice", "alice@example.com")
        with pytest.raises(TypeError, match="string"):
            contact.email = 123  # type: ignore
    
    def test_phone_setter(self) -> None:
        """Test phone setter."""
        contact = Contact("Alice", "alice@example.com")
        contact.phone = "555-5678"
        assert contact.phone == "555-5678"
    
    def test_phone_setter_non_string_raises(self) -> None:
        """Test phone setter with non-string raises TypeError."""
        contact = Contact("Alice", "alice@example.com")
        with pytest.raises(TypeError, match="string"):
            contact.phone = 5551234  # type: ignore
    
    def test_domain_property(self) -> None:
        """Test domain property."""
        contact = Contact("Alice", "alice@example.com")
        assert contact.domain == "example.com"
    
    def test_domain_complex(self) -> None:
        """Test domain property with complex domain."""
        contact = Contact("Alice", "user@mail.company.co.uk")
        assert contact.domain == "mail.company.co.uk"
    
    def test_username_property(self) -> None:
        """Test username property."""
        contact = Contact("Alice", "alice@example.com")
        assert contact.username == "alice"
    
    def test_username_complex(self) -> None:
        """Test username property with complex username."""
        contact = Contact("Alice", "user.name+tag@example.com")
        assert contact.username == "user.name+tag"
    
    def test_is_gmail_true(self) -> None:
        """Test is_gmail returns True for gmail addresses."""
        contact = Contact("Alice", "alice@gmail.com")
        assert contact.is_gmail() is True
    
    def test_is_gmail_false(self) -> None:
        """Test is_gmail returns False for non-gmail addresses."""
        contact = Contact("Alice", "alice@example.com")
        assert contact.is_gmail() is False
    
    def test_get_display_info_without_phone(self) -> None:
        """Test get_display_info without phone."""
        contact = Contact("Alice", "alice@example.com")
        info = contact.get_display_info()
        assert "Alice" in info
        assert "alice@example.com" in info
        assert "Tel" not in info
    
    def test_get_display_info_with_phone(self) -> None:
        """Test get_display_info with phone."""
        contact = Contact("Alice", "alice@example.com", "555-1234")
        info = contact.get_display_info()
        assert "Alice" in info
        assert "alice@example.com" in info
        assert "555-1234" in info
    
    def test_valid_emails(self) -> None:
        """Test various valid email formats."""
        valid_emails = [
            "simple@example.com",
            "very.common@example.com",
            "disposable.style.stripe.with+symbol@example.com",
            "other.email-with-hyphen@example.com",
            "user.name+tag+sorting@example.com",
            "x@example.com",
            "example-indeed@strange-example.com",
            "user%example.com@example.org",
        ]
        for email in valid_emails:
            contact = Contact("Test", email)
            assert contact.email == email.lower()

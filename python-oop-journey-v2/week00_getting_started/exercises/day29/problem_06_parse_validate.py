"""Problem 06: Parse and Validate Records

Topic: String parsing, validation, error handling
Difficulty: Medium

Create a robust parser for formatted records with multiple validation checks.

Required functions:
- parse_email_record(record): Parse email|name|age format
- validate_email(email): Check if email format is valid
- validate_age(age): Check if age is valid (18-120)
- process_email_records(records): Process multiple records

Record format:
    "email@example.com|John Doe|25"

Validation rules:
- Email must contain @ and . in reasonable positions
- Name must be non-empty and contain only letters and spaces
- Age must be integer between 18 and 120 inclusive

Example:
    >>> parse_email_record("john@example.com|John Doe|25")
    {'email': 'john@example.com', 'name': 'John Doe', 'age': 25}
    >>> validate_email("john@example.com")
    True
    >>> validate_email("invalid-email")
    False
    >>> process_email_records(["a@b.com|Alice|30", "invalid"])
    {
        'valid': [{'email': 'a@b.com', 'name': 'Alice', 'age': 30}],
        'invalid': [('invalid', 'Invalid format')]
    }
"""

from __future__ import annotations


def parse_email_record(record: str) -> dict | None:
    """Parse an email record string into components.

    Args:
        record: String in format "email|name|age"

    Returns:
        Dictionary with email, name, age fields, or None if invalid format
    """
    raise NotImplementedError("Implement parse_email_record")


def validate_email(email: str) -> bool:
    """Validate email format.

    Basic validation: must contain @, must have content before and after @,
    must contain . in domain part.

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    raise NotImplementedError("Implement validate_email")


def validate_age(age_str: str) -> tuple[bool, int | None, str]:
    """Validate age string.

    Args:
        age_str: String representation of age

    Returns:
        Tuple of (is_valid, age_as_int, error_message)
    """
    raise NotImplementedError("Implement validate_age")


def process_email_records(records: list[str]) -> dict:
    """Process multiple email records.

    Args:
        records: List of record strings

    Returns:
        Dictionary with:
            - valid: List of valid parsed records
            - invalid: List of (record, error) tuples
    """
    raise NotImplementedError("Implement process_email_records")

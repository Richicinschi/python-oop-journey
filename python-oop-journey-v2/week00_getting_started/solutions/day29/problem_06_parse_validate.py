"""Reference solution for Problem 06: Parse and Validate Records."""

from __future__ import annotations


def parse_email_record(record: str) -> dict | None:
    """Parse an email record string into components.

    Args:
        record: String in format "email|name|age"

    Returns:
        Dictionary with email, name, age fields, or None if invalid format
    """
    parts = record.split("|")
    if len(parts) != 3:
        return None

    return {
        "email": parts[0].strip(),
        "name": parts[1].strip(),
        "age": parts[2].strip(),
    }


def validate_email(email: str) -> bool:
    """Validate email format.

    Basic validation: must contain @, must have content before and after @,
    must contain . in domain part, no spaces allowed.

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
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

    if "." not in domain:
        return False

    return True


def validate_age(age_str: str) -> tuple[bool, int | None, str]:
    """Validate age string.

    Args:
        age_str: String representation of age

    Returns:
        Tuple of (is_valid, age_as_int, error_message)
    """
    try:
        age = int(age_str)
    except ValueError:
        return False, None, "Age must be an integer"

    if not 18 <= age <= 120:
        return False, None, "Age must be between 18 and 120"

    return True, age, ""


def process_email_records(records: list[str]) -> dict:
    """Process multiple email records.

    Args:
        records: List of record strings

    Returns:
        Dictionary with valid and invalid records
    """
    valid = []
    invalid = []

    for record in records:
        parsed = parse_email_record(record)
        if parsed is None:
            invalid.append((record, "Invalid format"))
            continue

        if not validate_email(parsed["email"]):
            invalid.append((record, "Invalid email"))
            continue

        is_valid_age, age, age_error = validate_age(parsed["age"])
        if not is_valid_age:
            invalid.append((record, age_error))
            continue

        # Validate name (letters and spaces only)
        if not all(c.isalpha() or c.isspace() for c in parsed["name"]):
            invalid.append((record, "Invalid name"))
            continue

        valid.append(
            {
                "email": parsed["email"],
                "name": parsed["name"],
                "age": age,
            }
        )

    return {"valid": valid, "invalid": invalid}

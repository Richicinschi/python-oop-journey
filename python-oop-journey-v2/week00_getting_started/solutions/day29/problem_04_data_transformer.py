"""Reference solution for Problem 04: Data Transformer Pipeline."""

from __future__ import annotations


def parse_record(line: str) -> dict[str, str] | None:
    """Parse a CSV-like record into a dictionary.

    Args:
        line: A comma-separated string with fields: name,age,city,salary

    Returns:
        Dictionary with field names as keys, or None if parsing fails
    """
    parts = line.split(",")
    if len(parts) != 4:
        return None

    return {
        "name": parts[0].strip(),
        "age": parts[1].strip(),
        "city": parts[2].strip(),
        "salary": parts[3].strip(),
    }


def validate_record(record: dict) -> tuple[bool, str]:
    """Validate a parsed record.

    Args:
        record: Dictionary with record fields

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not record:
        return False, "Empty record"

    required = ["name", "age", "city", "salary"]
    for field in required:
        if field not in record or not record[field]:
            return False, f"Missing field: {field}"

    # Validate age
    try:
        age = int(record["age"])
        if not 0 <= age <= 150:
            return False, "Age must be between 0 and 150"
    except ValueError:
        return False, "Age must be an integer"

    # Validate salary
    try:
        salary = float(record["salary"])
        if salary < 0:
            return False, "Salary must be non-negative"
    except ValueError:
        return False, "Salary must be a number"

    return True, ""


def transform_record(record: dict[str, str]) -> dict | None:
    """Apply transformations to a validated record.

    Args:
        record: Dictionary with string values

    Returns:
        Transformed dictionary with proper types, or None if invalid
    """
    is_valid, error = validate_record(record)
    if not is_valid:
        return None

    return {
        "name": record["name"].strip().title(),
        "age": int(record["age"]),
        "city": record["city"].strip(),
        "salary": round(float(record["salary"]), 2),
    }


def process_records(lines: list[str]) -> dict:
    """Process multiple records through the pipeline.

    Args:
        lines: List of CSV-like record strings

    Returns:
        Dictionary with success, failed, and stats
    """
    success = []
    failed = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        record = parse_record(line)
        if record is None:
            failed.append((line, "Invalid format"))
            continue

        is_valid, error = validate_record(record)
        if not is_valid:
            failed.append((line, error))
            continue

        transformed = transform_record(record)
        if transformed:
            success.append(transformed)
        else:
            failed.append((line, "Transformation failed"))

    return {
        "success": success,
        "failed": failed,
        "stats": {
            "count_success": len(success),
            "count_failed": len(failed),
            "count_total": len(success) + len(failed),
        },
    }

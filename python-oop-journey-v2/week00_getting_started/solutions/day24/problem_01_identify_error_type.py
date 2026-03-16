"""Reference solution for Problem 01: Identify Error Type."""

from __future__ import annotations


def identify_error(scenario: str) -> str:
    """Return the error type name for a given scenario.

    Args:
        scenario: A string describing an error scenario

    Returns:
        The name of the Python exception type as a string
    """
    error_map = {
        "division_by_zero": "ZeroDivisionError",
        "undefined_variable": "NameError",
        "wrong_type": "TypeError",
        "index_too_big": "IndexError",
        "key_not_found": "KeyError",
        "invalid_conversion": "ValueError",
    }
    return error_map.get(scenario, "UnknownError")

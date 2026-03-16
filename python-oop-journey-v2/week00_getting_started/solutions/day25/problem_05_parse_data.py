"""Reference solution for Problem 05: Parse Data."""

from __future__ import annotations


def parse_data(data_string: str) -> dict:
    """Parse a key:value pair string into a dictionary.

    Args:
        data_string: A string in format "key1:value1,key2:value2"

    Returns:
        A dictionary of parsed key-value pairs
    """
    result = {}
    
    if not data_string or ":" not in data_string:
        return result
    
    pairs = data_string.split(",")
    
    for pair in pairs:
        if ":" in pair:
            parts = pair.split(":", 1)  # Split on first colon only
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                if key:  # Only add if key is not empty
                    result[key] = value
    
    return result

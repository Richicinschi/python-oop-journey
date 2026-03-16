"""Problem 05: Parse Data

Topic: Try and Except
Difficulty: Medium

Write a function that parses data from a string into a dictionary.

The input format is: "key1:value1,key2:value2,..."

Handle errors gracefully:
- Invalid format: return empty dict
- Malformed pairs: skip them

Examples:
    >>> parse_data("name:Alice,age:30")
    {'name': 'Alice', 'age': '30'}
    >>> parse_data("invalid")
    {}
    >>> parse_data("good:pair,badpair,also:good")
    {'good': 'pair', 'also': 'good'}

Requirements:
    - Parse key-value pairs separated by commas
    - Each pair should be key:value
    - Skip malformed pairs (those without colon)
    - Return empty dict for completely invalid input

HINTS:
    Hint 1 (Conceptual): Break the problem into steps:
        1. Split the input string by commas to get pairs
        2. For each pair, check if it has a colon
        3. Split valid pairs by colon to get key and value
        4. Add to dictionary

    Hint 2 (Structural):
        - Use string.split(',') to get pairs
        - Use string.split(':', 1) to split on first colon only
          (This preserves colons in the value part)
        - Check if split result has exactly 2 parts
        - Skip pairs that don't have a colon

    Hint 3 (Edge Cases):
        - Empty string: parse_data("") -> {}
        - Pair with empty key: parse_data(":value") -> skip this pair
        - Pair with multiple colons: parse_data("time:10:30") -> key="time", value="10:30"
        - All malformed: parse_data("a,b,c") -> {}

DEBUGGING TIPS:
    - If getting index errors, check your split result length before accessing [0] or [1]
    - If colons in values are being split: use split(':', 1) instead of split(':')
    - If empty pairs are being added: check for empty keys before adding
    - Use print(f"Processing pair: {pair}") to see what's happening
"""

from __future__ import annotations


def parse_data(data_string: str) -> dict:
    """Parse a key:value pair string into a dictionary.

    Args:
        data_string: A string in format "key1:value1,key2:value2"

    Returns:
        A dictionary of parsed key-value pairs
    """
    raise NotImplementedError("Implement parse_data")

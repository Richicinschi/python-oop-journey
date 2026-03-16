"""Problem 07: Nested Data Flattener

Topic: Recursion, lists, data structures
Difficulty: Medium

Create functions to flatten nested data structures of arbitrary depth.

Required functions:
- flatten_list(nested): Flatten a nested list structure
- flatten_dict(nested, prefix): Flatten a nested dictionary
- flatten_mixed(data): Flatten mixed nested structures

Rules:
- flatten_list: [[1, 2], [3, [4, 5]]] -> [1, 2, 3, 4, 5]
- flatten_dict: {'a': {'b': 1}} -> {'a.b': 1} with prefix option
- flatten_mixed: Handle lists containing mixed types including dicts

Example:
    >>> flatten_list([1, [2, 3], [[4, 5], 6]])
    [1, 2, 3, 4, 5, 6]
    >>> flatten_dict({'a': 1, 'b': {'c': 2, 'd': {'e': 3}}})
    {'a': 1, 'b.c': 2, 'b.d.e': 3}
    >>> flatten_mixed([1, {'a': [2, 3]}, [4, 5]])
    [1, {'a': [2, 3]}, 4, 5]  # dicts not flattened, only lists

HINTS:
    Hint 1 (Conceptual): Recursion is your friend for arbitrary nesting depth.
        When you encounter a nested list, you need to flatten it too.
        Think: "What is my base case? What is my recursive case?"

    Hint 2 (Structural):
        For flatten_list:
        1. Create an empty result list
        2. Loop through each item in the input
        3. If item is a list: extend result with flatten_list(item)
        4. If item is not a list: append item to result
        5. Return result

        For flatten_dict:
        1. Create empty result dict
        2. For each key, value in input items():
           - If value is a dict: recurse with prefix + key + "."
           - Else: result[new_key] = value
        3. Return result

    Hint 3 (Edge Cases):
        - Empty lists: flatten_list([]) -> []
        - Empty nested lists: flatten_list([1, [], 2]) -> [1, 2]
        - Deep nesting: flatten_list([1, [2, [3, [4]]]]) -> [1, 2, 3, 4]
        - Strings in lists: flatten_mixed should NOT split strings!

DEBUGGING TIPS:
    - If getting infinite recursion, check your base case (are you checking for list type correctly?)
    - Use isinstance(item, list) to check if something is a list
    - Add print(f"Processing: {item}") to trace through the recursion
    - For flatten_dict, print the prefix at each level to see key construction
    - Remember: strings are iterable too! Don't accidentally recurse into strings
"""

from __future__ import annotations


def flatten_list(nested: list) -> list:
    """Flatten a nested list structure to a single level.

    Args:
        nested: A list potentially containing nested lists

    Returns:
        Flattened list with all non-list elements
    """
    raise NotImplementedError("Implement flatten_list")


def flatten_dict(nested: dict, prefix: str = "") -> dict[str, any]:
    """Flatten a nested dictionary using dot notation for keys.

    Args:
        nested: A potentially nested dictionary
        prefix: Prefix for keys (used in recursion)

    Returns:
        Flattened dictionary with dot-separated keys
    """
    raise NotImplementedError("Implement flatten_dict")


def flatten_mixed(data: list) -> list:
    """Flatten list structures, preserving non-list items.

    Flattens nested lists but keeps dictionaries and other types as-is.

    Args:
        data: A list potentially containing nested lists and other types

    Returns:
        List with nested lists flattened, other types preserved
    """
    raise NotImplementedError("Implement flatten_mixed")

"""Problem 04: Create Shopping List

Topic: Function Parameters - **kwargs
Difficulty: Easy

Write a function that creates a shopping list from keyword arguments.

Function Signature:
    def create_shopping_list(**items: int) -> dict[str, int]

Requirements:
    - Accept item_name=quantity as keyword arguments
    - Return a dictionary mapping item names to quantities
    - Return empty dict if no items provided

Behavior Notes:
    - **items collects keyword args into a dictionary
    - Keys are item names, values are quantities
    - Return the dictionary directly

Examples:
    >>> create_shopping_list(apple=5, banana=3, orange=2)
    {'apple': 5, 'banana': 3, 'orange': 2}
    
    Single item:
    >>> create_shopping_list(milk=1)
    {'milk': 1}
    
    No items:
    >>> create_shopping_list()
    {}

Input Validation:
    - You may assume all keyword values are integers

"""

from __future__ import annotations


def create_shopping_list(**items: int) -> dict[str, int]:
    """Create a shopping list from keyword arguments.

    Args:
        **items: Item names as keys, quantities as values.

    Returns:
        A dictionary of items and quantities.
    """
    raise NotImplementedError("Implement create_shopping_list")

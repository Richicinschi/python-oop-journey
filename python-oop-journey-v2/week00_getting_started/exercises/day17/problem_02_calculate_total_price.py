"""Problem 02: Calculate Total Price

Topic: Function Parameters - *args
Difficulty: Easy

Write a function that calculates the total price with variable items.

Function Signature:
    def calculate_total_price(base_price: float, *additional_costs: float) -> float

Requirements:
    - Start with base_price
    - Add all additional_costs
    - Return the total

Behavior Notes:
    - *additional_costs collects extra arguments into a tuple
    - Sum all values in the tuple
    - Works with zero additional costs

Examples:
    >>> calculate_total_price(100.0, 10.0, 20.0, 5.0)
    135.0
    
    No additional costs:
    >>> calculate_total_price(50.0)
    50.0
    
    Single additional cost:
    >>> calculate_total_price(100.0, 25.0)
    125.0
    
    Base price only:
    >>> calculate_total_price(0.0)
    0.0

Input Validation:
    - You may assume all arguments are numbers (int or float)

"""

from __future__ import annotations


def calculate_total_price(base_price: float, *additional_costs: float) -> float:
    """Calculate total price with variable additional costs.

    Args:
        base_price: The starting price.
        *additional_costs: Variable number of additional costs.

    Returns:
        The total price (base + sum of additional).
    """
    raise NotImplementedError("Implement calculate_total_price")

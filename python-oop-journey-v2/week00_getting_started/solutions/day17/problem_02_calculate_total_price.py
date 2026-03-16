"""Problem 02: Calculate Total Price - Solution."""

from __future__ import annotations


def calculate_total_price(
    price: float,
    quantity: int,
    tax_rate: float = 0.0,
    discount: float = 0.0,
) -> float:
    """Calculate the total price with optional tax and discount.

    The calculation order is:
    1. Calculate subtotal: price * quantity
    2. Apply discount: subtotal - (subtotal * discount)
    3. Apply tax: discounted_amount + (discounted_amount * tax_rate)

    Args:
        price: Price per unit.
        quantity: Number of units.
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%). Default is 0.0.
        discount: Discount rate as decimal (e.g., 0.10 for 10%). Default is 0.0.

    Returns:
        The final total price after discount and tax.
    """
    subtotal = price * quantity
    after_discount = subtotal * (1 - discount)
    total = after_discount * (1 + tax_rate)
    return round(total, 2)

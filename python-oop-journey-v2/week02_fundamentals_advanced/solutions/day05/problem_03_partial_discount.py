"""Problem 03: Partial Discount - Solution

Use functools.partial to create specialized discount and pricing functions
from a general pricing function.
"""

from __future__ import annotations

from functools import partial
from typing import Callable


def calculate_price(
    base_price: float,
    discount_rate: float,
    tax_rate: float,
    quantity: int
) -> float:
    """Calculate the final price for a product.

    Args:
        base_price: The base price of a single unit.
        discount_rate: Discount as a decimal (0.1 = 10% off).
        tax_rate: Tax rate as a decimal (0.08 = 8% tax).
        quantity: Number of units.

    Returns:
        The final price after discount and tax.

    Example:
        >>> calculate_price(100.0, 0.1, 0.08, 2)
        194.4  # (100 * 0.9 * 2) * 1.08 = 194.4
    """
    discounted_unit_price = base_price * (1 - discount_rate)
    subtotal = discounted_unit_price * quantity
    total = subtotal * (1 + tax_rate)
    return round(total, 2)


def create_fixed_discount_calculator(discount_rate: float) -> Callable[[float, float, int], float]:
    """Create a pricing calculator with a fixed discount rate.

    Args:
        discount_rate: The discount rate to apply.

    Returns:
        A function that takes (base_price, tax_rate, quantity).

    Example:
        >>> ten_percent_off = create_fixed_discount_calculator(0.10)
        >>> ten_percent_off(100.0, 0.08, 1)
        97.2
    """
    def calculator(base_price: float, tax_rate: float, quantity: int) -> float:
        return calculate_price(base_price, discount_rate, tax_rate, quantity)
    return calculator


def create_standard_pricer(tax_rate: float) -> Callable[[float, float, int], float]:
    """Create a standard pricing calculator for a region.

    Args:
        tax_rate: The tax rate for the region.

    Returns:
        A function that takes (base_price, discount_rate, quantity).
    """
    def pricer(base_price: float, discount_rate: float, quantity: int) -> float:
        return calculate_price(base_price, discount_rate, tax_rate, quantity)
    return pricer


def create_bulk_pricer(min_qty: int, bulk_discount: float) -> Callable[[float, float, float, int], float | None]:
    """Create a pricer that applies bulk discount only for minimum quantity.

    Args:
        min_qty: Minimum quantity to qualify for bulk discount.
        bulk_discount: Additional discount for bulk purchases.

    Returns:
        A function that returns price or None if below minimum.
    """
    def pricer(base_price: float, discount_rate: float, tax_rate: float, quantity: int) -> float | None:
        if quantity < min_qty:
            return None
        # Apply bulk discount in addition to regular discount
        total_discount = discount_rate + bulk_discount
        # Cap total discount at 100%
        total_discount = min(total_discount, 1.0)
        return calculate_price(base_price, total_discount, tax_rate, quantity)

    return pricer

"""Problem 04: Shopping Cart Refactor

Topic: Refactoring Dict-Based to Class-Based
Difficulty: Medium

Refactor a dictionary-based shopping cart into an encapsulated class design.

BEFORE (Dict-Based):
    cart = create_cart()
    add_to_cart(cart, "SKU123", "Widget", 29.99, 2)
    cart["items"][0]["quantity"] = 5  # Direct mutation!
    total = cart["total"]

AFTER (OOP):
    cart = ShoppingCart()
    cart.add_item("SKU123", "Widget", 29.99, 2)
    # No direct access - use methods
    total = cart.total

Your task:
1. Create Product as a value object
2. Create LineItem to represent cart line items
3. Create ShoppingCart with proper encapsulation
4. Prevent direct state manipulation
5. Support cart operations: add, remove, update, clear
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self


# ============================================================================
# PROCEDURAL CODE (Before) - DO NOT MODIFY
# ============================================================================

def create_cart_procedural() -> dict:
    """Create a new shopping cart as dictionary."""
    return {"items": [], "subtotal": 0.0, "tax": 0.0, "total": 0.0}


def add_to_cart_procedural(
    cart: dict,
    sku: str,
    name: str,
    price: float,
    quantity: int,
) -> None:
    """Add item to cart dictionary."""
    # Check if item already exists
    for item in cart["items"]:
        if item["sku"] == sku:
            item["quantity"] += quantity
            item["line_total"] = item["price"] * item["quantity"]
            _recalculate_cart_procedural(cart)
            return
    
    # Add new item
    cart["items"].append({
        "sku": sku,
        "name": name,
        "price": price,
        "quantity": quantity,
        "line_total": price * quantity,
    })
    _recalculate_cart_procedural(cart)


def remove_from_cart_procedural(cart: dict, sku: str) -> bool:
    """Remove item from cart by SKU."""
    for i, item in enumerate(cart["items"]):
        if item["sku"] == sku:
            cart["items"].pop(i)
            _recalculate_cart_procedural(cart)
            return True
    return False


def update_quantity_procedural(cart: dict, sku: str, quantity: int) -> bool:
    """Update quantity for an item."""
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")
    
    for item in cart["items"]:
        if item["sku"] == sku:
            if quantity == 0:
                remove_from_cart_procedural(cart, sku)
            else:
                item["quantity"] = quantity
                item["line_total"] = item["price"] * quantity
                _recalculate_cart_procedural(cart)
            return True
    return False


def _recalculate_cart_procedural(cart: dict) -> None:
    """Recalculate cart totals."""
    cart["subtotal"] = sum(item["line_total"] for item in cart["items"])
    cart["tax"] = cart["subtotal"] * 0.08  # 8% tax
    cart["total"] = cart["subtotal"] + cart["tax"]


def get_cart_summary_procedural(cart: dict) -> dict:
    """Get cart summary."""
    return {
        "item_count": len(cart["items"]),
        "total_quantity": sum(item["quantity"] for item in cart["items"]),
        "subtotal": cart["subtotal"],
        "tax": cart["tax"],
        "total": cart["total"],
    }


def format_cart_procedural(cart: dict) -> str:
    """Format cart as string."""
    lines = ["Shopping Cart:", "-" * 50]
    for item in cart["items"]:
        lines.append(
            f"  {item['sku']}: {item['name']} - "
            f"{item['quantity']} x ${item['price']:.2f} = "
            f"${item['line_total']:.2f}"
        )
    lines.append("-" * 50)
    lines.append(f"Subtotal: ${cart['subtotal']:.2f}")
    lines.append(f"Tax (8%): ${cart['tax']:.2f}")
    lines.append(f"Total: ${cart['total']:.2f}")
    return "\n".join(lines)


# ============================================================================
# YOUR IMPLEMENTATION (After) - TODO: Implement these classes
# ============================================================================


@dataclass(frozen=True)
class Product:
    """Value object representing a product.
    
    Attributes:
        sku: Stock keeping unit (unique identifier)
        name: Product name
        price: Unit price (must be >= 0)
    
    TODO:
    1. Define fields with frozen=True
    2. Validate price >= 0 in __post_init__
    """
    
    def __post_init__(self) -> None:
        """TODO: Validate price >= 0."""
        raise NotImplementedError("Implement validation")


@dataclass
class LineItem:
    """Represents a line item in the cart.
    
    Attributes:
        product: The Product
        quantity: Number of units (must be > 0)
    
    TODO:
    1. Define fields
    2. Add __post_init__ validation for quantity > 0
    3. Implement line_total property
    4. Implement update_quantity method that returns new LineItem
    """
    
    def __post_init__(self) -> None:
        """TODO: Validate quantity > 0."""
        raise NotImplementedError("Implement validation")
    
    @property
    def line_total(self) -> float:
        """TODO: Return product.price * quantity."""
        raise NotImplementedError("Implement line_total")
    
    def update_quantity(self, new_quantity: int) -> LineItem:
        """TODO: Return new LineItem with updated quantity.
        
        Used for immutable updates.
        """
        raise NotImplementedError("Implement update_quantity")
    
    def __str__(self) -> str:
        """TODO: Return formatted: 'SKU: Name - Q x $Price = $Total'."""
        raise NotImplementedError("Implement __str__")


class ShoppingCart:
    """Shopping cart with encapsulated state.
    
    Replaces the dict-based cart with proper encapsulation.
    
    Class Attributes:
        TAX_RATE: Sales tax rate (0.08 = 8%)
    
    TODO:
    1. Initialize empty _items dict (sku -> LineItem)
    2. Implement properties: items, subtotal, tax, total
    3. Implement methods: add_item, remove_item, update_quantity
    4. Implement clear, get_summary, format
    """
    
    TAX_RATE = 0.08
    
    def __init__(self) -> None:
        """TODO: Initialize with empty items dict."""
        raise NotImplementedError("Implement __init__")
    
    @property
    def items(self) -> tuple[LineItem, ...]:
        """TODO: Return immutable view of line items."""
        raise NotImplementedError("Implement items property")
    
    @property
    def subtotal(self) -> float:
        """TODO: Return sum of all line totals."""
        raise NotImplementedError("Implement subtotal")
    
    @property
    def tax(self) -> float:
        """TODO: Return tax amount (subtotal * TAX_RATE)."""
        raise NotImplementedError("Implement tax")
    
    @property
    def total(self) -> float:
        """TODO: Return final total (subtotal + tax)."""
        raise NotImplementedError("Implement total")
    
    @property
    def item_count(self) -> int:
        """TODO: Return number of unique items (SKUs)."""
        raise NotImplementedError("Implement item_count")
    
    @property
    def total_quantity(self) -> int:
        """TODO: Return sum of all quantities."""
        raise NotImplementedError("Implement total_quantity")
    
    def add_item(
        self,
        sku: str,
        name: str,
        price: float,
        quantity: int,
    ) -> Self:
        """TODO: Add item to cart.
        
        If SKU exists, increment quantity.
        If new, create Product and LineItem.
        Returns self for chaining.
        """
        raise NotImplementedError("Implement add_item")
    
    def remove_item(self, sku: str) -> bool:
        """TODO: Remove item by SKU.
        
        Returns True if found and removed, False otherwise.
        """
        raise NotImplementedError("Implement remove_item")
    
    def update_quantity(self, sku: str, quantity: int) -> bool:
        """TODO: Update quantity for item.
        
        If quantity <= 0, remove the item.
        Returns True if SKU found, False otherwise.
        Raises ValueError if quantity < 0.
        """
        raise NotImplementedError("Implement update_quantity")
    
    def clear(self) -> Self:
        """TODO: Remove all items from cart. Returns self."""
        raise NotImplementedError("Implement clear")
    
    def has_item(self, sku: str) -> bool:
        """TODO: Check if SKU is in cart."""
        raise NotImplementedError("Implement has_item")
    
    def get_line_item(self, sku: str) -> LineItem | None:
        """TODO: Get LineItem by SKU or None."""
        raise NotImplementedError("Implement get_line_item")
    
    def get_summary(self) -> dict[str, float | int]:
        """TODO: Return summary dict with:
        - item_count
        - total_quantity
        - subtotal
        - tax
        - total
        """
        raise NotImplementedError("Implement get_summary")
    
    def format(self) -> str:
        """TODO: Format cart as string matching procedural output."""
        raise NotImplementedError("Implement format")
    
    def __str__(self) -> str:
        """TODO: Delegate to format()."""
        raise NotImplementedError("Implement __str__")
    
    def __len__(self) -> int:
        """TODO: Return item_count."""
        raise NotImplementedError("Implement __len__")
    
    def __bool__(self) -> bool:
        """TODO: Return True if cart has items."""
        raise NotImplementedError("Implement __bool__")

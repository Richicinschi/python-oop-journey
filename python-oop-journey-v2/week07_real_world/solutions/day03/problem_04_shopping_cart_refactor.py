"""Reference solution for Problem 04: Shopping Cart Refactor."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self


# ============================================================================
# PROCEDURAL CODE (Before) - Kept for reference
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
    for item in cart["items"]:
        if item["sku"] == sku:
            item["quantity"] += quantity
            item["line_total"] = item["price"] * item["quantity"]
            _recalculate_cart_procedural(cart)
            return
    
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
    cart["tax"] = cart["subtotal"] * 0.08
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
# OOP IMPLEMENTATION (After)
# ============================================================================


@dataclass(frozen=True)
class Product:
    """Value object representing a product."""
    
    sku: str
    name: str
    price: float
    
    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError(f"Price cannot be negative: {self.price}")


@dataclass
class LineItem:
    """Represents a line item in the cart."""
    
    product: Product
    quantity: int
    
    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(f"Quantity must be positive: {self.quantity}")
    
    @property
    def line_total(self) -> float:
        return self.product.price * self.quantity
    
    def update_quantity(self, new_quantity: int) -> LineItem:
        """Return new LineItem with updated quantity."""
        return LineItem(self.product, new_quantity)
    
    def __str__(self) -> str:
        return (
            f"{self.product.sku}: {self.product.name} - "
            f"{self.quantity} x ${self.product.price:.2f} = "
            f"${self.line_total:.2f}"
        )


class ShoppingCart:
    """Shopping cart with encapsulated state."""
    
    TAX_RATE = 0.08
    
    def __init__(self) -> None:
        self._items: dict[str, LineItem] = {}
    
    @property
    def items(self) -> tuple[LineItem, ...]:
        return tuple(self._items.values())
    
    @property
    def subtotal(self) -> float:
        return sum(item.line_total for item in self._items.values())
    
    @property
    def tax(self) -> float:
        return self.subtotal * self.TAX_RATE
    
    @property
    def total(self) -> float:
        return self.subtotal + self.tax
    
    @property
    def item_count(self) -> int:
        return len(self._items)
    
    @property
    def total_quantity(self) -> int:
        return sum(item.quantity for item in self._items.values())
    
    def add_item(
        self,
        sku: str,
        name: str,
        price: float,
        quantity: int,
    ) -> Self:
        """Add item to cart."""
        if sku in self._items:
            # Update existing
            existing = self._items[sku]
            new_quantity = existing.quantity + quantity
            self._items[sku] = existing.update_quantity(new_quantity)
        else:
            # Add new
            product = Product(sku, name, price)
            self._items[sku] = LineItem(product, quantity)
        return self
    
    def remove_item(self, sku: str) -> bool:
        """Remove item by SKU."""
        if sku in self._items:
            del self._items[sku]
            return True
        return False
    
    def update_quantity(self, sku: str, quantity: int) -> bool:
        """Update quantity for item."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        if sku not in self._items:
            return False
        
        if quantity == 0:
            del self._items[sku]
        else:
            existing = self._items[sku]
            self._items[sku] = existing.update_quantity(quantity)
        return True
    
    def clear(self) -> Self:
        """Remove all items from cart."""
        self._items.clear()
        return self
    
    def has_item(self, sku: str) -> bool:
        """Check if SKU is in cart."""
        return sku in self._items
    
    def get_line_item(self, sku: str) -> LineItem | None:
        """Get LineItem by SKU."""
        return self._items.get(sku)
    
    def get_summary(self) -> dict[str, float | int]:
        """Get cart summary."""
        return {
            "item_count": self.item_count,
            "total_quantity": self.total_quantity,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "total": self.total,
        }
    
    def format(self) -> str:
        """Format cart as string."""
        lines = ["Shopping Cart:", "-" * 50]
        for item in self._items.values():
            lines.append(f"  {item}")
        lines.extend([
            "-" * 50,
            f"Subtotal: ${self.subtotal:.2f}",
            f"Tax (8%): ${self.tax:.2f}",
            f"Total: ${self.total:.2f}",
        ])
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return self.format()
    
    def __len__(self) -> int:
        return self.item_count
    
    def __bool__(self) -> bool:
        return self.item_count > 0

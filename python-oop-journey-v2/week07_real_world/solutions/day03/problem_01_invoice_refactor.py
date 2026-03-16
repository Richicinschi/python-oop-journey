"""Reference solution for Problem 01: Invoice System Refactor."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self


# ============================================================================
# PROCEDURAL CODE (Before) - Kept for reference/comparison
# ============================================================================

def create_invoice_procedural(customer_name: str, customer_email: str) -> dict:
    """Create a new invoice as a dictionary."""
    return {
        "customer_name": customer_name,
        "customer_email": customer_email,
        "items": [],
        "subtotal": 0.0,
        "tax": 0.0,
        "total": 0.0,
    }


def add_item_procedural(
    invoice: dict, name: str, quantity: int, unit_price: float
) -> None:
    """Add an item to the invoice dictionary."""
    item = {
        "name": name,
        "quantity": quantity,
        "unit_price": unit_price,
        "line_total": quantity * unit_price,
    }
    invoice["items"].append(item)
    _recalculate_procedural(invoice)


def _recalculate_procedural(invoice: dict) -> None:
    """Recalculate invoice totals."""
    invoice["subtotal"] = sum(item["line_total"] for item in invoice["items"])
    invoice["tax"] = invoice["subtotal"] * 0.10
    invoice["total"] = invoice["subtotal"] + invoice["tax"]


def format_invoice_procedural(invoice: dict) -> str:
    """Format invoice as a string."""
    lines = [f"Invoice for {invoice['customer_name']}", "-" * 40]
    for item in invoice["items"]:
        lines.append(
            f"  {item['name']}: {item['quantity']} x ${item['unit_price']:.2f}"
        )
    lines.extend([
        "-" * 40,
        f"Subtotal: ${invoice['subtotal']:.2f}",
        f"Tax (10%): ${invoice['tax']:.2f}",
        f"Total: ${invoice['total']:.2f}",
    ])
    return "\n".join(lines)


# ============================================================================
# OOP IMPLEMENTATION (After)
# ============================================================================


@dataclass(frozen=True)
class Customer:
    """Value object representing a customer."""
    
    name: str
    email: str
    
    def __post_init__(self) -> None:
        if "@" not in self.email:
            raise ValueError(f"Invalid email address: {self.email}")


@dataclass(frozen=True)
class InvoiceItem:
    """Value object representing a line item on an invoice."""
    
    name: str
    quantity: int
    unit_price: float
    
    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(f"Quantity must be positive, got {self.quantity}")
        if self.unit_price < 0:
            raise ValueError(f"Unit price cannot be negative, got {self.unit_price}")
    
    @property
    def line_total(self) -> float:
        return self.quantity * self.unit_price
    
    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} x ${self.unit_price:.2f}"


class Invoice:
    """Invoice entity with encapsulated state."""
    
    TAX_RATE = 0.10
    
    def __init__(self, customer: Customer) -> None:
        self._customer = customer
        self._items: list[InvoiceItem] = []
        self._subtotal: float = 0.0
        self._tax: float = 0.0
        self._total: float = 0.0
    
    @property
    def customer(self) -> Customer:
        return self._customer
    
    @property
    def items(self) -> tuple[InvoiceItem, ...]:
        return tuple(self._items)
    
    @property
    def subtotal(self) -> float:
        return self._subtotal
    
    @property
    def tax(self) -> float:
        return self._tax
    
    @property
    def total(self) -> float:
        return self._total
    
    def add_item(self, name: str, quantity: int, unit_price: float) -> Self:
        item = InvoiceItem(name, quantity, unit_price)
        self._items.append(item)
        self._recalculate()
        return self
    
    def remove_item(self, index: int) -> Self:
        if 0 <= index < len(self._items):
            self._items.pop(index)
            self._recalculate()
        return self
    
    def _recalculate(self) -> None:
        self._subtotal = sum(item.line_total for item in self._items)
        self._tax = self._subtotal * self.TAX_RATE
        self._total = self._subtotal + self._tax
    
    def format(self) -> str:
        lines = [f"Invoice for {self._customer.name}", "-" * 40]
        for item in self._items:
            lines.append(f"  {item}")
        lines.extend([
            "-" * 40,
            f"Subtotal: ${self._subtotal:.2f}",
            f"Tax (10%): ${self._tax:.2f}",
            f"Total: ${self._total:.2f}",
        ])
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return self.format()


def create_invoice(customer: Customer) -> Invoice:
    """Factory function to create a new invoice."""
    return Invoice(customer)

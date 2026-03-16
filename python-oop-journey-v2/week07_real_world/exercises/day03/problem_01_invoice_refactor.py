"""Problem 01: Invoice System Refactor

Topic: Refactoring Procedural to OOP
Difficulty: Medium

Refactor a procedural invoice system into an object-oriented design.

BEFORE (Procedural):
    invoice = create_invoice("John Doe", "john@example.com")
    add_item(invoice, "Widget", 2, 29.99)
    total = calculate_total(invoice)

AFTER (OOP):
    customer = Customer("John Doe", "john@example.com")
    invoice = Invoice(customer)
    invoice.add_item("Widget", 2, 29.99)
    total = invoice.total

Your task:
1. Create InvoiceItem as a value object with validation
2. Create Customer as a value object with email validation
3. Create Invoice class with encapsulated state
4. Ensure proper validation and immutability where appropriate
5. Support method chaining for fluent interface
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self


# ============================================================================
# PROCEDURAL CODE (Before) - DO NOT MODIFY
# This shows what we're refactoring FROM
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
    invoice["tax"] = invoice["subtotal"] * 0.10  # 10% tax
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
# YOUR IMPLEMENTATION (After) - TODO: Implement these classes
# ============================================================================


@dataclass(frozen=True)
class Customer:
    """Value object representing a customer.
    
    Must validate that email contains '@' character.
    
    Attributes:
        name: Customer's full name
        email: Customer's email address (must contain '@')
    """
    
    name: str
    email: str
    
    def __post_init__(self) -> None:
        """TODO: Validate email contains '@'."""
        raise NotImplementedError("Implement email validation")


@dataclass(frozen=True)
class InvoiceItem:
    """Value object representing a line item on an invoice.
    
    Must validate:
    - quantity > 0
    - unit_price >= 0
    
    Attributes:
        name: Item name
        quantity: Number of items (must be positive)
        unit_price: Price per item (must be non-negative)
    """
    
    name: str
    quantity: int
    unit_price: float
    
    def __post_init__(self) -> None:
        """TODO: Validate quantity > 0 and unit_price >= 0."""
        raise NotImplementedError("Implement validation")
    
    @property
    def line_total(self) -> float:
        """TODO: Calculate and return quantity * unit_price."""
        raise NotImplementedError("Implement line_total property")
    
    def __str__(self) -> str:
        """TODO: Return formatted string: 'name: quantity x $price'."""
        raise NotImplementedError("Implement __str__")


class Invoice:
    """Invoice entity with encapsulated state.
    
    Manages invoice items, calculates subtotal/tax/total automatically.
    Provides immutable view of items through the items property.
    
    Attributes:
        TAX_RATE: Class constant for tax calculation (0.10 = 10%)
        customer: The customer this invoice belongs to
        items: Tuple of InvoiceItem (read-only)
        subtotal: Sum of all line totals
        tax: Tax amount based on subtotal
        total: Final amount (subtotal + tax)
    """
    
    TAX_RATE = 0.10
    
    def __init__(self, customer: Customer) -> None:
        """TODO: Initialize invoice with customer, empty items list, zero totals."""
        raise NotImplementedError("Implement __init__")
    
    @property
    def customer(self) -> Customer:
        """TODO: Return the customer."""
        raise NotImplementedError("Implement customer property")
    
    @property
    def items(self) -> tuple[InvoiceItem, ...]:
        """TODO: Return tuple copy of items (immutable view)."""
        raise NotImplementedError("Implement items property")
    
    @property
    def subtotal(self) -> float:
        """TODO: Return current subtotal."""
        raise NotImplementedError("Implement subtotal property")
    
    @property
    def tax(self) -> float:
        """TODO: Return current tax amount."""
        raise NotImplementedError("Implement tax property")
    
    @property
    def total(self) -> float:
        """TODO: Return current total."""
        raise NotImplementedError("Implement total property")
    
    def add_item(self, name: str, quantity: int, unit_price: float) -> Self:
        """TODO: Add an item to the invoice and return self for chaining.
        
        Should:
        1. Create InvoiceItem with validation
        2. Add to internal items list
        3. Recalculate totals
        4. Return self
        """
        raise NotImplementedError("Implement add_item")
    
    def remove_item(self, index: int) -> Self:
        """TODO: Remove item at index if valid, return self for chaining.
        
        Should:
        1. Check if index is valid (0 <= index < len(items))
        2. Remove item if valid
        3. Recalculate totals
        4. Return self
        """
        raise NotImplementedError("Implement remove_item")
    
    def _recalculate(self) -> None:
        """TODO: Recalculate subtotal, tax, and total.
        
        Private method called internally after modifications.
        """
        raise NotImplementedError("Implement _recalculate")
    
    def format(self) -> str:
        """TODO: Format invoice as string matching procedural output format.
        
        Format:
        Invoice for {customer.name}
        ----------------------------------------
          {item1}
          {item2}
        ----------------------------------------
        Subtotal: $XX.XX
        Tax (10%): $XX.XX
        Total: $XX.XX
        """
        raise NotImplementedError("Implement format")
    
    def __str__(self) -> str:
        """TODO: Return formatted invoice (delegate to format())."""
        raise NotImplementedError("Implement __str__")


# ============================================================================
# HELPER FUNCTION - For compatibility during migration
# ============================================================================

def create_invoice(customer: Customer) -> Invoice:
    """Factory function to create a new invoice.
    
    This provides a clean API similar to the procedural version.
    """
    raise NotImplementedError("Implement create_invoice factory function")

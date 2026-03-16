"""Tests for Problem 01: Invoice System Refactor."""

from __future__ import annotations

import pytest

from week07_real_world.solutions.day03.problem_01_invoice_refactor import (
    Customer,
    Invoice,
    InvoiceItem,
    create_invoice,
    create_invoice_procedural,
    add_item_procedural,
    format_invoice_procedural,
)


class TestCustomer:
    """Tests for Customer value object."""
    
    def test_valid_customer(self) -> None:
        customer = Customer("John Doe", "john@example.com")
        assert customer.name == "John Doe"
        assert customer.email == "john@example.com"
    
    def test_invalid_email_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid email"):
            Customer("John Doe", "invalid-email")
    
    def test_empty_email_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid email"):
            Customer("John Doe", "")
    
    def test_immutable(self) -> None:
        customer = Customer("John", "john@example.com")
        with pytest.raises(AttributeError):
            customer.name = "Jane"


class TestInvoiceItem:
    """Tests for InvoiceItem value object."""
    
    def test_valid_item(self) -> None:
        item = InvoiceItem("Widget", 2, 29.99)
        assert item.name == "Widget"
        assert item.quantity == 2
        assert item.unit_price == 29.99
    
    def test_line_total_calculation(self) -> None:
        item = InvoiceItem("Gadget", 3, 10.00)
        assert item.line_total == 30.00
    
    def test_zero_quantity_raises(self) -> None:
        with pytest.raises(ValueError, match="Quantity must be positive"):
            InvoiceItem("Widget", 0, 10.00)
    
    def test_negative_quantity_raises(self) -> None:
        with pytest.raises(ValueError, match="Quantity must be positive"):
            InvoiceItem("Widget", -1, 10.00)
    
    def test_negative_price_raises(self) -> None:
        with pytest.raises(ValueError, match="Unit price cannot be negative"):
            InvoiceItem("Widget", 1, -10.00)
    
    def test_zero_price_allowed(self) -> None:
        item = InvoiceItem("Free Item", 1, 0.0)
        assert item.unit_price == 0.0
        assert item.line_total == 0.0
    
    def test_str_formatting(self) -> None:
        item = InvoiceItem("Widget", 2, 29.99)
        assert str(item) == "Widget: 2 x $29.99"
    
    def test_immutable(self) -> None:
        item = InvoiceItem("Widget", 1, 10.00)
        with pytest.raises(AttributeError):
            item.name = "Changed"


class TestInvoice:
    """Tests for Invoice entity."""
    
    def test_init(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = Invoice(customer)
        assert invoice.customer == customer
        assert invoice.items == ()
        assert invoice.subtotal == 0.0
        assert invoice.tax == 0.0
        assert invoice.total == 0.0
    
    def test_add_item_updates_totals(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = Invoice(customer)
        invoice.add_item("Widget", 2, 10.00)
        
        assert len(invoice.items) == 1
        assert invoice.subtotal == 20.00
        assert invoice.tax == 2.00  # 10%
        assert invoice.total == 22.00
    
    def test_add_item_returns_self_for_chaining(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = Invoice(customer)
        result = invoice.add_item("A", 1, 10.0)
        assert result is invoice
    
    def test_chained_add_items(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = (
            Invoice(customer)
            .add_item("Widget", 2, 10.00)
            .add_item("Gadget", 1, 20.00)
        )
        
        assert len(invoice.items) == 2
        assert invoice.subtotal == 40.00
        assert invoice.tax == 4.00
        assert invoice.total == 44.00
    
    def test_items_is_immutable_view(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = Invoice(customer)
        invoice.add_item("Widget", 1, 10.0)
        
        items = invoice.items
        assert isinstance(items, tuple)
        # Cannot modify the tuple
        with pytest.raises(TypeError):
            items[0] = None  # type: ignore
    
    def test_remove_item_valid_index(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = Invoice(customer)
        invoice.add_item("Widget", 1, 10.0)
        invoice.add_item("Gadget", 1, 20.0)
        
        invoice.remove_item(0)
        
        assert len(invoice.items) == 1
        assert invoice.items[0].name == "Gadget"
        assert invoice.subtotal == 20.0
    
    def test_remove_item_invalid_index_ignored(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = Invoice(customer)
        invoice.add_item("Widget", 1, 10.0)
        
        invoice.remove_item(5)  # Out of bounds
        
        assert len(invoice.items) == 1
    
    def test_remove_item_returns_self(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = Invoice(customer)
        result = invoice.remove_item(0)
        assert result is invoice
    
    def test_empty_invoice_format(self) -> None:
        customer = Customer("John Doe", "john@example.com")
        invoice = Invoice(customer)
        formatted = invoice.format()
        
        assert "Invoice for John Doe" in formatted
        assert "Subtotal: $0.00" in formatted
        assert "Tax (10%): $0.00" in formatted
        assert "Total: $0.00" in formatted
    
    def test_invoice_format_with_items(self) -> None:
        customer = Customer("John Doe", "john@example.com")
        invoice = Invoice(customer)
        invoice.add_item("Widget", 2, 29.99)
        invoice.add_item("Gadget", 1, 49.99)
        
        formatted = invoice.format()
        
        assert "Invoice for John Doe" in formatted
        assert "Widget: 2 x $29.99" in formatted
        assert "Gadget: 1 x $49.99" in formatted
        assert "Subtotal: $109.97" in formatted
        # Tax is rounded: 10.997 → 11.00
        assert "Tax (10%): $11.00" in formatted
        assert "Total: $120.97" in formatted  # Rounded
    
    def test_str_delegates_to_format(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = Invoice(customer)
        assert str(invoice) == invoice.format()


class TestCreateInvoiceFactory:
    """Tests for factory function."""
    
    def test_factory_creates_invoice(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = create_invoice(customer)
        
        assert isinstance(invoice, Invoice)
        assert invoice.customer == customer


class TestProceduralCompatibility:
    """Tests ensuring procedural code produces same results as OOP."""
    
    def test_procedural_vs_oop_totals(self) -> None:
        # Procedural
        proc_invoice = create_invoice_procedural("John", "john@example.com")
        add_item_procedural(proc_invoice, "Widget", 2, 29.99)
        add_item_procedural(proc_invoice, "Gadget", 1, 49.99)
        
        # OOP
        customer = Customer("John", "john@example.com")
        oop_invoice = Invoice(customer)
        oop_invoice.add_item("Widget", 2, 29.99)
        oop_invoice.add_item("Gadget", 1, 49.99)
        
        assert proc_invoice["subtotal"] == pytest.approx(oop_invoice.subtotal)
        assert proc_invoice["tax"] == pytest.approx(oop_invoice.tax)
        assert proc_invoice["total"] == pytest.approx(oop_invoice.total)
    
    def test_procedural_vs_oop_formatting(self) -> None:
        # Procedural
        proc_invoice = create_invoice_procedural("John Doe", "john@example.com")
        add_item_procedural(proc_invoice, "Widget", 2, 29.99)
        proc_formatted = format_invoice_procedural(proc_invoice)
        
        # OOP
        customer = Customer("John Doe", "john@example.com")
        oop_invoice = Invoice(customer)
        oop_invoice.add_item("Widget", 2, 29.99)
        oop_formatted = oop_invoice.format()
        
        assert "Invoice for John Doe" in proc_formatted
        assert "Invoice for John Doe" in oop_formatted
        assert "Widget: 2 x $29.99" in proc_formatted
        assert "Widget: 2 x $29.99" in oop_formatted


class TestValidation:
    """Tests for validation behavior."""
    
    def test_invalid_item_in_add_item_raises(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = Invoice(customer)
        
        with pytest.raises(ValueError):
            invoice.add_item("Bad", 0, 10.0)  # Invalid quantity
    
    def test_multiple_items_recalculate_correctly(self) -> None:
        customer = Customer("John", "john@example.com")
        invoice = Invoice(customer)
        
        for i in range(10):
            invoice.add_item(f"Item{i}", 1, float(i))
        
        expected_subtotal = sum(float(i) for i in range(10))  # 45.0
        expected_tax = expected_subtotal * 0.10
        expected_total = expected_subtotal + expected_tax
        
        assert invoice.subtotal == pytest.approx(expected_subtotal)
        assert invoice.tax == pytest.approx(expected_tax)
        assert invoice.total == pytest.approx(expected_total)

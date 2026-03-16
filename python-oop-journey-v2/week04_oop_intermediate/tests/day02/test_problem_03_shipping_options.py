"""Tests for Problem 03: Shipping Options."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day02.problem_03_shipping_options import (
    ExpressShipping,
    InternationalShipping,
    Shipping,
    StandardShipping,
)


class TestShipping:
    """Tests for Shipping base class."""

    def test_init_sets_attributes(self) -> None:
        """Test that all attributes are set."""
        shipping = Shipping(2.0, "New York", 5.0)
        assert shipping.weight == 2.0
        assert shipping.destination == "New York"
        assert shipping.base_cost == 5.0

    def test_init_validates_weight(self) -> None:
        """Test that non-positive weight raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            Shipping(0, "NY", 5.0)

    def test_init_validates_destination(self) -> None:
        """Test that empty destination raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            Shipping(2.0, "", 5.0)

    def test_calculate_cost_returns_base(self) -> None:
        """Test that base class returns only base cost."""
        shipping = Shipping(2.0, "NY", 5.0)
        assert shipping.calculate_cost() == 5.0

    def test_estimate_days_returns_default(self) -> None:
        """Test that base class returns default estimate."""
        shipping = Shipping(2.0, "NY", 5.0)
        assert shipping.estimate_days() == "3-5 days"

    def test_get_details_returns_dict(self) -> None:
        """Test get_details() returns expected dictionary."""
        shipping = Shipping(2.0, "NY", 5.0)
        details = shipping.get_details()
        assert details["weight"] == 2.0
        assert details["destination"] == "NY"
        assert details["base_cost"] == 5.0
        assert details["cost"] == 5.0
        assert details["days"] == "3-5 days"


class TestStandardShipping:
    """Tests for StandardShipping class."""

    def test_rate_per_kg_constant(self) -> None:
        """Test RATE_PER_KG is 0.50."""
        assert StandardShipping.RATE_PER_KG == 0.50

    def test_calculate_cost_includes_weight(self) -> None:
        """Test cost includes base + weight * rate."""
        shipping = StandardShipping(2.0, "NY", 5.0)
        # 5.0 + (2.0 * 0.50) = 6.0
        assert shipping.calculate_cost() == 6.0

    def test_estimate_days_returns_standard(self) -> None:
        """Test standard shipping returns 5-7 days."""
        shipping = StandardShipping(2.0, "NY", 5.0)
        assert shipping.estimate_days() == "5-7 days"

    def test_get_details_extends_parent(self) -> None:
        """Test get_details() extends parent's dict."""
        shipping = StandardShipping(2.0, "NY", 5.0)
        details = shipping.get_details()
        assert details["method"] == "standard"
        assert details["rate_per_kg"] == 0.50

    def test_inheritance_from_shipping(self) -> None:
        """Test that StandardShipping inherits from Shipping."""
        assert issubclass(StandardShipping, Shipping)


class TestExpressShipping:
    """Tests for ExpressShipping class."""

    def test_rate_per_kg_constant(self) -> None:
        """Test RATE_PER_KG is 1.50."""
        assert ExpressShipping.RATE_PER_KG == 1.50

    def test_tracking_included_constant(self) -> None:
        """Test TRACKING_INCLUDED is True."""
        assert ExpressShipping.TRACKING_INCLUDED is True

    def test_calculate_cost_includes_weight(self) -> None:
        """Test cost includes base + weight * rate."""
        shipping = ExpressShipping(2.0, "NY", 5.0)
        # 5.0 + (2.0 * 1.50) = 8.0
        assert shipping.calculate_cost() == 8.0

    def test_estimate_days_returns_express(self) -> None:
        """Test express shipping returns 1-2 days."""
        shipping = ExpressShipping(2.0, "NY", 5.0)
        assert shipping.estimate_days() == "1-2 days"

    def test_has_tracking_returns_true(self) -> None:
        """Test has_tracking() returns True."""
        shipping = ExpressShipping(2.0, "NY", 5.0)
        assert shipping.has_tracking() is True

    def test_get_details_extends_parent(self) -> None:
        """Test get_details() extends parent's dict."""
        shipping = ExpressShipping(2.0, "NY", 5.0)
        details = shipping.get_details()
        assert details["method"] == "express"
        assert details["tracking"] is True
        assert details["rate_per_kg"] == 1.50

    def test_inheritance_from_shipping(self) -> None:
        """Test that ExpressShipping inherits from Shipping."""
        assert issubclass(ExpressShipping, Shipping)


class TestInternationalShipping:
    """Tests for InternationalShipping class."""

    def test_rate_per_kg_constant(self) -> None:
        """Test RATE_PER_KG is 3.00."""
        assert InternationalShipping.RATE_PER_KG == 3.00

    def test_customs_handling_constant(self) -> None:
        """Test CUSTOMS_HANDLING is True."""
        assert InternationalShipping.CUSTOMS_HANDLING is True

    def test_restricted_destinations_constant(self) -> None:
        """Test RESTRICTED_DESTINATIONS exists."""
        expected = ("North Korea", "Iran", "Syria")
        assert InternationalShipping.RESTRICTED_DESTINATIONS == expected

    def test_init_validates_restricted_destination(self) -> None:
        """Test that restricted destination raises ValueError."""
        with pytest.raises(ValueError, match="restricted"):
            InternationalShipping(2.0, "North Korea", 5.0)

    def test_calculate_cost_includes_weight(self) -> None:
        """Test cost includes base + weight * rate."""
        shipping = InternationalShipping(2.0, "France", 5.0)
        # 5.0 + (2.0 * 3.00) = 11.0
        assert shipping.calculate_cost() == 11.0

    def test_estimate_days_returns_international(self) -> None:
        """Test international shipping returns 7-14 days."""
        shipping = InternationalShipping(2.0, "France", 5.0)
        assert shipping.estimate_days() == "7-14 days"

    def test_requires_customs_returns_true(self) -> None:
        """Test requires_customs() returns True."""
        shipping = InternationalShipping(2.0, "France", 5.0)
        assert shipping.requires_customs() is True

    def test_get_details_extends_parent(self) -> None:
        """Test get_details() extends parent's dict."""
        shipping = InternationalShipping(2.0, "France", 5.0)
        details = shipping.get_details()
        assert details["method"] == "international"
        assert details["customs"] is True
        assert details["rate_per_kg"] == 3.00

    def test_inheritance_from_shipping(self) -> None:
        """Test that InternationalShipping inherits from Shipping."""
        assert issubclass(InternationalShipping, Shipping)

"""Reference solution for Problem 03: Shipping Options."""

from __future__ import annotations


class Shipping:
    """Base shipping class."""

    def __init__(self, weight: float, destination: str, base_cost: float) -> None:
        """Initialize shipping with weight, destination, and base cost.
        
        Args:
            weight: Package weight in kilograms (must be > 0)
            destination: Delivery destination
            base_cost: Base shipping cost
            
        Raises:
            ValueError: If weight <= 0 or destination is empty
        """
        if weight <= 0:
            raise ValueError("Weight must be positive")
        if not destination:
            raise ValueError("Destination cannot be empty")
        self.weight = weight
        self.destination = destination
        self.base_cost = base_cost

    def calculate_cost(self) -> float:
        """Calculate shipping cost.
        
        Returns:
            Base cost only for base class
        """
        return self.base_cost

    def estimate_days(self) -> str:
        """Estimate delivery time.
        
        Returns:
            Delivery time estimate string
        """
        return "3-5 days"

    def get_details(self) -> dict[str, object]:
        """Return shipping details as dictionary."""
        return {
            "weight": self.weight,
            "destination": self.destination,
            "base_cost": self.base_cost,
            "cost": self.calculate_cost(),
            "days": self.estimate_days(),
        }


class StandardShipping(Shipping):
    """Standard shipping option (5-7 days, $0.50/kg)."""

    RATE_PER_KG = 0.50
    DAYS_ESTIMATE = "5-7 days"

    def calculate_cost(self) -> float:
        """Calculate standard shipping cost.
        
        Base cost + (weight * RATE_PER_KG)
        """
        base = super().calculate_cost()
        return base + (self.weight * self.RATE_PER_KG)

    def estimate_days(self) -> str:
        """Return standard delivery estimate."""
        return self.DAYS_ESTIMATE

    def get_details(self) -> dict[str, object]:
        """Return standard shipping details."""
        details = super().get_details()
        details.update({
            "method": "standard",
            "rate_per_kg": self.RATE_PER_KG,
        })
        return details


class ExpressShipping(Shipping):
    """Express shipping option (1-2 days, $1.50/kg, tracking)."""

    RATE_PER_KG = 1.50
    DAYS_ESTIMATE = "1-2 days"
    TRACKING_INCLUDED = True

    def calculate_cost(self) -> float:
        """Calculate express shipping cost."""
        base = super().calculate_cost()
        return base + (self.weight * self.RATE_PER_KG)

    def estimate_days(self) -> str:
        """Return express delivery estimate."""
        return self.DAYS_ESTIMATE

    def has_tracking(self) -> bool:
        """Return whether tracking is included."""
        return self.TRACKING_INCLUDED

    def get_details(self) -> dict[str, object]:
        """Return express shipping details."""
        details = super().get_details()
        details.update({
            "method": "express",
            "tracking": self.TRACKING_INCLUDED,
            "rate_per_kg": self.RATE_PER_KG,
        })
        return details


class InternationalShipping(Shipping):
    """International shipping option (7-14 days, $3.00/kg, customs)."""

    RATE_PER_KG = 3.00
    DAYS_ESTIMATE = "7-14 days"
    CUSTOMS_HANDLING = True

    RESTRICTED_DESTINATIONS: tuple[str, ...] = ("North Korea", "Iran", "Syria")

    def __init__(self, weight: float, destination: str, base_cost: float) -> None:
        """Initialize international shipping with restricted country check.
        
        Raises:
            ValueError: If destination is in RESTRICTED_DESTINATIONS
        """
        if destination in self.RESTRICTED_DESTINATIONS:
            raise ValueError(f"Shipping to {destination} is restricted")
        super().__init__(weight, destination, base_cost)

    def calculate_cost(self) -> float:
        """Calculate international shipping cost."""
        base = super().calculate_cost()
        return base + (self.weight * self.RATE_PER_KG)

    def estimate_days(self) -> str:
        """Return international delivery estimate."""
        return self.DAYS_ESTIMATE

    def requires_customs(self) -> bool:
        """Return whether customs handling is required."""
        return self.CUSTOMS_HANDLING

    def get_details(self) -> dict[str, object]:
        """Return international shipping details."""
        details = super().get_details()
        details.update({
            "method": "international",
            "customs": self.CUSTOMS_HANDLING,
            "rate_per_kg": self.RATE_PER_KG,
        })
        return details

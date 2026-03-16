"""Problem 03: Shipping Options

Topic: Overriding calculation methods with super()
Difficulty: Medium

Create a shipping option hierarchy where child classes override cost calculation
and delivery estimation methods, using super() to build upon base behavior.

Classes to implement:
- Shipping: Base class with weight, destination, base_cost
- StandardShipping: Base + $0.50 per kg, 5-7 days
- ExpressShipping: Base + $1.50 per kg, 1-2 days, tracking included
- InternationalShipping: Base + $3.00 per kg, 7-14 days, customs handling

Example:
    >>> base = Shipping(2.0, "New York", 5.0)
    >>> base.calculate_cost()
    5.0
    >>> base.estimate_days()
    '3-5 days'
    
    >>> standard = StandardShipping(2.0, "New York", 5.0)
    >>> standard.calculate_cost()
    6.0  # 5.0 + (2.0 * 0.50)
    >>> standard.estimate_days()
    '5-7 days'

Requirements:
    - Shipping: weight (kg), destination (str), base_cost (float)
    - calculate_cost(): Returns total shipping cost
    - estimate_days(): Returns delivery time estimate string
    - get_details(): Returns shipping details dict
    - Child classes override calculate_cost() adding to parent's result
    - Child classes override estimate_days() completely
    - Child classes extend get_details() via super()
"""

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
        raise NotImplementedError("Initialize all attributes with validation")

    def calculate_cost(self) -> float:
        """Calculate shipping cost.
        
        Returns:
            Base cost only for base class
        """
        raise NotImplementedError("Return base_cost")

    def estimate_days(self) -> str:
        """Estimate delivery time.
        
        Returns:
            Delivery time estimate string
        """
        raise NotImplementedError("Return '3-5 days'")

    def get_details(self) -> dict[str, object]:
        """Return shipping details as dictionary.
        
        Returns dict with: weight, destination, base_cost, cost, days
        """
        raise NotImplementedError("Return complete shipping details")


class StandardShipping(Shipping):
    """Standard shipping option (5-7 days, $0.50/kg)."""

    RATE_PER_KG = 0.50
    DAYS_ESTIMATE = "5-7 days"

    def calculate_cost(self) -> float:
        """Calculate standard shipping cost.
        
        Base cost + (weight * RATE_PER_KG)
        """
        raise NotImplementedError("Use super().calculate_cost() and add weight cost")

    def estimate_days(self) -> str:
        """Return standard delivery estimate."""
        raise NotImplementedError("Return DAYS_ESTIMATE")

    def get_details(self) -> dict[str, object]:
        """Return standard shipping details.
        
        Extends parent with: method='standard', rate_per_kg
        """
        raise NotImplementedError("Extend with super()")


class ExpressShipping(Shipping):
    """Express shipping option (1-2 days, $1.50/kg, tracking)."""

    RATE_PER_KG = 1.50
    DAYS_ESTIMATE = "1-2 days"
    TRACKING_INCLUDED = True

    def calculate_cost(self) -> float:
        """Calculate express shipping cost.
        
        Base cost + (weight * RATE_PER_KG)
        """
        raise NotImplementedError("Use super().calculate_cost() and add weight cost")

    def estimate_days(self) -> str:
        """Return express delivery estimate."""
        raise NotImplementedError("Return DAYS_ESTIMATE")

    def has_tracking(self) -> bool:
        """Return whether tracking is included."""
        raise NotImplementedError("Return TRACKING_INCLUDED")

    def get_details(self) -> dict[str, object]:
        """Return express shipping details.
        
        Extends parent with: method='express', tracking, rate_per_kg
        """
        raise NotImplementedError("Extend with super()")


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
        raise NotImplementedError("Use super().__init__() and check restrictions")

    def calculate_cost(self) -> float:
        """Calculate international shipping cost.
        
        Base cost + (weight * RATE_PER_KG)
        """
        raise NotImplementedError("Use super().calculate_cost() and add weight cost")

    def estimate_days(self) -> str:
        """Return international delivery estimate."""
        raise NotImplementedError("Return DAYS_ESTIMATE")

    def requires_customs(self) -> bool:
        """Return whether customs handling is required."""
        raise NotImplementedError("Return CUSTOMS_HANDLING")

    def get_details(self) -> dict[str, object]:
        """Return international shipping details.
        
        Extends parent with: method='international', customs, rate_per_kg
        """
        raise NotImplementedError("Extend with super()")

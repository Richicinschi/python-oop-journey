"""Service layer for business logic.

Contains core business operations using design patterns:
- Strategy pattern for search and fine calculation
- Observer pattern for event notifications
- Factory pattern for entity creation
"""

from .catalog_service import CatalogService, SearchStrategy
from .circulation_service import CirculationService, EventBus, CirculationEvent
from .reservation_service import ReservationService
from .fine_service import FineService, FineCalculationStrategy

__all__ = [
    "CatalogService",
    "SearchStrategy",
    "CirculationService",
    "EventBus",
    "CirculationEvent",
    "ReservationService",
    "FineService",
    "FineCalculationStrategy",
]

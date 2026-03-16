"""Reference solution for Problem 05: Contract-Style Interface Tests."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Product:
    """Product information for inventory operations."""
    id: str
    name: str
    sku: str
    unit_cost: Decimal


@dataclass
class InventoryItem:
    """Represents a quantity of product in inventory."""
    product: Product
    quantity: int
    location: str


@dataclass
class Reservation:
    """Inventory reservation for an order."""
    id: UUID
    product_id: str
    quantity: int
    order_id: str
    status: str


class InsufficientStockError(Exception):
    """Raised when requested quantity exceeds available stock."""
    pass


class ProductNotFoundError(Exception):
    """Raised when a product cannot be found."""
    pass


class ReservationNotFoundError(Exception):
    """Raised when a reservation cannot be found."""
    pass


class InvalidOperationError(Exception):
    """Raised when an invalid operation is attempted."""
    pass


class InventoryRepository(ABC):
    """Abstract interface for inventory storage operations."""
    
    @abstractmethod
    def find_by_product_id(self, product_id: str) -> Optional[InventoryItem]:
        """Find inventory record by product ID."""
        pass
    
    @abstractmethod
    def find_by_sku(self, sku: str) -> Optional[InventoryItem]:
        """Find inventory record by SKU."""
        pass
    
    @abstractmethod
    def update_quantity(self, product_id: str, new_quantity: int) -> InventoryItem:
        """Update available quantity for a product."""
        pass
    
    @abstractmethod
    def reserve(self, product_id: str, quantity: int, order_id: str) -> Reservation:
        """Reserve inventory for an order."""
        pass
    
    @abstractmethod
    def release_reservation(self, reservation_id: UUID) -> InventoryItem:
        """Release a reservation, returning stock to available."""
        pass
    
    @abstractmethod
    def confirm_reservation(self, reservation_id: UUID) -> InventoryItem:
        """Confirm a reservation (convert to actual deduction)."""
        pass
    
    @abstractmethod
    def get_all(self) -> list[InventoryItem]:
        """Get all inventory items."""
        pass
    
    @abstractmethod
    def get_reservations_for_order(self, order_id: str) -> list[Reservation]:
        """Get all reservations for an order."""
        pass


class InMemoryInventoryRepository(InventoryRepository):
    """In-memory implementation of inventory repository."""
    
    def __init__(self) -> None:
        """Initialize empty inventory storage."""
        self._inventory: dict[str, InventoryItem] = {}  # product_id -> item
        self._by_sku: dict[str, str] = {}  # sku -> product_id
        self._reservations: dict[UUID, Reservation] = {}
        self._order_reservations: dict[str, list[UUID]] = {}  # order_id -> reservation_ids
    
    def find_by_product_id(self, product_id: str) -> Optional[InventoryItem]:
        """Find by product ID."""
        item = self._inventory.get(product_id)
        return item if item and item.quantity >= 0 else None
    
    def find_by_sku(self, sku: str) -> Optional[InventoryItem]:
        """Find by SKU."""
        product_id = self._by_sku.get(sku)
        if product_id:
            return self.find_by_product_id(product_id)
        return None
    
    def update_quantity(self, product_id: str, new_quantity: int) -> InventoryItem:
        """Update quantity."""
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        item = self._inventory.get(product_id)
        if item is None:
            raise ProductNotFoundError(f"Product {product_id} not found")
        
        # Calculate reserved quantity for this product
        reserved = sum(
            r.quantity for r in self._reservations.values()
            if r.product_id == product_id and r.status == "active"
        )
        
        if new_quantity < reserved:
            raise InsufficientStockError(f"Cannot reduce below reserved quantity ({reserved})")
        
        new_item = InventoryItem(
            product=item.product,
            quantity=new_quantity,
            location=item.location
        )
        self._inventory[product_id] = new_item
        return new_item
    
    def reserve(self, product_id: str, quantity: int, order_id: str) -> Reservation:
        """Create reservation."""
        if quantity <= 0:
            raise ValueError("Reservation quantity must be positive")
        
        item = self._inventory.get(product_id)
        if item is None:
            raise ProductNotFoundError(f"Product {product_id} not found")
        
        # Calculate available (total - reserved)
        reserved = sum(
            r.quantity for r in self._reservations.values()
            if r.product_id == product_id and r.status == "active"
        )
        available = item.quantity - reserved
        
        if quantity > available:
            raise InsufficientStockError(
                f"Requested {quantity} but only {available} available"
            )
        
        reservation = Reservation(
            id=uuid4(),
            product_id=product_id,
            quantity=quantity,
            order_id=order_id,
            status="active"
        )
        
        self._reservations[reservation.id] = reservation
        if order_id not in self._order_reservations:
            self._order_reservations[order_id] = []
        self._order_reservations[order_id].append(reservation.id)
        
        return reservation
    
    def release_reservation(self, reservation_id: UUID) -> InventoryItem:
        """Release reservation."""
        reservation = self._reservations.get(reservation_id)
        if reservation is None:
            raise ReservationNotFoundError(f"Reservation {reservation_id} not found")
        
        if reservation.status != "active":
            raise InvalidOperationError(f"Cannot release reservation with status {reservation.status}")
        
        reservation.status = "released"
        return self._inventory[reservation.product_id]
    
    def confirm_reservation(self, reservation_id: UUID) -> InventoryItem:
        """Confirm reservation."""
        reservation = self._reservations.get(reservation_id)
        if reservation is None:
            raise ReservationNotFoundError(f"Reservation {reservation_id} not found")
        
        if reservation.status != "active":
            raise InvalidOperationError(f"Cannot confirm reservation with status {reservation.status}")
        
        # Actually deduct from inventory
        item = self._inventory[reservation.product_id]
        new_quantity = item.quantity - reservation.quantity
        
        new_item = InventoryItem(
            product=item.product,
            quantity=new_quantity,
            location=item.location
        )
        self._inventory[reservation.product_id] = new_item
        reservation.status = "confirmed"
        
        return new_item
    
    def get_all(self) -> list[InventoryItem]:
        """Get all items."""
        return list(self._inventory.values())
    
    def get_reservations_for_order(self, order_id: str) -> list[Reservation]:
        """Get reservations for order."""
        reservation_ids = self._order_reservations.get(order_id, [])
        return [self._reservations[rid] for rid in reservation_ids]
    
    def add_initial_stock(self, item: InventoryItem) -> None:
        """Helper method to seed initial inventory."""
        self._inventory[item.product.id] = item
        self._by_sku[item.product.sku] = item.product.id


class InventoryService:
    """Service layer for inventory operations."""
    
    def __init__(self, repository: InventoryRepository) -> None:
        """Initialize with repository."""
        self._repository = repository
    
    def check_stock(self, product_id: str, required_quantity: int = 1) -> bool:
        """Check if sufficient stock exists."""
        item = self._repository.find_by_product_id(product_id)
        if item is None:
            return False
        return item.quantity >= required_quantity
    
    def allocate_stock(self, product_id: str, quantity: int, order_id: str) -> Reservation:
        """Allocate stock for an order."""
        return self._repository.reserve(product_id, quantity, order_id)
    
    def get_available_quantity(self, product_id: str) -> int:
        """Get available (non-reserved) quantity."""
        item = self._repository.find_by_product_id(product_id)
        return item.quantity if item else 0

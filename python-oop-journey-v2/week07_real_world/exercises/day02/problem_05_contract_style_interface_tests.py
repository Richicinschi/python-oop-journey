"""Problem 05: Contract-Style Interface Tests

Topic: Interface contracts
Difficulty: Medium

Learn to write contract tests that verify all implementations
of an interface satisfy the same behavioral contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Generic, TypeVar, Optional
from uuid import UUID


@dataclass(frozen=True)
class Product:
    """Product information for inventory operations.
    
    Attributes:
        id: Unique product identifier
        name: Product name
        sku: Stock keeping unit
        unit_cost: Cost per unit
    """
    id: str
    name: str
    sku: str
    unit_cost: Decimal


@dataclass
class InventoryItem:
    """Represents a quantity of product in inventory.
    
    Attributes:
        product: The product
        quantity: Units available
        location: Storage location code
    """
    product: Product
    quantity: int
    location: str


@dataclass
class Reservation:
    """Inventory reservation for an order.
    
    Attributes:
        id: Unique reservation ID
        product_id: Reserved product
        quantity: Reserved quantity
        order_id: Associated order
        status: Current reservation status
    """
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


class InventoryRepository(ABC):
    """Abstract interface for inventory storage operations.
    
    This interface defines the contract that all inventory
    repositories must satisfy. Contract tests verify that
    all implementations behave consistently.
    """
    
    @abstractmethod
    def find_by_product_id(self, product_id: str) -> Optional[InventoryItem]:
        """Find inventory record by product ID.
        
        Contract:
        - Returns None if product not found
        - Returns item with quantity >= 0
        - Does not modify state
        
        Args:
            product_id: Product to find
            
        Returns:
            Inventory item or None
        """
        raise NotImplementedError("Implement find_by_product_id")
    
    @abstractmethod
    def find_by_sku(self, sku: str) -> Optional[InventoryItem]:
        """Find inventory record by SKU.
        
        Contract:
        - SKU matching is case-sensitive
        - Returns None if SKU not found
        
        Args:
            sku: SKU to search for
            
        Returns:
            Inventory item or None
        """
        raise NotImplementedError("Implement find_by_sku")
    
    @abstractmethod
    def update_quantity(self, product_id: str, new_quantity: int) -> InventoryItem:
        """Update available quantity for a product.
        
        Contract:
        - Raises ProductNotFoundError if product doesn't exist
        - Raises ValueError if new_quantity < 0
        - Returns updated item
        - Persists change immediately
        
        Args:
            product_id: Product to update
            new_quantity: New quantity value
            
        Returns:
            Updated inventory item
        """
        raise NotImplementedError("Implement update_quantity")
    
    @abstractmethod
    def reserve(self, product_id: str, quantity: int, order_id: str) -> Reservation:
        """Reserve inventory for an order.
        
        Contract:
        - Raises ProductNotFoundError if product unknown
        - Raises InsufficientStockError if quantity > available
        - Raises ValueError if quantity <= 0
        - Creates reservation with 'active' status
        - Reduces available quantity
        - Returns new reservation
        
        Args:
            product_id: Product to reserve
            quantity: Amount to reserve
            order_id: Associated order
            
        Returns:
            New reservation
        """
        raise NotImplementedError("Implement reserve")
    
    @abstractmethod
    def release_reservation(self, reservation_id: UUID) -> InventoryItem:
        """Release a reservation, returning stock to available.
        
        Contract:
        - Raises ReservationNotFoundError if not found
        - Raises InvalidOperationError if already released/cancelled
        - Increases available quantity
        - Updates reservation status to 'released'
        - Returns updated inventory item
        
        Args:
            reservation_id: Reservation to release
            
        Returns:
            Updated inventory item
        """
        raise NotImplementedError("Implement release_reservation")
    
    @abstractmethod
    def confirm_reservation(self, reservation_id: UUID) -> InventoryItem:
        """Confirm a reservation (convert to actual deduction).
        
        Contract:
        - Raises ReservationNotFoundError if not found
        - Updates status to 'confirmed'
        - Quantity remains deducted from inventory
        - Returns updated inventory item
        
        Args:
            reservation_id: Reservation to confirm
            
        Returns:
            Updated inventory item
        """
        raise NotImplementedError("Implement confirm_reservation")
    
    @abstractmethod
    def get_all(self) -> list[InventoryItem]:
        """Get all inventory items.
        
        Contract:
        - Returns empty list if no items
        - Does not modify state
        - Order is not specified (implementation dependent)
        
        Returns:
            List of all inventory items
        """
        raise NotImplementedError("Implement get_all")
    
    @abstractmethod
    def get_reservations_for_order(self, order_id: str) -> list[Reservation]:
        """Get all reservations for an order.
        
        Contract:
        - Returns empty list if no reservations
        - Does not modify state
        
        Args:
            order_id: Order to look up
            
        Returns:
            List of reservations
        """
        raise NotImplementedError("Implement get_reservations_for_order")


class InMemoryInventoryRepository(InventoryRepository):
    """In-memory implementation of inventory repository.
    
    Suitable for testing and small-scale use.
    Not thread-safe.
    
    TODO: Implement this in-memory repository.
    """
    
    def __init__(self) -> None:
        """Initialize empty inventory storage."""
        raise NotImplementedError("Implement __init__")
    
    def find_by_product_id(self, product_id: str) -> Optional[InventoryItem]:
        """Find by product ID."""
        raise NotImplementedError("Implement find_by_product_id")
    
    def find_by_sku(self, sku: str) -> Optional[InventoryItem]:
        """Find by SKU."""
        raise NotImplementedError("Implement find_by_sku")
    
    def update_quantity(self, product_id: str, new_quantity: int) -> InventoryItem:
        """Update quantity."""
        raise NotImplementedError("Implement update_quantity")
    
    def reserve(self, product_id: str, quantity: int, order_id: str) -> Reservation:
        """Create reservation."""
        raise NotImplementedError("Implement reserve")
    
    def release_reservation(self, reservation_id: UUID) -> InventoryItem:
        """Release reservation."""
        raise NotImplementedError("Implement release_reservation")
    
    def confirm_reservation(self, reservation_id: UUID) -> InventoryItem:
        """Confirm reservation."""
        raise NotImplementedError("Implement confirm_reservation")
    
    def get_all(self) -> list[InventoryItem]:
        """Get all items."""
        raise NotImplementedError("Implement get_all")
    
    def get_reservations_for_order(self, order_id: str) -> list[Reservation]:
        """Get reservations for order."""
        raise NotImplementedError("Implement get_reservations_for_order")
    
    def add_initial_stock(self, item: InventoryItem) -> None:
        """Helper method to seed initial inventory (not in interface).
        
        Args:
            item: Item to add
        """
        raise NotImplementedError("Implement add_initial_stock")


class InventoryService:
    """Service layer for inventory operations.
    
    TODO: Implement service methods.
    """
    
    def __init__(self, repository: InventoryRepository) -> None:
        """Initialize with repository.
        
        Args:
            repository: Storage implementation
        """
        raise NotImplementedError("Implement __init__")
    
    def check_stock(self, product_id: str, required_quantity: int = 1) -> bool:
        """Check if sufficient stock exists.
        
        Args:
            product_id: Product to check
            required_quantity: Quantity needed
            
        Returns:
            True if stock >= required
        """
        raise NotImplementedError("Implement check_stock")
    
    def allocate_stock(self, product_id: str, quantity: int, order_id: str) -> Reservation:
        """Allocate stock for an order.
        
        Args:
            product_id: Product to allocate
            quantity: Amount needed
            order_id: Associated order
            
        Returns:
            Created reservation
        """
        raise NotImplementedError("Implement allocate_stock")
    
    def get_available_quantity(self, product_id: str) -> int:
        """Get available (non-reserved) quantity.
        
        Args:
            product_id: Product to check
            
        Returns:
            Available quantity (0 if not found)
        """
        raise NotImplementedError("Implement get_available_quantity")

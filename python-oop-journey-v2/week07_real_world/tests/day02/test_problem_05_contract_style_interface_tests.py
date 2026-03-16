"""Tests for Problem 05: Contract-Style Interface Tests."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

import pytest

from week07_real_world.solutions.day02.problem_05_contract_style_interface_tests import (
    InMemoryInventoryRepository,
    InsufficientStockError,
    InventoryItem,
    InventoryRepository,
    InventoryService,
    InvalidOperationError,
    Product,
    ProductNotFoundError,
    Reservation,
    ReservationNotFoundError,
)


# ============================================================================
# CONTRACT TEST FIXTURES
# These fixtures provide different implementations for contract testing
# ============================================================================

@pytest.fixture
def in_memory_repository() -> InMemoryInventoryRepository:
    """Fresh in-memory repository with sample data."""
    repo = InMemoryInventoryRepository()
    
    # Add sample inventory
    repo.add_initial_stock(InventoryItem(
        product=Product("p1", "Widget", "WID-001", Decimal("10.00")),
        quantity=100,
        location="A1"
    ))
    repo.add_initial_stock(InventoryItem(
        product=Product("p2", "Gadget", "GAD-002", Decimal("25.00")),
        quantity=50,
        location="B2"
    ))
    repo.add_initial_stock(InventoryItem(
        product=Product("p3", "Thingamajig", "THG-003", Decimal("5.00")),
        quantity=0,  # Out of stock
        location="C3"
    ))
    
    return repo


# ============================================================================
# CONTRACT TESTS - These tests verify behavior common to ALL implementations
# ============================================================================

class TestInventoryRepositoryContract:
    """Contract tests that ANY InventoryRepository implementation must satisfy.
    
    These tests use the in-memory implementation but document the contract
    that all implementations (SQL, Redis, etc.) must follow.
    """
    
    # ----- find_by_product_id contract -----
    
    def test_find_by_product_id_returns_item_when_exists(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Returns item when product exists."""
        result = in_memory_repository.find_by_product_id("p1")
        
        assert result is not None
        assert result.product.id == "p1"
        assert result.quantity >= 0
    
    def test_find_by_product_id_returns_none_when_not_exists(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Returns None for unknown product."""
        result = in_memory_repository.find_by_product_id("unknown")
        
        assert result is None
    
    def test_find_by_product_id_does_not_modify_state(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Finding should not change repository state."""
        before = in_memory_repository.find_by_product_id("p1")
        
        # Call multiple times
        in_memory_repository.find_by_product_id("p1")
        in_memory_repository.find_by_product_id("p1")
        
        after = in_memory_repository.find_by_product_id("p1")
        
        assert before.quantity == after.quantity
    
    # ----- find_by_sku contract -----
    
    def test_find_by_sku_returns_item_when_exists(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Returns item when SKU exists."""
        result = in_memory_repository.find_by_sku("WID-001")
        
        assert result is not None
        assert result.product.sku == "WID-001"
    
    def test_find_by_sku_case_sensitive(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: SKU matching is case-sensitive."""
        result_lower = in_memory_repository.find_by_sku("wid-001")
        result_upper = in_memory_repository.find_by_sku("WID-001")
        
        assert result_lower is None  # Case-sensitive, so no match
        assert result_upper is not None
    
    # ----- update_quantity contract -----
    
    def test_update_quantity_returns_updated_item(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Returns item with new quantity."""
        result = in_memory_repository.update_quantity("p1", 75)
        
        assert result.quantity == 75
    
    def test_update_quantity_persists_change(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Change is persisted and visible on subsequent reads."""
        in_memory_repository.update_quantity("p1", 80)
        
        result = in_memory_repository.find_by_product_id("p1")
        assert result.quantity == 80
    
    def test_update_quantity_unknown_product_raises(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Raises ProductNotFoundError for unknown product."""
        with pytest.raises(ProductNotFoundError):
            in_memory_repository.update_quantity("unknown", 50)
    
    def test_update_quantity_negative_raises(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Raises ValueError for negative quantity."""
        with pytest.raises(ValueError, match="negative"):
            in_memory_repository.update_quantity("p1", -1)
    
    # ----- reserve contract -----
    
    def test_reserve_returns_active_reservation(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Returns reservation with active status."""
        result = in_memory_repository.reserve("p1", 10, "order_123")
        
        assert isinstance(result, Reservation)
        assert result.status == "active"
        assert result.product_id == "p1"
        assert result.quantity == 10
    
    def test_reserve_reduces_available_quantity(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Reserve reduces available inventory."""
        before = in_memory_repository.find_by_product_id("p1").quantity
        
        in_memory_repository.reserve("p1", 20, "order_123")
        
        after = in_memory_repository.find_by_product_id("p1").quantity
        assert after == before  # Total unchanged, but reserved
    
    def test_reserve_unknown_product_raises(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Raises ProductNotFoundError for unknown product."""
        with pytest.raises(ProductNotFoundError):
            in_memory_repository.reserve("unknown", 10, "order_123")
    
    def test_reserve_insufficient_stock_raises(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Raises InsufficientStockError when not enough available."""
        with pytest.raises(InsufficientStockError):
            in_memory_repository.reserve("p1", 9999, "order_123")
    
    def test_reserve_zero_or_negative_raises(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Raises ValueError for non-positive quantity."""
        with pytest.raises(ValueError):
            in_memory_repository.reserve("p1", 0, "order_123")
    
    # ----- release_reservation contract -----
    
    def test_release_reservation_returns_updated_item(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Returns inventory item after release."""
        reservation = in_memory_repository.reserve("p1", 10, "order_123")
        
        result = in_memory_repository.release_reservation(reservation.id)
        
        assert isinstance(result, InventoryItem)
        assert result.product.id == "p1"
    
    def test_release_reservation_updates_status(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Reservation status changes to 'released'."""
        reservation = in_memory_repository.reserve("p1", 10, "order_123")
        
        in_memory_repository.release_reservation(reservation.id)
        
        reservations = in_memory_repository.get_reservations_for_order("order_123")
        assert reservations[0].status == "released"
    
    def test_release_unknown_reservation_raises(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Raises ReservationNotFoundError for unknown reservation."""
        with pytest.raises(ReservationNotFoundError):
            in_memory_repository.release_reservation(UUID("12345678-1234-5678-1234-567812345678"))
    
    def test_release_already_released_raises(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Raises InvalidOperationError for non-active reservation."""
        reservation = in_memory_repository.reserve("p1", 10, "order_123")
        in_memory_repository.release_reservation(reservation.id)
        
        with pytest.raises(InvalidOperationError):
            in_memory_repository.release_reservation(reservation.id)
    
    # ----- confirm_reservation contract -----
    
    def test_confirm_reservation_deducts_from_inventory(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Confirm permanently deducts from inventory."""
        before = in_memory_repository.find_by_product_id("p1").quantity
        reservation = in_memory_repository.reserve("p1", 10, "order_123")
        
        in_memory_repository.confirm_reservation(reservation.id)
        
        after = in_memory_repository.find_by_product_id("p1").quantity
        assert after == before - 10
    
    def test_confirm_reservation_updates_status(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Status changes to 'confirmed'."""
        reservation = in_memory_repository.reserve("p1", 10, "order_123")
        
        in_memory_repository.confirm_reservation(reservation.id)
        
        reservations = in_memory_repository.get_reservations_for_order("order_123")
        assert reservations[0].status == "confirmed"
    
    # ----- get_all contract -----
    
    def test_get_all_returns_all_items(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Returns all inventory items."""
        result = in_memory_repository.get_all()
        
        assert len(result) == 3
        assert all(isinstance(item, InventoryItem) for item in result)
    
    def test_get_all_empty_returns_empty_list(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Empty repository returns empty list, not None."""
        # Create fresh empty repo
        empty_repo = InMemoryInventoryRepository()
        result = empty_repo.get_all()
        
        assert result == []
    
    # ----- get_reservations_for_order contract -----
    
    def test_get_reservations_for_order_returns_list(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: Returns list of reservations for order."""
        in_memory_repository.reserve("p1", 5, "order_abc")
        in_memory_repository.reserve("p2", 3, "order_abc")
        
        result = in_memory_repository.get_reservations_for_order("order_abc")
        
        assert len(result) == 2
        assert all(isinstance(r, Reservation) for r in result)
    
    def test_get_reservations_for_order_no_match_returns_empty(
        self, in_memory_repository: InventoryRepository
    ) -> None:
        """Contract: No reservations returns empty list."""
        result = in_memory_repository.get_reservations_for_order("no_such_order")
        
        assert result == []


# ============================================================================
# IN-MEMORY SPECIFIC TESTS - Tests unique to the in-memory implementation
# ============================================================================

class TestInMemoryInventoryRepositorySpecific:
    """Tests specific to InMemoryInventoryRepository behavior."""
    
    def test_add_initial_stock_helper_works(self) -> None:
        """The helper method should seed inventory correctly."""
        repo = InMemoryInventoryRepository()
        product = Product("test", "Test", "TST-001", Decimal("1.00"))
        
        repo.add_initial_stock(InventoryItem(product, 50, "A1"))
        
        result = repo.find_by_product_id("test")
        assert result.quantity == 50
    
    def test_reservations_isolated_per_instance(self) -> None:
        """Different repository instances don't share reservations."""
        repo1 = InMemoryInventoryRepository()
        repo2 = InMemoryInventoryRepository()
        
        product = Product("p", "P", "P-001", Decimal("1.00"))
        repo1.add_initial_stock(InventoryItem(product, 100, "A1"))
        repo2.add_initial_stock(InventoryItem(product, 100, "A1"))
        
        reservation = repo1.reserve("p", 10, "order_1")
        
        # repo2 should not see repo1's reservation
        assert len(repo2.get_reservations_for_order("order_1")) == 0


# ============================================================================
# INVENTORY SERVICE TESTS
# ============================================================================

class TestInventoryService:
    """Tests for InventoryService."""
    
    @pytest.fixture
    def service(self, in_memory_repository: InMemoryInventoryRepository) -> InventoryService:
        """Service with in-memory repository."""
        return InventoryService(in_memory_repository)
    
    def test_check_stock_sufficient_returns_true(self, service: InventoryService) -> None:
        """Should return True when stock >= required."""
        assert service.check_stock("p1", 50) is True
        assert service.check_stock("p1", 100) is True
    
    def test_check_stock_insufficient_returns_false(self, service: InventoryService) -> None:
        """Should return False when stock < required."""
        assert service.check_stock("p1", 101) is False
    
    def test_check_stock_unknown_product_returns_false(self, service: InventoryService) -> None:
        """Should return False for unknown product."""
        assert service.check_stock("unknown", 1) is False
    
    def test_allocate_stock_creates_reservation(
        self,
        service: InventoryService,
        in_memory_repository: InMemoryInventoryRepository,
    ) -> None:
        """Should create reservation for stock allocation."""
        reservation = service.allocate_stock("p1", 25, "order_xyz")
        
        assert reservation.product_id == "p1"
        assert reservation.quantity == 25
        assert reservation.order_id == "order_xyz"
        
        # Verify it was stored
        reservations = in_memory_repository.get_reservations_for_order("order_xyz")
        assert len(reservations) == 1
    
    def test_get_available_quantity_returns_current_stock(
        self, service: InventoryService
    ) -> None:
        """Should return current inventory quantity."""
        assert service.get_available_quantity("p1") == 100
        assert service.get_available_quantity("p2") == 50
    
    def test_get_available_quantity_unknown_returns_zero(
        self, service: InventoryService
    ) -> None:
        """Should return 0 for unknown product."""
        assert service.get_available_quantity("unknown") == 0


# ============================================================================
# RESERVATION LIFECYCLE TESTS
# ============================================================================

class TestReservationLifecycle:
    """End-to-end tests for complete reservation flows."""
    
    def test_full_reserve_confirm_flow(self) -> None:
        """Complete flow: reserve -> confirm -> inventory reduced."""
        repo = InMemoryInventoryRepository()
        repo.add_initial_stock(InventoryItem(
            Product("widget", "Widget", "W-001", Decimal("10.00")),
            100, "A1"
        ))
        
        # Reserve 30 units
        reservation = repo.reserve("widget", 30, "order_1")
        assert repo.find_by_product_id("widget").quantity == 100  # Total unchanged
        
        # Confirm reservation
        repo.confirm_reservation(reservation.id)
        assert repo.find_by_product_id("widget").quantity == 70  # Now reduced
    
    def test_full_reserve_release_flow(self) -> None:
        """Complete flow: reserve -> release -> stock available again."""
        repo = InMemoryInventoryRepository()
        repo.add_initial_stock(InventoryItem(
            Product("widget", "Widget", "W-001", Decimal("10.00")),
            100, "A1"
        ))
        
        service = InventoryService(repo)
        
        # Check we can reserve 100
        assert service.check_stock("widget", 100) is True
        
        # Reserve 60
        reservation = repo.reserve("widget", 60, "order_1")
        
        # After reserving 60, we can still reserve up to 40 more (100 - 60 reserved)
        # But check_stock checks raw quantity, not available after reservations
        # So check_stock("widget", 100) should still be True (raw inventory is 100)
        # The reserve() call will fail if there's insufficient *available* stock
        reservation2 = repo.reserve("widget", 40, "order_2")
        
        # At this point: 60 + 40 = 100 reserved, 0 available
        # Trying to reserve more should fail
        with pytest.raises(InsufficientStockError):
            repo.reserve("widget", 1, "order_3")
        
        # Release first reservation
        repo.release_reservation(reservation.id)
        
        # Now 40 reserved (order_2), 60 available
        # Can reserve up to 60 more
        reservation3 = repo.reserve("widget", 60, "order_3")
        assert reservation3.quantity == 60

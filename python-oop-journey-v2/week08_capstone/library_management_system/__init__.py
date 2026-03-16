"""Library Management System - Week 8 Capstone.

A comprehensive library management system demonstrating:
- Repository Pattern for data access
- Strategy Pattern for search and fine calculation
- Observer Pattern for event notifications
- Factory Pattern for entity creation
"""

__version__ = "1.0.0"

from .domain.enums import (
    CopyStatus,
    LoanStatus,
    MembershipStatus,
    ReservationStatus,
    FineStatus,
    StaffRole,
    Condition,
)
from .domain.book import Book, BookCopy
from .domain.member import Member, Librarian
from .domain.loan import Loan, Reservation
from .domain.fine import Fine
from .repositories.book_repository import BookRepository, InMemoryBookRepository
from .repositories.member_repository import MemberRepository, InMemoryMemberRepository
from .repositories.loan_repository import LoanRepository, InMemoryLoanRepository
from .services.catalog_service import CatalogService, SearchStrategy
from .services.circulation_service import CirculationService, EventBus, CirculationEvent
from .services.reservation_service import ReservationService
from .services.fine_service import FineService, FineCalculationStrategy

__all__ = [
    # Enums
    "CopyStatus",
    "LoanStatus",
    "MembershipStatus",
    "ReservationStatus",
    "FineStatus",
    "StaffRole",
    "Condition",
    # Domain
    "Book",
    "BookCopy",
    "Member",
    "Librarian",
    "Loan",
    "Reservation",
    "Fine",
    # Repositories
    "BookRepository",
    "InMemoryBookRepository",
    "MemberRepository",
    "InMemoryMemberRepository",
    "LoanRepository",
    "InMemoryLoanRepository",
    # Services
    "CatalogService",
    "SearchStrategy",
    "CirculationService",
    "EventBus",
    "CirculationEvent",
    "ReservationService",
    "FineService",
    "FineCalculationStrategy",
]

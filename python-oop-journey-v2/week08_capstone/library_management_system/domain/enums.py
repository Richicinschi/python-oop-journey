"""Domain enumerations for the Library Management System."""

from __future__ import annotations

from enum import Enum, auto


class CopyStatus(Enum):
    """Status of a physical book copy."""

    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"
    LOST = "lost"


class LoanStatus(Enum):
    """Status of a book loan."""

    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"
    LOST = "lost"


class MembershipStatus(Enum):
    """Status of a library membership."""

    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"


class ReservationStatus(Enum):
    """Status of a book reservation."""

    PENDING = "pending"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class FineStatus(Enum):
    """Payment status of a fine."""

    OUTSTANDING = "outstanding"
    PAID = "paid"
    WAIVED = "waived"


class StaffRole(Enum):
    """Role levels for library staff."""

    ASSISTANT = "assistant"
    LIBRARIAN = "librarian"
    MANAGER = "manager"


class Condition(Enum):
    """Physical condition rating for book copies."""

    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    DAMAGED = "damaged"

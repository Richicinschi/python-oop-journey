"""Reservation service for managing book reservations."""

from __future__ import annotations

from typing import Optional

from ..domain.loan import Reservation
from ..domain.enums import ReservationStatus
from ..repositories.book_repository import BookRepository
from ..repositories.loan_repository import LoanRepository
from ..repositories.member_repository import MemberRepository


class ReservationService:
    """Service for managing book reservations.

    Handles the reservation queue and fulfillment process.
    """

    def __init__(
        self,
        book_repository: BookRepository,
        member_repository: MemberRepository,
        loan_repository: LoanRepository,
    ) -> None:
        self._book_repo = book_repository
        self._member_repo = member_repository
        self._loan_repo = loan_repository
        self._reservations: dict[str, Reservation] = {}  # In-memory storage

    def create_reservation(
        self,
        book_isbn: str,
        member_id: str,
        reservation_id: Optional[str] = None,
    ) -> tuple[bool, str, Optional[Reservation]]:
        """Create a new reservation for a book.

        Returns:
            Tuple of (success, message, reservation)
        """
        # Validate book
        book = self._book_repo.find_book_by_isbn(book_isbn)
        if not book:
            return False, "Book not found", None

        # Validate member
        member = self._member_repo.find_by_id(member_id)
        if not member:
            return False, "Member not found", None

        if not member.can_reserve():
            return False, "Member cannot make reservations", None

        # Check if member already has a pending reservation for this book
        existing = self._find_member_reservation_for_book(member_id, book_isbn)
        if existing and existing.status in (
            ReservationStatus.PENDING,
        ):
            return False, "Member already has a reservation for this book", existing

        # Calculate queue position
        queue_position = self._get_queue_position(book_isbn)

        # Create reservation
        res_id = reservation_id or f"RES-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        reservation = Reservation.create(
            reservation_id=res_id,
            book_isbn=book_isbn,
            member_id=member_id,
            queue_position=queue_position,
        )

        self._reservations[reservation.reservation_id] = reservation

        return True, "Reservation created successfully", reservation

    def cancel_reservation(self, reservation_id: str) -> tuple[bool, str]:
        """Cancel a reservation.

        Returns:
            Tuple of (success, message)
        """
        reservation = self._reservations.get(reservation_id)
        if not reservation:
            return False, "Reservation not found"

        try:
            reservation.cancel()
            # Reorder queue
            self._reorder_queue(reservation.book_isbn)
            return True, "Reservation cancelled successfully"
        except Exception as e:
            return False, str(e)

    def fulfill_reservation(
        self,
        reservation_id: str,
    ) -> tuple[bool, str, Optional[Reservation]]:
        """Mark a reservation as fulfilled.

        Returns:
            Tuple of (success, message, reservation)
        """
        reservation = self._reservations.get(reservation_id)
        if not reservation:
            return False, "Reservation not found", None

        try:
            reservation.fulfill()
            # Reorder queue
            self._reorder_queue(reservation.book_isbn)
            return True, "Reservation fulfilled", reservation
        except Exception as e:
            return False, str(e), None

    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        """Get a reservation by ID."""
        return self._reservations.get(reservation_id)

    def get_member_reservations(self, member_id: str) -> list[Reservation]:
        """Get all reservations for a member."""
        return [
            r for r in self._reservations.values() if r.member_id == member_id
        ]

    def get_member_active_reservations(self, member_id: str) -> list[Reservation]:
        """Get active (pending) reservations for a member."""
        return [
            r
            for r in self._reservations.values()
            if r.member_id == member_id
            and r.status == ReservationStatus.PENDING
        ]

    def get_book_reservations(self, book_isbn: str) -> list[Reservation]:
        """Get all reservations for a book."""
        return [
            r for r in self._reservations.values() if r.book_isbn == book_isbn
        ]

    def get_pending_reservations(self, book_isbn: str) -> list[Reservation]:
        """Get pending reservations for a book."""
        return [
            r
            for r in self._reservations.values()
            if r.book_isbn == book_isbn
            and r.status == ReservationStatus.PENDING
        ]

    def cleanup_expired_reservations(self) -> list[Reservation]:
        """Mark expired reservations and return them.

        Returns:
            List of newly expired reservations
        """
        from datetime import date
        expired = []
        for reservation in self._reservations.values():
            if (
                reservation.status == ReservationStatus.PENDING
                and reservation.is_expired()
            ):
                reservation.expire()
                expired.append(reservation)
                # Reorder queue for this book
                self._reorder_queue(reservation.book_isbn)
        return expired

    def _find_member_reservation_for_book(
        self, member_id: str, book_isbn: str
    ) -> Optional[Reservation]:
        """Find if a member has a reservation for a specific book."""
        for reservation in self._reservations.values():
            if reservation.member_id == member_id and reservation.book_isbn == book_isbn:
                return reservation
        return None

    def _get_queue_position(self, book_isbn: str) -> int:
        """Get the next queue position for a book."""
        pending = self.get_pending_reservations(book_isbn)
        return len(pending) + 1

    def _reorder_queue(self, book_isbn: str) -> None:
        """Reorder the reservation queue after a cancellation or fulfillment."""
        pending = [
            r
            for r in self._reservations.values()
            if r.book_isbn == book_isbn
            and r.status == ReservationStatus.PENDING
        ]
        # Sort by reservation date (FIFO queue)
        pending.sort(key=lambda r: r.reservation_date)
        # Update queue positions
        for i, reservation in enumerate(pending, 1):
            reservation.update_queue_position(i)

    def get_reservation_statistics(self) -> dict:
        """Get statistics about reservations."""
        total = len(self._reservations)
        pending = sum(
            1 for r in self._reservations.values() if r.status == ReservationStatus.PENDING
        )
        fulfilled = sum(
            1
            for r in self._reservations.values()
            if r.status == ReservationStatus.FULFILLED
        )
        cancelled = sum(
            1
            for r in self._reservations.values()
            if r.status == ReservationStatus.CANCELLED
        )
        expired = sum(
            1 for r in self._reservations.values() if r.status == ReservationStatus.EXPIRED
        )

        return {
            "total": total,
            "pending": pending,
            "fulfilled": fulfilled,
            "cancelled": cancelled,
            "expired": expired,
        }


# Import needed for the create_reservation method
from datetime import datetime

"""Loan repository implementation using the Repository pattern."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from ..domain.loan import Loan
from ..domain.enums import LoanStatus


class LoanRepository(ABC):
    """Abstract repository for Loan entities.

    Following the Repository pattern, this abstracts the data access
    layer from the domain logic.
    """

    @abstractmethod
    def save(self, loan: Loan) -> Loan:
        """Save a loan to the repository."""
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, loan_id: str) -> Optional[Loan]:
        """Find a loan by its unique ID."""
        raise NotImplementedError

    @abstractmethod
    def find_by_member(self, member_id: str) -> list[Loan]:
        """Find all loans for a specific member."""
        raise NotImplementedError

    @abstractmethod
    def find_by_copy_barcode(self, barcode: str) -> list[Loan]:
        """Find all loans for a specific book copy."""
        raise NotImplementedError

    @abstractmethod
    def find_active_by_member(self, member_id: str) -> list[Loan]:
        """Find active (non-returned) loans for a member."""
        raise NotImplementedError

    @abstractmethod
    def find_active_by_copy(self, barcode: str) -> Optional[Loan]:
        """Find the active loan for a specific book copy."""
        raise NotImplementedError

    @abstractmethod
    def find_overdue_loans(self) -> list[Loan]:
        """Find all overdue loans."""
        raise NotImplementedError

    @abstractmethod
    def find_by_status(self, status: LoanStatus) -> list[Loan]:
        """Find all loans with a specific status."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Loan]:
        """Get all loans in the repository."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, loan_id: str) -> bool:
        """Delete a loan from the repository."""
        raise NotImplementedError


class InMemoryLoanRepository(LoanRepository):
    """In-memory implementation of LoanRepository.

    Stores loans in dictionaries. Suitable for testing
    and small-scale applications.
    """

    def __init__(self) -> None:
        self._loans: dict[str, Loan] = {}  # loan_id -> Loan

    def save(self, loan: Loan) -> Loan:
        """Save a loan to the repository."""
        self._loans[loan.loan_id] = loan
        return loan

    def find_by_id(self, loan_id: str) -> Optional[Loan]:
        """Find a loan by its unique ID."""
        return self._loans.get(loan_id)

    def find_by_member(self, member_id: str) -> list[Loan]:
        """Find all loans for a specific member."""
        return [loan for loan in self._loans.values() if loan.member_id == member_id]

    def find_by_copy_barcode(self, barcode: str) -> list[Loan]:
        """Find all loans for a specific book copy."""
        return [
            loan for loan in self._loans.values() if loan.copy_barcode == barcode
        ]

    def find_active_by_member(self, member_id: str) -> list[Loan]:
        """Find active (non-returned) loans for a member."""
        return [
            loan
            for loan in self._loans.values()
            if loan.member_id == member_id and loan.status in (LoanStatus.ACTIVE, LoanStatus.OVERDUE)
        ]

    def find_active_by_copy(self, barcode: str) -> Optional[Loan]:
        """Find the active loan for a specific book copy."""
        for loan in self._loans.values():
            if loan.copy_barcode == barcode and loan.status in (LoanStatus.ACTIVE, LoanStatus.OVERDUE):
                return loan
        return None

    def find_overdue_loans(self) -> list[Loan]:
        """Find all overdue loans."""
        return [
            loan
            for loan in self._loans.values()
            if loan.status == LoanStatus.OVERDUE or (loan.status == LoanStatus.ACTIVE and loan.is_overdue())
        ]

    def find_by_status(self, status: LoanStatus) -> list[Loan]:
        """Find all loans with a specific status."""
        return [loan for loan in self._loans.values() if loan.status == status]

    def get_all(self) -> list[Loan]:
        """Get all loans in the repository."""
        return list(self._loans.values())

    def delete(self, loan_id: str) -> bool:
        """Delete a loan from the repository."""
        return self._loans.pop(loan_id, None) is not None

    def clear(self) -> None:
        """Clear all data (useful for testing)."""
        self._loans.clear()

"""Repository layer for data persistence.

Implements the Repository pattern to abstract data access.
"""

from .book_repository import BookRepository, InMemoryBookRepository
from .member_repository import MemberRepository, InMemoryMemberRepository
from .loan_repository import LoanRepository, InMemoryLoanRepository

__all__ = [
    "BookRepository",
    "InMemoryBookRepository",
    "MemberRepository",
    "InMemoryMemberRepository",
    "LoanRepository",
    "InMemoryLoanRepository",
]

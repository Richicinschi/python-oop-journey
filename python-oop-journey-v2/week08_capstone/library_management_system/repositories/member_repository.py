"""Member repository implementation using the Repository pattern."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from ..domain.member import Member
from ..domain.enums import MembershipStatus


class MemberRepository(ABC):
    """Abstract repository for Member entities.

    Following the Repository pattern, this abstracts the data access
    layer from the domain logic.
    """

    @abstractmethod
    def save(self, member: Member) -> Member:
        """Save a member to the repository."""
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, member_id: str) -> Optional[Member]:
        """Find a member by their unique ID."""
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Member]:
        """Find a member by their email address."""
        raise NotImplementedError

    @abstractmethod
    def find_by_name(self, name: str) -> list[Member]:
        """Find members by name (partial match)."""
        raise NotImplementedError

    @abstractmethod
    def find_by_status(self, status: MembershipStatus) -> list[Member]:
        """Find all members with a specific status."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Member]:
        """Get all members in the repository."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, member_id: str) -> bool:
        """Delete a member from the repository."""
        raise NotImplementedError


class InMemoryMemberRepository(MemberRepository):
    """In-memory implementation of MemberRepository.

    Stores members in dictionaries. Suitable for testing
    and small-scale applications.
    """

    def __init__(self) -> None:
        self._members: dict[str, Member] = {}  # member_id -> Member
        self._email_index: dict[str, str] = {}  # email -> member_id

    def save(self, member: Member) -> Member:
        """Save a member to the repository."""
        self._members[member.member_id] = member
        self._email_index[member.email] = member.member_id
        return member

    def find_by_id(self, member_id: str) -> Optional[Member]:
        """Find a member by their unique ID."""
        return self._members.get(member_id)

    def find_by_email(self, email: str) -> Optional[Member]:
        """Find a member by their email address."""
        member_id = self._email_index.get(email)
        if member_id:
            return self._members.get(member_id)
        return None

    def find_by_name(self, name: str) -> list[Member]:
        """Find members by name (case-insensitive partial match)."""
        name_lower = name.lower()
        return [
            member
            for member in self._members.values()
            if name_lower in member.name.lower()
        ]

    def find_by_status(self, status: MembershipStatus) -> list[Member]:
        """Find all members with a specific status."""
        return [member for member in self._members.values() if member.status == status]

    def get_all(self) -> list[Member]:
        """Get all members in the repository."""
        return list(self._members.values())

    def delete(self, member_id: str) -> bool:
        """Delete a member from the repository."""
        member = self._members.pop(member_id, None)
        if member:
            self._email_index.pop(member.email, None)
            return True
        return False

    def clear(self) -> None:
        """Clear all data (useful for testing)."""
        self._members.clear()
        self._email_index.clear()

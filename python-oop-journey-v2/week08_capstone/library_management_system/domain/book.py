"""Book domain entities - Book and BookCopy."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import ClassVar, Self

from .enums import CopyStatus, Condition


class DomainError(Exception):
    """Base exception for domain errors."""
    pass


class ValidationError(DomainError):
    """Raised when validation fails."""
    pass


@dataclass
class BookCopy:
    """A physical copy of a book in the library.

    Each copy has a unique barcode and tracks its own status independently
    of other copies of the same book.

    Attributes:
        barcode: Unique identifier for this physical copy
        book_isbn: ISBN of the book this copy represents
        branch_id: Identifier for the library branch holding this copy
        acquisition_date: Date the library acquired this copy
        status: Current availability status
        condition: Physical condition of the copy

    Example:
        >>> copy = BookCopy(
        ...     barcode="CP001",
        ...     book_isbn="978-0-123456-78-9",
        ...     branch_id="BRANCH01"
        ... )
        >>> copy.status
        <CopyStatus.AVAILABLE: 'available'>
    """

    barcode: str
    book_isbn: str
    branch_id: str = "MAIN"
    acquisition_date: date = field(default_factory=date.today)
    status: CopyStatus = CopyStatus.AVAILABLE
    condition: Condition = Condition.GOOD

    def __post_init__(self) -> None:
        """Validate copy data after initialization."""
        if not self.barcode or not isinstance(self.barcode, str):
            raise ValidationError("Barcode must be a non-empty string")
        if not self.book_isbn or not isinstance(self.book_isbn, str):
            raise ValidationError("Book ISBN must be a non-empty string")
        if not isinstance(self.status, CopyStatus):
            raise ValidationError(f"Invalid status: {self.status}")
        if not isinstance(self.condition, Condition):
            raise ValidationError(f"Invalid condition: {self.condition}")

    def is_available(self) -> bool:
        """Check if this copy can be borrowed.

        Returns:
            True if the copy is available for checkout.
        """
        return self.status == CopyStatus.AVAILABLE

    def can_transition_to(self, new_status: CopyStatus) -> bool:
        """Check if status transition is valid.

        Args:
            new_status: The desired new status.

        Returns:
            True if the transition is allowed.
        """
        valid_transitions = {
            CopyStatus.AVAILABLE: [
                CopyStatus.BORROWED,
                CopyStatus.RESERVED,
                CopyStatus.MAINTENANCE,
            ],
            CopyStatus.BORROWED: [
                CopyStatus.AVAILABLE,
                CopyStatus.RESERVED,
                CopyStatus.LOST,
            ],
            CopyStatus.RESERVED: [CopyStatus.AVAILABLE, CopyStatus.BORROWED],
            CopyStatus.MAINTENANCE: [CopyStatus.AVAILABLE],
            CopyStatus.LOST: [CopyStatus.AVAILABLE],
        }
        return new_status in valid_transitions.get(self.status, [])

    def update_status(self, new_status: CopyStatus) -> Self:
        """Update the status of this copy.

        Args:
            new_status: The new status to set.

        Returns:
            Self for method chaining.

        Raises:
            ValidationError: If the status transition is invalid.
        """
        if not self.can_transition_to(new_status):
            raise ValidationError(
                f"Cannot transition from {self.status.value} to {new_status.value}"
            )
        self.status = new_status
        return self

    def mark_as_borrowed(self) -> Self:
        """Mark this copy as borrowed.

        Returns:
            Self for method chaining.
        """
        return self.update_status(CopyStatus.BORROWED)

    def mark_as_returned(self) -> Self:
        """Mark this copy as available (returned).

        Returns:
            Self for method chaining.
        """
        return self.update_status(CopyStatus.AVAILABLE)

    def mark_as_reserved(self) -> Self:
        """Mark this copy as reserved.

        Returns:
            Self for method chaining.
        """
        return self.update_status(CopyStatus.RESERVED)

    def mark_as_lost(self) -> Self:
        """Mark this copy as lost.

        Returns:
            Self for method chaining.
        """
        return self.update_status(CopyStatus.LOST)


@dataclass
class Book:
    """A book in the library catalog.

    Represents the catalog information (title, author, etc.) rather than
    a specific physical copy. A book can have multiple copies.

    Attributes:
        isbn: International Standard Book Number (unique identifier)
        title: Book title
        authors: Tuple of author names
        publisher: Publishing house
        publication_year: Year of publication
        genre: Book category/genre
        page_count: Number of pages (optional)
        copies: List of physical copies of this book

    Example:
        >>> book = Book(
        ...     isbn="978-0-123456-78-9",
        ...     title="Clean Code",
        ...     authors=("Robert C. Martin",),
        ...     publisher="Prentice Hall",
        ...     publication_year=2008,
        ...     genre="Technology"
        ... )
        >>> book.add_copy(BookCopy(barcode="CP001", book_isbn=book.isbn))
    """

    isbn: str
    title: str
    authors: tuple[str, ...]
    publisher: str
    publication_year: int
    genre: str
    page_count: int | None = None
    copies: list[BookCopy] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate book data after initialization."""
        if not self.isbn or not isinstance(self.isbn, str):
            raise ValidationError("ISBN must be a non-empty string")
        if not self._is_valid_isbn(self.isbn):
            raise ValidationError(f"Invalid ISBN format: {self.isbn}")
        if not self.title or not isinstance(self.title, str):
            raise ValidationError("Title must be a non-empty string")
        if not self.authors or not isinstance(self.authors, tuple):
            raise ValidationError("Authors must be a non-empty tuple")
        if not all(isinstance(a, str) and a.strip() for a in self.authors):
            raise ValidationError("All authors must be non-empty strings")
        if not self.publisher or not isinstance(self.publisher, str):
            raise ValidationError("Publisher must be a non-empty string")
        if not isinstance(self.publication_year, int):
            raise ValidationError("Publication year must be an integer")
        from datetime import datetime
        if self.publication_year > datetime.now().year:
            raise ValidationError("Publication year cannot be in the future")
        if not isinstance(self.genre, str):
            raise ValidationError("Genre must be a string")

    @staticmethod
    def _is_valid_isbn(isbn: str) -> bool:
        """Validate ISBN-10 or ISBN-13 format.

        Args:
            isbn: The ISBN string to validate.

        Returns:
            True if valid ISBN format.
        """
        # Remove hyphens and spaces
        cleaned = isbn.replace("-", "").replace(" ", "")
        # Check for ISBN-10 (10 digits, last can be X)
        if len(cleaned) == 10:
            return cleaned[:9].isdigit() and (cleaned[9].isdigit() or cleaned[9].upper() == "X")
        # Check for ISBN-13 (13 digits)
        if len(cleaned) == 13:
            return cleaned.isdigit()
        return False

    def add_copy(self, copy: BookCopy) -> Self:
        """Add a physical copy to this book.

        Args:
            copy: The BookCopy to add.

        Returns:
            Self for method chaining.

        Raises:
            ValidationError: If copy's ISBN doesn't match this book.
        """
        if copy.book_isbn != self.isbn:
            raise ValidationError(
                f"Copy ISBN {copy.book_isbn} does not match book ISBN {self.isbn}"
            )
        # Check for duplicate barcode
        if any(c.barcode == copy.barcode for c in self.copies):
            raise ValidationError(f"Copy with barcode {copy.barcode} already exists")
        self.copies.append(copy)
        return self

    def remove_copy(self, barcode: str) -> BookCopy:
        """Remove a physical copy by barcode.

        Args:
            barcode: The barcode of the copy to remove.

        Returns:
            The removed BookCopy.

        Raises:
            ValidationError: If copy not found or is currently borrowed.
        """
        for i, copy in enumerate(self.copies):
            if copy.barcode == barcode:
                if copy.status == CopyStatus.BORROWED:
                    raise ValidationError(
                        f"Cannot remove borrowed copy {barcode}"
                    )
                return self.copies.pop(i)
        raise ValidationError(f"Copy with barcode {barcode} not found")

    def get_copy(self, barcode: str) -> BookCopy | None:
        """Get a copy by its barcode.

        Args:
            barcode: The barcode to search for.

        Returns:
            The BookCopy if found, None otherwise.
        """
        for copy in self.copies:
            if copy.barcode == barcode:
                return copy
        return None

    def get_available_copies(self) -> list[BookCopy]:
        """Get all available copies of this book.

        Returns:
            List of copies with AVAILABLE status.
        """
        return [c for c in self.copies if c.status == CopyStatus.AVAILABLE]

    def has_available_copies(self) -> bool:
        """Check if any copy is available.

        Returns:
            True if at least one copy is available.
        """
        return any(c.status == CopyStatus.AVAILABLE for c in self.copies)

    def get_copies_by_branch(self, branch_id: str) -> list[BookCopy]:
        """Get all copies at a specific branch.

        Args:
            branch_id: The branch identifier.

        Returns:
            List of copies at the specified branch.
        """
        return [c for c in self.copies if c.branch_id == branch_id]

    @property
    def author_string(self) -> str:
        """Get formatted author string.

        Returns:
            Comma-separated list of authors.
        """
        return ", ".join(self.authors)

    @property
    def copy_count(self) -> int:
        """Get total number of copies.

        Returns:
            The number of physical copies.
        """
        return len(self.copies)

    @property
    def available_copy_count(self) -> int:
        """Get number of available copies.

        Returns:
            The number of copies with AVAILABLE status.
        """
        return len(self.get_available_copies())

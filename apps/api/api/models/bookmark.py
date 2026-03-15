"""Bookmark model for user-saved problems."""

from datetime import datetime
from enum import Enum as PyEnum
from uuid import uuid4

from sqlalchemy import String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base


class ItemType(str, PyEnum):
    """Types of items that can be bookmarked."""

    PROBLEM = "problem"
    DAY = "day"
    WEEK = "week"
    THEORY = "theory"


class Bookmark(Base):
    """Bookmark model for user-saved problems.
    
    Note: The database schema uses String(36) for id to match other tables,
    and 'notes' as the column name (not 'note').
    """

    __tablename__ = "bookmarks"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    item_type: Mapped[ItemType] = mapped_column(
        Enum(ItemType),
        nullable=False,
        index=True,
    )
    item_slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="bookmarks")

    def __repr__(self) -> str:
        return f"<Bookmark(id={self.id}, user_id={self.user_id}, item_type={self.item_type}, item_slug={self.item_slug})>"

    def to_dict(self) -> dict:
        """Convert bookmark to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_type": self.item_type.value if self.item_type else None,
            "item_slug": self.item_slug,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

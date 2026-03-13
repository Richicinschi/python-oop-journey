"""Bookmark model for user-saved problems."""

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship

from api.database import Base


class ItemType(str, PyEnum):
    """Types of items that can be bookmarked."""

    PROBLEM = "problem"
    DAY = "day"
    WEEK = "week"
    THEORY = "theory"


class Bookmark(Base):
    """Bookmark model for user-saved problems."""

    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    item_type = Column(Enum(ItemType), nullable=False, index=True)
    item_slug = Column(String, nullable=False, index=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="bookmarks")

    def __repr__(self) -> str:
        return f"<Bookmark(id={self.id}, user_id={self.user_id}, item_type={self.item_type}, item_slug={self.item_slug})>"

    def to_dict(self) -> dict:
        """Convert bookmark to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_type": self.item_type.value if self.item_type else None,
            "item_slug": self.item_slug,
            "note": self.note,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

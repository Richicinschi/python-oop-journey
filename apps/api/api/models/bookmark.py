"""Bookmark model for user-saved problems."""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from api.database import Base


class Bookmark(Base):
    """Bookmark model for user-saved problems."""

    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_slug = Column(String, nullable=False, index=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="bookmarks")

    def __repr__(self) -> str:
        return f"<Bookmark(id={self.id}, user_id={self.user_id}, problem_slug={self.problem_slug})>"

    def to_dict(self) -> dict:
        """Convert bookmark to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "problem_slug": self.problem_slug,
            "note": self.note,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

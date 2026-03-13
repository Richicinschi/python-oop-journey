"""Draft model for saved code."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base


class Draft(Base):
    """User code drafts for problems."""

    __tablename__ = "drafts"
    __table_args__ = (
        UniqueConstraint("user_id", "problem_slug", name="uq_user_problem_draft"),
    )

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
    problem_slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )
    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    is_auto_save: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="drafts")

    def __repr__(self) -> str:
        return f"<Draft user={self.user_id} problem={self.problem_slug}>"

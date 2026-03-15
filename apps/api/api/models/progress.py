"""Progress model."""

from datetime import datetime
from enum import Enum as PyEnum
from uuid import uuid4

from sqlalchemy import String, DateTime, ForeignKey, Integer, Enum, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base


class ProblemStatus(str, PyEnum):
    """Problem completion status."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SOLVED = "solved"
    NEEDS_REVIEW = "needs_review"


class Progress(Base):
    """User progress on problems."""

    __tablename__ = "progress"
    __table_args__ = (
        UniqueConstraint("user_id", "problem_slug", name="uq_user_problem_progress"),
        # Composite index for user progress queries filtered by status
        Index("idx_progress_user_status", "user_id", "status", postgresql_using="btree"),
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
    week_slug: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )
    day_slug: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )
    status: Mapped[ProblemStatus] = mapped_column(
        Enum(ProblemStatus),
        default=ProblemStatus.NOT_STARTED,
        nullable=False,
        index=True,
    )
    attempts_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    solved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    first_attempted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_attempted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    time_spent_seconds: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="progress")

    def __repr__(self) -> str:
        return f"<Progress user={self.user_id} problem={self.problem_slug} status={self.status}>"

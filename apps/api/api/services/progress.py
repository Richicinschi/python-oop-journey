"""Progress service for tracking user problem completion."""

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, func, and_, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.progress import Progress, ProblemStatus
from api.models.activity import Activity, ActivityType

logger = logging.getLogger(__name__)


class ProgressService:
    """Service for managing user progress on problems."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_progress(self, user_id: str, problem_slug: str) -> Progress | None:
        """Get progress for a specific problem."""
        stmt = select(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.problem_slug == problem_slug,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_create_progress(
        self, user_id: str, problem_slug: str
    ) -> Progress:
        """Get existing progress or create new entry."""
        progress = await self.get_progress(user_id, problem_slug)
        if progress:
            return progress

        # Create new progress entry
        progress = Progress(
            user_id=user_id,
            problem_slug=problem_slug,
            status=ProblemStatus.NOT_STARTED,
        )
        self.session.add(progress)
        await self.session.commit()
        await self.session.refresh(progress)
        return progress

    async def update_progress(
        self,
        user_id: str,
        problem_slug: str,
        status: ProblemStatus | None = None,
        week_slug: str | None = None,
        day_slug: str | None = None,
        time_spent_seconds: int | None = None,
    ) -> Progress:
        """Update progress for a problem."""
        progress = await self.get_or_create_progress(user_id, problem_slug)

        # Update denormalized fields if provided
        if week_slug:
            progress.week_slug = week_slug
        if day_slug:
            progress.day_slug = day_slug

        # Update status
        if status and status != progress.status:
            progress.status = status
            
            # Track first attempt
            if status == ProblemStatus.IN_PROGRESS and not progress.first_attempted_at:
                progress.first_attempted_at = datetime.now(timezone.utc)
            
            # Track completion
            if status == ProblemStatus.SOLVED and not progress.solved_at:
                progress.solved_at = datetime.now(timezone.utc)

        # Update time spent
        if time_spent_seconds:
            progress.time_spent_seconds += time_spent_seconds

        progress.last_attempted_at = datetime.now(timezone.utc)
        progress.updated_at = datetime.now(timezone.utc)

        await self.session.commit()
        await self.session.refresh(progress)
        return progress

    async def record_attempt(self, user_id: str, problem_slug: str) -> Progress:
        """Record an attempt on a problem."""
        progress = await self.get_or_create_progress(user_id, problem_slug)
        
        progress.attempts_count += 1
        progress.last_attempted_at = datetime.now(timezone.utc)
        
        # Set first attempted if not set
        if not progress.first_attempted_at:
            progress.first_attempted_at = datetime.now(timezone.utc)
        
        # Auto-update status to in_progress if not started
        if progress.status == ProblemStatus.NOT_STARTED:
            progress.status = ProblemStatus.IN_PROGRESS

        progress.updated_at = datetime.now(timezone.utc)
        
        await self.session.commit()
        await self.session.refresh(progress)
        return progress

    async def get_all_progress(self, user_id: str) -> list[Progress]:
        """Get all progress entries for a user."""
        stmt = select(Progress).where(Progress.user_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_week_progress(
        self, user_id: str, week_slug: str
    ) -> dict:
        """Get progress statistics for a specific week."""
        stmt = select(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.week_slug == week_slug,
            )
        )
        result = await self.session.execute(stmt)
        progress_list = list(result.scalars().all())

        total = len(progress_list)
        completed = sum(1 for p in progress_list if p.status == ProblemStatus.SOLVED)
        in_progress = sum(1 for p in progress_list if p.status == ProblemStatus.IN_PROGRESS)
        not_started = sum(1 for p in progress_list if p.status == ProblemStatus.NOT_STARTED)

        return {
            "week_slug": week_slug,
            "total_problems": total,
            "completed": completed,
            "in_progress": in_progress,
            "not_started": not_started,
            "completion_percentage": round((completed / total * 100), 2) if total > 0 else 0,
        }

    async def get_overall_progress(self, user_id: str, total_problems: int = 50) -> dict:
        """Get overall progress statistics for a user."""
        stmt = select(Progress).where(Progress.user_id == user_id)
        result = await self.session.execute(stmt)
        progress_list = list(result.scalars().all())

        completed = sum(1 for p in progress_list if p.status == ProblemStatus.SOLVED)
        in_progress = sum(1 for p in progress_list if p.status == ProblemStatus.IN_PROGRESS)
        not_started = total_problems - completed - in_progress

        total_time = sum(p.time_spent_seconds for p in progress_list)
        streak = await self.calculate_streak(user_id)
        longest_streak = await self.calculate_longest_streak(user_id)

        # Get last active date
        last_active = None
        if progress_list:
            last_attempt = max(
                (p.last_attempted_at for p in progress_list if p.last_attempted_at),
                default=None,
            )
            last_active = last_attempt

        return {
            "total_problems": total_problems,
            "completed": completed,
            "in_progress": in_progress,
            "not_started": max(0, not_started),
            "completion_percentage": round((completed / total_problems * 100), 2) if total_problems > 0 else 0,
            "current_streak": streak,
            "longest_streak": longest_streak,
            "total_time_spent_seconds": total_time,
            "last_active_at": last_active,
        }

    async def calculate_streak(self, user_id: str) -> int:
        """Calculate current streak of consecutive days with activity.
        
        PERFORMANCE NOTE: This fetches all distinct dates and calculates the streak
        in Python. For users with very high activity over many years, consider:
        - Using a SQL window function approach with LAG() to find gaps
        - Caching the streak result and updating incrementally
        - Materializing streak counts in a user_stats table
        """
        # Get activity dates for the last 365 days
        cutoff = datetime.now(timezone.utc) - timedelta(days=365)
        stmt = (
            select(distinct(func.date(Activity.created_at)))
            .where(
                and_(
                    Activity.user_id == user_id,
                    Activity.created_at >= cutoff,
                )
            )
            .order_by(func.date(Activity.created_at).desc())
        )
        result = await self.session.execute(stmt)
        dates = [row[0] for row in result.all()]

        if not dates:
            return 0

        # Calculate streak
        today = datetime.now(timezone.utc).date()
        yesterday = today - timedelta(days=1)

        streak = 0
        expected_date = today

        for date in dates:
            if date == expected_date or date == yesterday:
                streak += 1
                expected_date = date - timedelta(days=1)
            elif date < expected_date:
                break

        return streak

    async def calculate_longest_streak(self, user_id: str) -> int:
        """Calculate longest streak of consecutive days with activity."""
        # Get all activity dates
        stmt = (
            select(distinct(func.date(Activity.created_at)))
            .where(Activity.user_id == user_id)
            .order_by(func.date(Activity.created_at))
        )
        result = await self.session.execute(stmt)
        dates = [row[0] for row in result.all()]

        if not dates:
            return 0

        longest = 1
        current = 1

        for i in range(1, len(dates)):
            if dates[i] - dates[i - 1] == timedelta(days=1):
                current += 1
                longest = max(longest, current)
            else:
                current = 1

        return longest


def get_progress_service(session: AsyncSession) -> ProgressService:
    """Factory function for ProgressService."""
    return ProgressService(session)

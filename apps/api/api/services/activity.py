"""Activity service for logging and retrieving user activities."""

import logging
from datetime import datetime, timedelta

from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.activity import Activity, ActivityType

logger = logging.getLogger(__name__)


class ActivityService:
    """Service for managing user activity logs."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_activity(
        self,
        user_id: str,
        activity_type: ActivityType,
        item_slug: str | None = None,
        metadata: dict | None = None,
    ) -> Activity:
        """Log a new activity."""
        activity = Activity(
            user_id=user_id,
            activity_type=activity_type,
            item_slug=item_slug,
            metadata=metadata or {},
        )
        self.session.add(activity)
        await self.session.commit()
        await self.session.refresh(activity)
        logger.debug(
            f"Logged activity: {activity_type} for user={user_id} item={item_slug}"
        )
        return activity

    async def get_recent_activity(
        self,
        user_id: str,
        limit: int = 20,
        activity_type: ActivityType | None = None,
    ) -> list[Activity]:
        """Get recent activity for a user."""
        stmt = select(Activity).where(Activity.user_id == user_id)

        if activity_type:
            stmt = stmt.where(Activity.activity_type == activity_type)

        stmt = stmt.order_by(desc(Activity.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_activity_summary(self, user_id: str, days: int = 7) -> dict:
        """Get activity summary for a time period."""
        cutoff = datetime.utcnow() - timedelta(days=days)

        # Get all activities in the period
        stmt = select(Activity).where(
            and_(
                Activity.user_id == user_id,
                Activity.created_at >= cutoff,
            )
        )
        result = await self.session.execute(stmt)
        activities = list(result.scalars().all())

        # Count by type
        problems_started = sum(
            1 for a in activities if a.activity_type == ActivityType.STARTED_PROBLEM
        )
        problems_solved = sum(
            1 for a in activities if a.activity_type == ActivityType.SOLVED_PROBLEM
        )
        problems_attempted = sum(
            1 for a in activities if a.activity_type == ActivityType.ATTEMPTED_PROBLEM
        )
        theory_views = sum(
            1 for a in activities if a.activity_type == ActivityType.VIEWED_THEORY
        )

        # Count unique days active
        active_days = set()
        for activity in activities:
            active_days.add(activity.created_at.date())

        return {
            "period_days": days,
            "total_activities": len(activities),
            "problems_started": problems_started,
            "problems_solved": problems_solved,
            "problems_attempted": problems_attempted,
            "theory_views": theory_views,
            "unique_days_active": len(active_days),
        }

    async def get_activity_by_date(
        self, user_id: str, date: datetime
    ) -> list[Activity]:
        """Get activities for a specific date."""
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        stmt = select(Activity).where(
            and_(
                Activity.user_id == user_id,
                Activity.created_at >= start,
                Activity.created_at < end,
            )
        ).order_by(desc(Activity.created_at))

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_activity_stats(
        self, user_id: str, days: int = 30
    ) -> dict:
        """Get detailed activity statistics."""
        cutoff = datetime.utcnow() - timedelta(days=days)

        # Get counts by activity type
        stmt = (
            select(Activity.activity_type, func.count(Activity.id))
            .where(
                and_(
                    Activity.user_id == user_id,
                    Activity.created_at >= cutoff,
                )
            )
            .group_by(Activity.activity_type)
        )
        result = await self.session.execute(stmt)
        type_counts = {row[0]: row[1] for row in result.all()}

        # Get daily activity counts
        daily_stmt = (
            select(
                func.date(Activity.created_at),
                func.count(Activity.id),
            )
            .where(
                and_(
                    Activity.user_id == user_id,
                    Activity.created_at >= cutoff,
                )
            )
            .group_by(func.date(Activity.created_at))
            .order_by(func.date(Activity.created_at))
        )
        daily_result = await self.session.execute(daily_stmt)
        daily_activity = [
            {"date": str(row[0]), "count": row[1]}
            for row in daily_result.all()
        ]

        return {
            "period_days": days,
            "by_type": type_counts,
            "daily_activity": daily_activity,
            "total": sum(type_counts.values()),
        }

    async def cleanup_old_activities(
        self, days: int = 365
    ) -> int:
        """Delete activities older than specified days. Returns count deleted."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        stmt = select(Activity).where(Activity.created_at < cutoff)
        result = await self.session.execute(stmt)
        old_activities = list(result.scalars().all())
        
        count = len(old_activities)
        for activity in old_activities:
            await self.session.delete(activity)
        
        if count > 0:
            await self.session.commit()
            logger.info(f"Cleaned up {count} old activities")
        
        return count


def get_activity_service(session: AsyncSession) -> ActivityService:
    """Factory function for ActivityService."""
    return ActivityService(session)

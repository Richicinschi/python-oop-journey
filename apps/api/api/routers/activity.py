"""Activity logging endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.dependencies.auth import get_current_user_id
from api.schemas.progress import (
    Activity,
    ActivityCreate,
    ActivityList,
    ActivitySummary,
)
from api.services.activity import get_activity_service, ActivityService

router = APIRouter()

# TODO: Replace with actual auth dependency that validates JWT tokens
# For now, using a dependency that returns a mock user ID for development
# See: api/dependencies/auth.py for implementation


@router.get(
    "/activity",
    response_model=ActivityList,
    summary="Get recent activity",
    description="Get recent activity for the current user.",
)
async def get_recent_activity(
    limit: int = 20,
    activity_type: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> ActivityList:
    """Get recent activity for the current user."""
    service = get_activity_service(db)
    
    from api.schemas.progress import ActivityType
    type_enum = ActivityType(activity_type) if activity_type else None
    
    activities = await service.get_recent_activity(
        current_user_id,
        limit=limit,
        activity_type=type_enum,
    )
    return ActivityList(items=activities, total=len(activities))


@router.post(
    "/activity",
    response_model=Activity,
    status_code=status.HTTP_201_CREATED,
    summary="Log activity",
    description="Log a new activity.",
)
async def log_activity(
    activity_data: ActivityCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> Activity:
    """Log a new activity."""
    service = get_activity_service(db)
    
    activity = await service.log_activity(
        user_id=current_user_id,
        activity_type=activity_data.activity_type,
        item_slug=activity_data.item_slug,
        metadata=activity_data.metadata,
    )
    
    return activity


@router.get(
    "/activity/summary",
    response_model=ActivitySummary,
    summary="Get activity summary",
    description="Get activity summary for a time period.",
)
async def get_activity_summary(
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> ActivitySummary:
    """Get activity summary for the specified number of days."""
    service = get_activity_service(db)
    summary = await service.get_activity_summary(current_user_id, days=days)
    return ActivitySummary(**summary)


@router.get(
    "/activity/stats",
    response_model=dict,
    summary="Get activity stats",
    description="Get detailed activity statistics.",
)
async def get_activity_stats(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> dict:
    """Get detailed activity statistics."""
    service = get_activity_service(db)
    stats = await service.get_activity_stats(current_user_id, days=days)
    return stats

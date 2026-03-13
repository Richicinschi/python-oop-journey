"""Progress tracking endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.schemas.progress import (
    Progress,
    ProgressCreate,
    ProgressList,
    ProgressStats,
    ProgressUpdate,
    WeekProgress,
    ProblemStatus,
)
from api.services.progress import get_progress_service, ProgressService
from api.services.activity import get_activity_service, ActivityService
from api.models.activity import ActivityType

router = APIRouter()

# Mock current user dependency - replace with actual auth
current_user_id = "mock-user-id"


@router.get(
    "/progress",
    response_model=ProgressList,
    summary="Get all user progress",
    description="Get progress for all problems for the current user.",
)
async def get_all_progress(
    db: AsyncSession = Depends(get_db),
) -> ProgressList:
    """Get all progress entries for the current user."""
    service = get_progress_service(db)
    progress_list = await service.get_all_progress(current_user_id)
    return ProgressList(items=progress_list, total=len(progress_list))


@router.get(
    "/progress/{problem_slug}",
    response_model=Progress,
    summary="Get problem progress",
    description="Get progress for a specific problem.",
    responses={
        404: {"description": "Progress not found"},
    },
)
async def get_problem_progress(
    problem_slug: str,
    db: AsyncSession = Depends(get_db),
) -> Progress:
    """Get progress for a specific problem."""
    service = get_progress_service(db)
    progress = await service.get_progress(current_user_id, problem_slug)
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No progress found for problem: {problem_slug}",
        )
    
    return progress


@router.post(
    "/progress/{problem_slug}",
    response_model=Progress,
    summary="Update progress",
    description="Update progress for a specific problem.",
)
async def update_progress(
    problem_slug: str,
    update: ProgressUpdate,
    db: AsyncSession = Depends(get_db),
) -> Progress:
    """Update progress for a specific problem."""
    progress_service = get_progress_service(db)
    activity_service = get_activity_service(db)
    
    # Update progress
    progress = await progress_service.update_progress(
        user_id=current_user_id,
        problem_slug=problem_slug,
        status=update.status,
        time_spent_seconds=update.time_spent_seconds,
    )
    
    # Log activity if status changed
    if update.status:
        if update.status == ProblemStatus.SOLVED:
            await activity_service.log_activity(
                user_id=current_user_id,
                activity_type=ActivityType.SOLVED_PROBLEM,
                item_slug=problem_slug,
            )
        elif update.status == ProblemStatus.IN_PROGRESS:
            await activity_service.log_activity(
                user_id=current_user_id,
                activity_type=ActivityType.STARTED_PROBLEM,
                item_slug=problem_slug,
            )
    
    # Record attempt if requested
    if update.add_attempt:
        progress = await progress_service.record_attempt(current_user_id, problem_slug)
        await activity_service.log_activity(
            user_id=current_user_id,
            activity_type=ActivityType.ATTEMPTED_PROBLEM,
            item_slug=problem_slug,
        )
    
    return progress


@router.post(
    "/progress/{problem_slug}/attempt",
    response_model=Progress,
    summary="Record attempt",
    description="Record an attempt on a problem.",
)
async def record_attempt(
    problem_slug: str,
    db: AsyncSession = Depends(get_db),
) -> Progress:
    """Record an attempt on a problem."""
    progress_service = get_progress_service(db)
    activity_service = get_activity_service(db)
    
    progress = await progress_service.record_attempt(current_user_id, problem_slug)
    
    await activity_service.log_activity(
        user_id=current_user_id,
        activity_type=ActivityType.ATTEMPTED_PROBLEM,
        item_slug=problem_slug,
    )
    
    return progress


@router.get(
    "/progress/stats/overall",
    response_model=ProgressStats,
    summary="Get overall stats",
    description="Get overall progress statistics including streak and completion percentage.",
)
async def get_overall_stats(
    total_problems: int = 50,
    db: AsyncSession = Depends(get_db),
) -> ProgressStats:
    """Get overall progress statistics."""
    service = get_progress_service(db)
    stats = await service.get_overall_progress(current_user_id, total_problems)
    return ProgressStats(**stats)


@router.get(
    "/progress/week/{week_slug}",
    response_model=WeekProgress,
    summary="Get week progress",
    description="Get progress statistics for a specific week.",
)
async def get_week_progress(
    week_slug: str,
    db: AsyncSession = Depends(get_db),
) -> WeekProgress:
    """Get progress for a specific week."""
    service = get_progress_service(db)
    stats = await service.get_week_progress(current_user_id, week_slug)
    return WeekProgress(**stats)

"""User and progress endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.dependencies.auth import get_current_user_id
from api.models.draft import Draft
from api.models.progress import Progress, ProblemStatus
from api.models.user import User
from api.schemas.user import Draft as DraftSchema
from api.schemas.user import DraftCreate
from api.schemas.user import Progress as ProgressSchema
from api.schemas.user import ProgressCreate, UserStats, User
from api.services.progress import get_progress_service
from api.services.draft import get_draft_service

router = APIRouter()


@router.get(
    "/users/me",
    response_model=User,
    summary="Get current user profile",
    description="Get the current user's profile and stats.",
    responses={
        401: {"description": "Authentication required"},
        404: {"description": "User not found"},
    },
)
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    """Get current user profile.
    
    TODO: Replace with actual user lookup from database when user management
    system is fully implemented. Currently returns a mock user profile.
    """
    # TODO: Query actual user from database
    # result = await db.execute(select(User).where(User.id == current_user_id))
    # user = result.scalar_one_or_none()
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")
    
    # Return mock user for development
    return User(
        id=current_user_id,
        email="user@example.com",
        display_name="Developer User",
        created_at="2024-01-01T00:00:00",
        updated_at="2024-01-01T00:00:00",
        last_seen="2024-01-01T00:00:00",
        is_active=True,
    )


@router.get(
    "/users/me/stats",
    response_model=UserStats,
    summary="Get user statistics",
    description="Get learning statistics for the current user.",
)
async def get_my_stats(
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    """Get user stats using the progress service."""
    progress_service = get_progress_service(db)
    
    # Get overall stats from progress service
    stats = await progress_service.get_overall_progress(
        current_user_id, 
        total_problems=50
    )
    
    return UserStats(
        total_problems=stats.get("total_problems", 50),
        completed_problems=stats.get("completed", 0),
        in_progress_problems=stats.get("in_progress", 0),
        completion_percentage=stats.get("completion_percentage", 0.0),
        streak_days=stats.get("streak_days", 0),
        favorite_week=stats.get("favorite_week"),
    )


@router.get(
    "/users/me/progress",
    response_model=list[ProgressSchema],
    summary="Get user progress",
    description="Get all progress entries for the current user.",
)
async def get_my_progress(
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    """Get user progress using the progress service."""
    progress_service = get_progress_service(db)
    
    progress_list = await progress_service.get_all_progress(current_user_id)
    
    # Convert to schema format
    return [
        ProgressSchema(
            id=p.id,
            user_id=p.user_id,
            problem_slug=p.problem_slug,
            status=p.status.value if hasattr(p.status, 'value') else p.status,
            attempts=p.attempts,
            completed_at=p.completed_at,
            created_at=p.created_at,
            updated_at=p.updated_at,
        )
        for p in progress_list
    ]


@router.post(
    "/users/me/progress",
    response_model=ProgressSchema,
    summary="Update progress",
    description="Update or create progress for a problem.",
)
async def update_progress(
    progress: ProgressCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    """Update problem progress using the progress service."""
    progress_service = get_progress_service(db)
    
    updated = await progress_service.update_progress(
        user_id=current_user_id,
        problem_slug=progress.problem_slug,
        status=progress.status,
    )
    
    return ProgressSchema(
        id=updated.id,
        user_id=updated.user_id,
        problem_slug=updated.problem_slug,
        status=updated.status.value if hasattr(updated.status, 'value') else updated.status,
        attempts=updated.attempts,
        completed_at=updated.completed_at,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
    )


@router.get(
    "/users/me/drafts",
    response_model=list[DraftSchema],
    summary="Get user drafts",
    description="Get all saved code drafts for the current user.",
)
async def get_my_drafts(
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    """Get user drafts using the draft service."""
    draft_service = get_draft_service(db)
    
    drafts = await draft_service.list_drafts(current_user_id)
    
    return [
        DraftSchema(
            id=d.id,
            user_id=d.user_id,
            problem_slug=d.problem_slug,
            code=d.code,
            saved_at=d.saved_at,
            created_at=d.created_at,
        )
        for d in drafts
    ]


@router.get(
    "/users/me/drafts/{problem_slug}",
    response_model=DraftSchema,
    summary="Get draft for problem",
    description="Get the saved draft for a specific problem.",
    responses={
        404: {"description": "Draft not found"},
    },
)
async def get_draft(
    problem_slug: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    """Get draft for a problem using the draft service."""
    draft_service = get_draft_service(db)
    
    draft = await draft_service.get_draft(current_user_id, problem_slug)
    
    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No draft found for problem: {problem_slug}",
        )
    
    return DraftSchema(
        id=draft.id,
        user_id=draft.user_id,
        problem_slug=draft.problem_slug,
        code=draft.code,
        saved_at=draft.saved_at,
        created_at=draft.created_at,
    )


@router.post(
    "/users/me/drafts",
    response_model=DraftSchema,
    summary="Save draft",
    description="Save or update a code draft for a problem.",
)
async def save_draft(
    draft: DraftCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    """Save code draft using the draft service."""
    draft_service = get_draft_service(db)
    
    saved = await draft_service.save_draft(
        user_id=current_user_id,
        problem_slug=draft.problem_slug,
        code=draft.code,
        is_auto_save=False,
    )
    
    return DraftSchema(
        id=saved.id,
        user_id=saved.user_id,
        problem_slug=saved.problem_slug,
        code=saved.code,
        saved_at=saved.saved_at,
        created_at=saved.created_at,
    )


@router.delete(
    "/users/me/drafts/{problem_slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete draft",
    description="Delete the saved draft for a specific problem.",
    responses={
        404: {"description": "Draft not found"},
    },
)
async def delete_draft(
    problem_slug: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    """Delete draft using the draft service."""
    draft_service = get_draft_service(db)
    
    deleted = await draft_service.delete_draft(current_user_id, problem_slug)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No draft found for problem: {problem_slug}",
        )

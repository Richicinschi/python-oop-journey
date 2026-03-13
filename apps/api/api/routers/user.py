"""User and progress endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.models.draft import Draft
from api.models.progress import Progress, ProblemStatus
from api.models.user import User
from api.schemas.user import Draft as DraftSchema
from api.schemas.user import DraftCreate
from api.schemas.user import Progress as ProgressSchema
from api.schemas.user import ProgressCreate, UserStats

router = APIRouter()


# TODO: Replace with actual auth dependency
async def get_current_user_dependency(
    db: AsyncSession = Depends(get_db),
) -> User:
    """Placeholder for getting current user from JWT."""
    # This will be replaced with proper JWT auth
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication required",
    )


@router.get(
    "/users/me",
    summary="Get current user profile",
    description="Get the current user's profile and stats.",
)
async def get_me():
    """Get current user (placeholder)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication required",
    )


@router.get(
    "/users/me/stats",
    response_model=UserStats,
    summary="Get user statistics",
    description="Get learning statistics for the current user.",
)
async def get_my_stats():
    """Get user stats (placeholder)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication required",
    )


@router.get(
    "/users/me/progress",
    response_model=list[ProgressSchema],
    summary="Get user progress",
    description="Get all progress entries for the current user.",
)
async def get_my_progress():
    """Get user progress (placeholder)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication required",
    )


@router.post(
    "/users/me/progress",
    response_model=ProgressSchema,
    summary="Update progress",
    description="Update or create progress for a problem.",
)
async def update_progress(
    progress: ProgressCreate,
    db: AsyncSession = Depends(get_db),
):
    """Update problem progress (placeholder)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication required",
    )


@router.get(
    "/users/me/drafts",
    response_model=list[DraftSchema],
    summary="Get user drafts",
    description="Get all saved code drafts for the current user.",
)
async def get_my_drafts():
    """Get user drafts (placeholder)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication required",
    )


@router.get(
    "/users/me/drafts/{problem_slug}",
    response_model=DraftSchema,
    summary="Get draft for problem",
    description="Get the saved draft for a specific problem.",
)
async def get_draft(problem_slug: str):
    """Get draft for a problem (placeholder)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication required",
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
):
    """Save code draft (placeholder)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication required",
    )


@router.delete(
    "/users/me/drafts/{problem_slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete draft",
    description="Delete the saved draft for a specific problem.",
)
async def delete_draft(problem_slug: str):
    """Delete draft (placeholder)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication required",
    )

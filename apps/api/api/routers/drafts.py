"""Draft management endpoints."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.dependencies.auth import get_current_user_id
from api.schemas.progress import Draft, DraftCreate, DraftList, DraftUpdate
from api.services.draft import get_draft_service, DraftService

router = APIRouter()

# TODO: Replace with actual auth dependency that validates JWT tokens
# For now, using a dependency that returns a mock user ID for development


@router.get(
    "/drafts",
    response_model=DraftList,
    summary="List all drafts",
    description="Get all saved code drafts for the current user.",
)
async def list_drafts(
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> DraftList:
    """List all drafts for the current user."""
    service = get_draft_service(db)
    drafts = await service.list_drafts(current_user_id, limit=limit, offset=offset)
    return DraftList(items=drafts, total=len(drafts))


@router.get(
    "/drafts/{problem_slug}",
    response_model=Draft,
    summary="Get draft",
    description="Get saved code draft for a specific problem.",
    responses={
        404: {"description": "Draft not found"},
    },
)
async def get_draft(
    problem_slug: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> Draft:
    """Get draft for a specific problem."""
    service = get_draft_service(db)
    draft = await service.get_draft(current_user_id, problem_slug)
    
    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No draft found for problem: {problem_slug}",
        )
    
    return draft


@router.post(
    "/drafts/{problem_slug}",
    response_model=Draft,
    summary="Save draft",
    description="Save or update code draft for a specific problem.",
)
async def save_draft(
    problem_slug: str,
    draft_data: DraftUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> Draft:
    """Save or update a draft."""
    service = get_draft_service(db)
    draft = await service.save_draft(
        user_id=current_user_id,
        problem_slug=problem_slug,
        code=draft_data.code,
        is_auto_save=draft_data.is_auto_save,
    )
    return draft


@router.delete(
    "/drafts/{problem_slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete draft",
    description="Delete saved code draft for a specific problem.",
    responses={
        404: {"description": "Draft not found"},
    },
)
async def delete_draft(
    problem_slug: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> None:
    """Delete draft for a specific problem."""
    service = get_draft_service(db)
    deleted = await service.delete_draft(current_user_id, problem_slug)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No draft found for problem: {problem_slug}",
        )

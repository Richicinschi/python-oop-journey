"""Bookmark management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.schemas.progress import (
    Bookmark,
    BookmarkCheck,
    BookmarkCreate,
    BookmarkList,
    BookmarkUpdate,
)
from api.services.bookmark import get_bookmark_service, BookmarkService
from api.services.activity import get_activity_service, ActivityService
from api.models.activity import ActivityType

router = APIRouter()

# Mock current user dependency - replace with actual auth
current_user_id = "mock-user-id"


@router.get(
    "/bookmarks",
    response_model=BookmarkList,
    summary="List bookmarks",
    description="Get all bookmarks for the current user.",
)
async def list_bookmarks(
    item_type: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
) -> BookmarkList:
    """List all bookmarks for the current user."""
    service = get_bookmark_service(db)
    
    from api.schemas.progress import ItemType
    type_enum = ItemType(item_type) if item_type else None
    
    bookmarks = await service.list_drafts(
        current_user_id,
        item_type=type_enum,
        limit=limit,
        offset=offset,
    )
    return BookmarkList(items=bookmarks, total=len(bookmarks))


@router.post(
    "/bookmarks",
    response_model=Bookmark,
    status_code=status.HTTP_201_CREATED,
    summary="Create bookmark",
    description="Create a new bookmark.",
)
async def create_bookmark(
    bookmark_data: BookmarkCreate,
    db: AsyncSession = Depends(get_db),
) -> Bookmark:
    """Create a new bookmark."""
    bookmark_service = get_bookmark_service(db)
    activity_service = get_activity_service(db)
    
    bookmark = await bookmark_service.create_bookmark(
        user_id=current_user_id,
        item_type=bookmark_data.item_type,
        item_slug=bookmark_data.item_slug,
        notes=bookmark_data.notes,
    )
    
    # Log activity
    await activity_service.log_activity(
        user_id=current_user_id,
        activity_type=ActivityType.CREATED_BOOKMARK,
        item_slug=bookmark_data.item_slug,
        metadata={"item_type": bookmark_data.item_type.value},
    )
    
    return bookmark


@router.delete(
    "/bookmarks/{bookmark_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete bookmark",
    description="Delete a bookmark by its ID.",
    responses={
        404: {"description": "Bookmark not found"},
    },
)
async def delete_bookmark(
    bookmark_id: str,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a bookmark."""
    bookmark_service = get_bookmark_service(db)
    activity_service = get_activity_service(db)
    
    # Get bookmark info before deleting for activity log
    bookmark = await bookmark_service.get_bookmark_by_id(current_user_id, bookmark_id)
    
    deleted = await bookmark_service.delete_bookmark_by_id(current_user_id, bookmark_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bookmark not found: {bookmark_id}",
        )
    
    # Log activity
    if bookmark:
        await activity_service.log_activity(
            user_id=current_user_id,
            activity_type=ActivityType.DELETED_BOOKMARK,
            item_slug=bookmark.item_slug,
            metadata={"item_type": bookmark.item_type.value},
        )


@router.get(
    "/bookmarks/check",
    response_model=BookmarkCheck,
    summary="Check bookmark status",
    description="Check if an item is bookmarked.",
)
async def check_bookmark(
    item_type: str,
    item_slug: str,
    db: AsyncSession = Depends(get_db),
) -> BookmarkCheck:
    """Check if an item is bookmarked."""
    service = get_bookmark_service(db)
    
    from api.schemas.progress import ItemType
    type_enum = ItemType(item_type)
    
    bookmark = await service.get_bookmark(current_user_id, type_enum, item_slug)
    
    return BookmarkCheck(
        is_bookmarked=bookmark is not None,
        bookmark_id=bookmark.id if bookmark else None,
    )


@router.patch(
    "/bookmarks/{bookmark_id}",
    response_model=Bookmark,
    summary="Update bookmark",
    description="Update bookmark notes.",
    responses={
        404: {"description": "Bookmark not found"},
    },
)
async def update_bookmark(
    bookmark_id: str,
    update_data: BookmarkUpdate,
    db: AsyncSession = Depends(get_db),
) -> Bookmark:
    """Update bookmark notes."""
    service = get_bookmark_service(db)
    
    bookmark = await service.update_bookmark_notes(
        current_user_id,
        bookmark_id,
        update_data.notes,
    )
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bookmark not found: {bookmark_id}",
        )
    
    return bookmark


@router.post(
    "/bookmarks/toggle",
    response_model=BookmarkCheck,
    summary="Toggle bookmark",
    description="Toggle bookmark status for an item. Creates if not exists, deletes if exists.",
)
async def toggle_bookmark(
    bookmark_data: BookmarkCreate,
    db: AsyncSession = Depends(get_db),
) -> BookmarkCheck:
    """Toggle bookmark status for an item."""
    bookmark_service = get_bookmark_service(db)
    activity_service = get_activity_service(db)
    
    is_bookmarked, bookmark = await bookmark_service.toggle_bookmark(
        user_id=current_user_id,
        item_type=bookmark_data.item_type,
        item_slug=bookmark_data.item_slug,
        notes=bookmark_data.notes,
    )
    
    # Log activity
    if is_bookmarked:
        await activity_service.log_activity(
            user_id=current_user_id,
            activity_type=ActivityType.CREATED_BOOKMARK,
            item_slug=bookmark_data.item_slug,
            metadata={"item_type": bookmark_data.item_type.value},
        )
    else:
        await activity_service.log_activity(
            user_id=current_user_id,
            activity_type=ActivityType.DELETED_BOOKMARK,
            item_slug=bookmark_data.item_slug,
            metadata={"item_type": bookmark_data.item_type.value},
        )
    
    return BookmarkCheck(
        is_bookmarked=is_bookmarked,
        bookmark_id=bookmark.id if bookmark else None,
    )

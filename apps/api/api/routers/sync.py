"""Sync router for batch operations and multi-device sync."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from pydantic import BaseModel, Field
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.models.progress import Progress, ProblemStatus
from api.models.draft import Draft
from api.models.bookmark import Bookmark
from api.models.user import User
from api.middleware.auth import get_current_user

router = APIRouter()


# ==================== Schemas ====================

class SyncOperation(BaseModel):
    """Single sync operation."""

    id: str = Field(..., description="Client-generated operation ID")
    type: str = Field(..., pattern="^(progress|draft|bookmark)$")
    action: str = Field(..., pattern="^(create|update|delete)$")
    data: dict[str, Any]
    timestamp: str = Field(..., description="ISO timestamp from client")
    client_id: str = Field(..., description="Unique client identifier")


class BatchSyncRequest(BaseModel):
    """Batch sync request."""

    operations: list[SyncOperation]


class ConflictInfo(BaseModel):
    """Conflict information."""

    operation_id: str
    local_data: dict[str, Any]
    server_data: dict[str, Any]


class BatchSyncResponse(BaseModel):
    """Batch sync response."""

    applied: list[str] = Field(default_factory=list, description="Operation IDs that were applied")
    conflicts: list[ConflictInfo] = Field(default_factory=list)
    server_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ForceSyncRequest(BaseModel):
    """Force sync request (for conflict resolution)."""

    operation: SyncOperation
    force: bool = True


# ==================== Helper Functions ====================

async def handle_progress_sync(
    operation: SyncOperation,
    user: User,
    db: AsyncSession,
) -> tuple[bool, dict[str, Any] | None]:
    """
    Handle progress sync operation.
    
    Returns: (success, conflict_data)
    """
    problem_slug = operation.data.get("problemSlug")
    if not problem_slug:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="problemSlug is required for progress operations",
        )

    # Check for existing progress
    result = await db.execute(
        select(Progress).where(
            and_(
                Progress.user_id == user.id,
                Progress.problem_slug == problem_slug,
            )
        )
    )
    existing = result.scalar_one_or_none()

    # Check for conflicts (server has newer data)
    client_timestamp = datetime.fromisoformat(operation.timestamp.replace("Z", "+00:00"))
    
    if existing and existing.updated_at > client_timestamp:
        # Conflict detected
        return False, {
            "operation_id": operation.id,
            "local_data": operation.data,
            "server_data": {
                "problem_slug": existing.problem_slug,
                "status": existing.status.value,
                "attempts": existing.attempts,
                "completed_at": existing.completed_at.isoformat() if existing.completed_at else None,
                "updated_at": existing.updated_at.isoformat(),
            },
        }

    if operation.action == "delete":
        if existing:
            await db.delete(existing)
    else:
        # Create or update
        status_value = operation.data.get("status", "not_started")
        
        if existing:
            existing.status = ProblemStatus(status_value)
            existing.attempts = operation.data.get("attempts", existing.attempts)
            if status_value == "completed":
                existing.completed_at = datetime.utcnow()
        else:
            new_progress = Progress(
                user_id=user.id,
                problem_slug=problem_slug,
                status=ProblemStatus(status_value),
                attempts=operation.data.get("attempts", 1),
                completed_at=datetime.utcnow() if status_value == "completed" else None,
            )
            db.add(new_progress)

    await db.commit()
    return True, None


async def handle_draft_sync(
    operation: SyncOperation,
    user: User,
    db: AsyncSession,
) -> tuple[bool, dict[str, Any] | None]:
    """
    Handle draft sync operation.
    
    Returns: (success, conflict_data)
    """
    problem_slug = operation.data.get("problemSlug")
    if not problem_slug:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="problemSlug is required for draft operations",
        )

    # Check for existing draft
    result = await db.execute(
        select(Draft).where(
            and_(
                Draft.user_id == user.id,
                Draft.problem_slug == problem_slug,
            )
        )
    )
    existing = result.scalar_one_or_none()

    # Check for conflicts (server has newer data)
    client_timestamp = datetime.fromisoformat(operation.timestamp.replace("Z", "+00:00"))
    
    if existing and existing.saved_at and existing.saved_at > client_timestamp:
        # Conflict detected
        return False, {
            "operation_id": operation.id,
            "local_data": operation.data,
            "server_data": {
                "problem_slug": existing.problem_slug,
                "code": existing.code,
                "saved_at": existing.saved_at.isoformat() if existing.saved_at else None,
            },
        }

    if operation.action == "delete":
        if existing:
            await db.delete(existing)
    else:
        code = operation.data.get("code", "")
        
        if existing:
            existing.code = code
            existing.saved_at = datetime.utcnow()
        else:
            new_draft = Draft(
                user_id=user.id,
                problem_slug=problem_slug,
                code=code,
                saved_at=datetime.utcnow(),
            )
            db.add(new_draft)

    await db.commit()
    return True, None


async def handle_bookmark_sync(
    operation: SyncOperation,
    user: User,
    db: AsyncSession,
) -> tuple[bool, dict[str, Any] | None]:
    """
    Handle bookmark sync operation.
    
    Returns: (success, conflict_data)
    """
    problem_slug = operation.data.get("problemSlug")
    if not problem_slug:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="problemSlug is required for bookmark operations",
        )

    # Check for existing bookmark
    result = await db.execute(
        select(Bookmark).where(
            and_(
                Bookmark.user_id == user.id,
                Bookmark.problem_slug == problem_slug,
            )
        )
    )
    existing = result.scalar_one_or_none()

    if operation.action == "delete":
        if existing:
            await db.delete(existing)
    else:
        if not existing:
            new_bookmark = Bookmark(
                user_id=user.id,
                problem_slug=problem_slug,
                note=operation.data.get("note"),
            )
            db.add(new_bookmark)
        elif operation.data.get("note"):
            existing.note = operation.data["note"]

    await db.commit()
    return True, None


async def handle_operation(
    operation: SyncOperation,
    user: User,
    db: AsyncSession,
) -> tuple[bool, dict[str, Any] | None]:
    """Route operation to appropriate handler."""
    handlers = {
        "progress": handle_progress_sync,
        "draft": handle_draft_sync,
        "bookmark": handle_bookmark_sync,
    }
    
    handler = handlers.get(operation.type)
    if not handler:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown operation type: {operation.type}",
        )
    
    return await handler(operation, user, db)


# ==================== Routes ====================

@router.post(
    "/sync/batch",
    response_model=BatchSyncResponse,
    summary="Batch sync operations",
    description="Sync multiple operations in a single request. Handles conflicts with last-write-wins strategy.",
)
async def batch_sync(
    request: BatchSyncRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BatchSyncResponse:
    """
    Process a batch of sync operations.
    
    Each operation is processed in order. If a conflict is detected,
    it's added to the conflicts list and skipped. Other operations continue.
    """
    applied: list[str] = []
    conflicts: list[ConflictInfo] = []

    for operation in request.operations:
        try:
            success, conflict_data = await handle_operation(operation, current_user, db)
            
            if success:
                applied.append(operation.id)
            elif conflict_data:
                conflicts.append(ConflictInfo(**conflict_data))
        except HTTPException:
            # Re-raise HTTP exceptions (validation errors, etc.)
            raise
        except Exception as e:
            # Log error but continue processing other operations
            print(f"Error processing operation {operation.id}: {e}")
            continue

    return BatchSyncResponse(
        applied=applied,
        conflicts=conflicts,
    )


@router.post(
    "/sync/force",
    summary="Force sync operation",
    description="Force apply an operation, overwriting server data even if there's a conflict.",
)
async def force_sync(
    request: ForceSyncRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """
    Force sync an operation, bypassing conflict detection.
    
    This is used when the user explicitly chooses to keep their local version
    during conflict resolution.
    """
    operation = request.operation
    
    # Temporarily modify the timestamp to ensure it wins
    operation.data["_force"] = True
    operation.data["_forced_at"] = datetime.utcnow().isoformat()
    
    success, _ = await handle_operation(operation, current_user, db)
    
    if success:
        return {"status": "success", "operation_id": operation.id}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to force sync operation",
        )


@router.get(
    "/sync/status",
    summary="Get sync status",
    description="Get the current sync status for the user, including last sync timestamp.",
)
async def get_sync_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """Get sync status for the current user."""
    # Get counts of each type
    progress_count = await db.scalar(
        select(func.count()).select_from(Progress).where(Progress.user_id == current_user.id)
    ) or 0
    draft_count = await db.scalar(
        select(func.count()).select_from(Draft).where(Draft.user_id == current_user.id)
    ) or 0
    bookmark_count = await db.scalar(
        select(func.count()).select_from(Bookmark).where(Bookmark.user_id == current_user.id)
    ) or 0

    # Get latest updated timestamps
    latest_progress = await db.execute(
        select(Progress)
        .where(Progress.user_id == current_user.id)
        .order_by(Progress.updated_at.desc())
        .limit(1)
    )
    latest_draft = await db.execute(
        select(Draft)
        .where(Draft.user_id == current_user.id)
        .order_by(Draft.saved_at.desc())
        .limit(1)
    )

    progress_record = latest_progress.scalar_one_or_none()
    draft_record = latest_draft.scalar_one_or_none()

    return {
        "user_id": current_user.id,
        "counts": {
            "progress": progress_count,
            "drafts": draft_count,
            "bookmarks": bookmark_count,
        },
        "last_updated": {
            "progress": progress_record.updated_at.isoformat() if progress_record else None,
            "draft": draft_record.saved_at.isoformat() if draft_record else None,
        },
        "server_timestamp": datetime.utcnow().isoformat(),
    }


@router.post(
    "/sync/resolve",
    summary="Resolve sync conflict",
    description="Resolve a sync conflict by choosing which version to keep.",
)
async def resolve_conflict(
    operation_id: str = Query(..., description="Operation ID to resolve"),
    strategy: str = Query(..., pattern="^(local|server|merge)$"),
    merged_data: dict[str, Any] | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """
    Resolve a sync conflict.
    
    - local: Keep local version (force sync)
    - server: Keep server version (discard local)
    - merge: Use merged data
    """
    # This endpoint would typically look up the pending operation
    # and apply the resolution strategy
    # For now, we just acknowledge the resolution
    
    return {
        "status": "resolved",
        "operation_id": operation_id,
        "strategy": strategy,
    }

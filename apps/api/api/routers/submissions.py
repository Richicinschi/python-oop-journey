"""Submission management endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.middleware.auth import get_current_user, optional_auth
from api.models.user import User
from api.schemas.submission import (
    Submission,
    SubmissionCreate,
    SubmissionUpdate,
    SubmissionList,
    SubmissionListItem,
    SubmissionResponse,
    SubmissionChecklist,
    SubmissionFilters,
    SubmissionStatus,
    SubmissionComment,
    SubmissionCommentCreate,
    SubmissionCommentList,
    ReviewQueue,
    ReviewQueueItem,
    BatchReviewAction,
    BatchReviewResult,
    GamificationStats,
)
from api.services.submission import get_submission_service, SubmissionService

router = APIRouter()


@router.post(
    "/projects/{project_slug}/submit",
    response_model=SubmissionResponse,
    summary="Submit project",
    description="Submit a project for review.",
    responses={
        400: {"description": "Invalid submission"},
        401: {"description": "Not authenticated"},
    },
)
async def create_submission(
    project_slug: str,
    data: SubmissionCreate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SubmissionResponse:
    """Submit a project for review.
    
    Creates a new submission with automated checks and test results.
    """
    service = get_submission_service(db)
    
    # Set project slug from path
    data.project_slug = project_slug
    
    response = await service.create_submission(user.id, data)
    return response


@router.get(
    "/projects/{project_slug}/checklist",
    response_model=SubmissionChecklist,
    summary="Get pre-submission checklist",
    description="Check if project is ready for submission.",
)
async def get_checklist(
    project_slug: str,
    files: dict[str, str],
    user: Annotated[User | None, Depends(optional_auth)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SubmissionChecklist:
    """Get pre-submission checklist for files."""
    service = get_submission_service(db)
    return await service.get_submission_checklist(files, project_slug)


@router.get(
    "/submissions",
    response_model=SubmissionList,
    summary="List submissions",
    description="Get all submissions for the current user.",
)
async def list_submissions(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    status: SubmissionStatus | None = None,
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> SubmissionList:
    """List all submissions for the current user."""
    service = get_submission_service(db)
    submissions, total = await service.get_user_submissions(
        user.id, limit=limit, offset=offset, status=status
    )
    
    # Convert to list items with summaries
    items = []
    for s in submissions:
        test_summary = s.test_results.get("test_summary", {
            "total": s.test_results.get("total", 0),
            "passed": s.test_results.get("passed", 0),
            "failed": s.test_results.get("failed", 0),
        })
        metrics_summary = {
            "lines_of_code": s.metrics.get("lines_of_code", 0),
            "function_count": s.metrics.get("function_count", 0),
        }
        
        items.append(SubmissionListItem(
            id=s.id,
            project_slug=s.project_slug,
            project_name=s.project_slug.replace("-", " ").title(),
            week_slug=s.week_slug,
            day_slug=s.day_slug,
            submitted_at=s.submitted_at,
            status=SubmissionStatus(s.status),
            test_summary=test_summary,
            metrics_summary=metrics_summary,
            is_exemplary=s.is_exemplary,
        ))
    
    return SubmissionList(
        items=items,
        total=total,
        page=offset // limit + 1,
        page_size=limit,
    )


@router.get(
    "/submissions/{submission_id}",
    response_model=Submission,
    summary="Get submission",
    description="Get detailed information about a submission.",
    responses={
        404: {"description": "Submission not found"},
    },
)
async def get_submission(
    submission_id: str,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Submission:
    """Get a specific submission by ID."""
    service = get_submission_service(db)
    submission = await service.get_submission(submission_id)
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found",
        )
    
    # Check ownership (or admin)
    if submission.user_id != user.id and not hasattr(user, 'is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this submission",
        )
    
    # Get reviewer name if available
    reviewer_name = None
    if submission.reviewer:
        reviewer_name = submission.reviewer.display_name or submission.reviewer.email
    
    return Submission(
        id=submission.id,
        user_id=submission.user_id,
        project_slug=submission.project_slug,
        project_name=submission.project_slug.replace("-", " ").title(),
        week_slug=submission.week_slug,
        day_slug=submission.day_slug,
        files=submission.files,
        submitted_at=submission.submitted_at,
        status=SubmissionStatus(submission.status),
        reviewer_notes=submission.reviewer_notes,
        reviewed_at=submission.reviewed_at,
        reviewed_by=submission.reviewed_by,
        reviewer_name=reviewer_name,
        test_results=submission.test_results,
        metrics=submission.metrics,
        is_exemplary=submission.is_exemplary,
        showcase_opt_in=submission.showcase_opt_in,
    )


@router.get(
    "/submissions/{submission_id}/files",
    response_model=dict[str, str],
    summary="Get submission files",
    description="Get the code snapshot for a submission.",
    responses={
        404: {"description": "Submission not found"},
    },
)
async def get_submission_files(
    submission_id: str,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    """Get the code snapshot for a submission."""
    service = get_submission_service(db)
    submission = await service.get_submission(submission_id)
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found",
        )
    
    # Check ownership (or admin)
    if submission.user_id != user.id and not hasattr(user, 'is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this submission",
        )
    
    return submission.files


# Admin/Reviewer endpoints

@router.get(
    "/admin/reviews/queue",
    response_model=ReviewQueue,
    summary="Get review queue",
    description="Get queue of pending submissions for review (admin only).",
)
async def get_review_queue(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> ReviewQueue:
    """Get the review queue for mentors."""
    # SECURITY: Enforce admin authorization
    if not getattr(user, 'is_admin', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    service = get_submission_service(db)
    pending, total = await service.get_pending_reviews(limit=limit)
    
    from datetime import datetime
    items = []
    for s in pending:
        waiting_hours = (datetime.utcnow() - s.submitted_at).total_seconds() / 3600
        test_summary = s.test_results.get("test_summary", {
            "total": s.test_results.get("total", 0),
            "passed": s.test_results.get("passed", 0),
        })
        metrics_summary = {
            "lines_of_code": s.metrics.get("lines_of_code", 0),
        }
        
        items.append(ReviewQueueItem(
            id=s.id,
            project_slug=s.project_slug,
            project_name=s.project_slug.replace("-", " ").title(),
            user_id=s.user_id,
            user_name=s.user.display_name if s.user else None,
            submitted_at=s.submitted_at,
            waiting_hours=round(waiting_hours, 1),
            test_summary=test_summary,
            metrics_summary=metrics_summary,
            priority_score=round(waiting_hours * 0.5 + test_summary.get("passed", 0) * 0.1, 2),
        ))
    
    return ReviewQueue(
        pending_count=total,
        items=items,
        my_reviews_today=0,  # TODO: Track reviewer stats
        avg_review_time_hours=None,
    )


@router.post(
    "/admin/submissions/{submission_id}/review",
    response_model=Submission,
    summary="Review submission",
    description="Review a submission and update its status (admin only).",
    responses={
        404: {"description": "Submission not found"},
    },
)
async def review_submission(
    submission_id: str,
    data: SubmissionUpdate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Submission:
    """Review a submission and update its status."""
    # SECURITY: Enforce admin authorization
    if not getattr(user, 'is_admin', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    service = get_submission_service(db)
    submission = await service.review_submission(submission_id, user.id, data)
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found",
        )
    
    # Get reviewer name
    reviewer_name = None
    if submission.reviewer:
        reviewer_name = submission.reviewer.display_name or submission.reviewer.email
    
    return Submission(
        id=submission.id,
        user_id=submission.user_id,
        project_slug=submission.project_slug,
        project_name=submission.project_slug.replace("-", " ").title(),
        week_slug=submission.week_slug,
        day_slug=submission.day_slug,
        files=submission.files,
        submitted_at=submission.submitted_at,
        status=SubmissionStatus(submission.status),
        reviewer_notes=submission.reviewer_notes,
        reviewed_at=submission.reviewed_at,
        reviewed_by=submission.reviewed_by,
        reviewer_name=reviewer_name,
        test_results=submission.test_results,
        metrics=submission.metrics,
        is_exemplary=submission.is_exemplary,
        showcase_opt_in=submission.showcase_opt_in,
    )


@router.post(
    "/admin/reviews/batch",
    response_model=BatchReviewResult,
    summary="Batch review",
    description="Review multiple submissions at once (admin only).",
)
async def batch_review(
    data: BatchReviewAction,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BatchReviewResult:
    """Review multiple submissions in batch."""
    # SECURITY: Enforce admin authorization
    if not getattr(user, 'is_admin', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    service = get_submission_service(db)
    processed = 0
    failed = 0
    errors = []
    
    for submission_id in data.submission_ids:
        try:
            result = await service.review_submission(
                submission_id, 
                user.id, 
                SubmissionUpdate(
                    status=data.status,
                    reviewer_notes=data.reviewer_notes,
                )
            )
            if result:
                processed += 1
            else:
                failed += 1
                errors.append(f"Submission {submission_id} not found")
        except Exception as e:
            failed += 1
            errors.append(f"Submission {submission_id}: {str(e)}")
    
    return BatchReviewResult(
        processed=processed,
        failed=failed,
        errors=errors,
    )


# Comments endpoints

@router.get(
    "/submissions/{submission_id}/comments",
    response_model=SubmissionCommentList,
    summary="Get comments",
    description="Get comments for a submission.",
)
async def get_comments(
    submission_id: str,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    file_path: str | None = None,
) -> SubmissionCommentList:
    """Get comments for a submission."""
    service = get_submission_service(db)
    
    # Verify submission exists and user has access
    submission = await service.get_submission(submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found",
        )
    
    comments = await service.get_comments(submission_id, file_path)
    
    comment_items = []
    for c in comments:
        comment_items.append(SubmissionComment(
            id=c.id,
            submission_id=c.submission_id,
            user_id=c.user_id,
            user_name=c.user.display_name if c.user else None,
            file_path=c.file_path,
            line_number=c.line_number,
            content=c.content,
            created_at=c.created_at,
            updated_at=c.updated_at,
            is_resolved=c.is_resolved,
        ))
    
    return SubmissionCommentList(
        items=comment_items,
        total=len(comment_items),
    )


@router.post(
    "/submissions/{submission_id}/comments",
    response_model=SubmissionComment,
    summary="Add comment",
    description="Add a comment to a submission.",
)
async def add_comment(
    submission_id: str,
    data: SubmissionCommentCreate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SubmissionComment:
    """Add a comment to a submission."""
    service = get_submission_service(db)
    
    # Verify submission exists and user has access
    submission = await service.get_submission(submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found",
        )
    
    comment = await service.add_comment(
        submission_id=submission_id,
        user_id=user.id,
        file_path=data.file_path,
        line_number=data.line_number,
        content=data.content,
    )
    
    return SubmissionComment(
        id=comment.id,
        submission_id=comment.submission_id,
        user_id=comment.user_id,
        user_name=user.display_name or user.email,
        file_path=comment.file_path,
        line_number=comment.line_number,
        content=comment.content,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        is_resolved=comment.is_resolved,
    )


# Gamification endpoints

@router.get(
    "/submissions/gamification/stats",
    response_model=GamificationStats,
    summary="Get gamification stats",
    description="Get gamification stats and achievements.",
)
async def get_gamification_stats(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> GamificationStats:
    """Get gamification stats for the current user."""
    service = get_submission_service(db)
    return await service.get_gamification_stats(user.id)

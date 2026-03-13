"""Draft service for managing saved code drafts."""

import logging

from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.draft import Draft

logger = logging.getLogger(__name__)


class DraftService:
    """Service for managing user code drafts."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_draft(self, user_id: str, problem_slug: str) -> Draft | None:
        """Get draft for a specific problem."""
        stmt = select(Draft).where(
            and_(
                Draft.user_id == user_id,
                Draft.problem_slug == problem_slug,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def save_draft(
        self,
        user_id: str,
        problem_slug: str,
        code: str,
        is_auto_save: bool = False,
    ) -> Draft:
        """Save or update a draft."""
        draft = await self.get_draft(user_id, problem_slug)

        if draft:
            # Update existing draft
            draft.code = code
            draft.is_auto_save = is_auto_save
        else:
            # Create new draft
            draft = Draft(
                user_id=user_id,
                problem_slug=problem_slug,
                code=code,
                is_auto_save=is_auto_save,
            )
            self.session.add(draft)

        await self.session.commit()
        await self.session.refresh(draft)
        logger.debug(f"Saved draft for user={user_id} problem={problem_slug}")
        return draft

    async def delete_draft(self, user_id: str, problem_slug: str) -> bool:
        """Delete a draft. Returns True if deleted, False if not found."""
        draft = await self.get_draft(user_id, problem_slug)
        if not draft:
            return False

        await self.session.delete(draft)
        await self.session.commit()
        logger.debug(f"Deleted draft for user={user_id} problem={problem_slug}")
        return True

    async def list_drafts(
        self,
        user_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Draft]:
        """List all drafts for a user, ordered by most recently saved."""
        stmt = (
            select(Draft)
            .where(Draft.user_id == user_id)
            .order_by(desc(Draft.saved_at))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete_all_drafts(self, user_id: str) -> int:
        """Delete all drafts for a user. Returns count of deleted drafts."""
        drafts = await self.list_drafts(user_id, limit=10000)
        count = len(drafts)
        
        for draft in drafts:
            await self.session.delete(draft)
        
        if count > 0:
            await self.session.commit()
            logger.info(f"Deleted {count} drafts for user={user_id}")
        
        return count


def get_draft_service(session: AsyncSession) -> DraftService:
    """Factory function for DraftService."""
    return DraftService(session)

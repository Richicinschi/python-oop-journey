"""Bookmark service for managing user bookmarks."""

import logging

from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.bookmark import Bookmark, ItemType

logger = logging.getLogger(__name__)


class BookmarkService:
    """Service for managing user bookmarks."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_bookmark(
        self, user_id: str, item_type: ItemType, item_slug: str
    ) -> Bookmark | None:
        """Get a specific bookmark."""
        stmt = select(Bookmark).where(
            and_(
                Bookmark.user_id == user_id,
                Bookmark.item_type == item_type,
                Bookmark.item_slug == item_slug,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_bookmark_by_id(self, user_id: str, bookmark_id: str) -> Bookmark | None:
        """Get a bookmark by its ID."""
        stmt = select(Bookmark).where(
            and_(
                Bookmark.user_id == user_id,
                Bookmark.id == bookmark_id,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_bookmark(
        self,
        user_id: str,
        item_type: ItemType,
        item_slug: str,
        notes: str | None = None,
    ) -> Bookmark:
        """Create a new bookmark."""
        # Check if already bookmarked
        existing = await self.get_bookmark(user_id, item_type, item_slug)
        if existing:
            # Update notes if provided
            if notes is not None:
                existing.notes = notes
                await self.session.commit()
                await self.session.refresh(existing)
            return existing

        # Create new bookmark
        bookmark = Bookmark(
            user_id=user_id,
            item_type=item_type,
            item_slug=item_slug,
            notes=notes,
        )
        self.session.add(bookmark)
        await self.session.commit()
        await self.session.refresh(bookmark)
        logger.debug(f"Created bookmark: {item_type}={item_slug} for user={user_id}")
        return bookmark

    async def delete_bookmark(
        self, user_id: str, item_type: ItemType, item_slug: str
    ) -> bool:
        """Delete a bookmark by type and slug. Returns True if deleted."""
        bookmark = await self.get_bookmark(user_id, item_type, item_slug)
        if not bookmark:
            return False

        await self.session.delete(bookmark)
        await self.session.commit()
        logger.debug(f"Deleted bookmark: {item_type}={item_slug} for user={user_id}")
        return True

    async def delete_bookmark_by_id(self, user_id: str, bookmark_id: str) -> bool:
        """Delete a bookmark by its ID. Returns True if deleted."""
        bookmark = await self.get_bookmark_by_id(user_id, bookmark_id)
        if not bookmark:
            return False

        await self.session.delete(bookmark)
        await self.session.commit()
        logger.debug(f"Deleted bookmark id={bookmark_id} for user={user_id}")
        return True

    async def list_bookmarks(
        self,
        user_id: str,
        item_type: ItemType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Bookmark]:
        """List bookmarks for a user, optionally filtered by type."""
        stmt = select(Bookmark).where(Bookmark.user_id == user_id)

        if item_type:
            stmt = stmt.where(Bookmark.item_type == item_type)

        stmt = stmt.order_by(desc(Bookmark.created_at)).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def is_bookmarked(
        self, user_id: str, item_type: ItemType, item_slug: str
    ) -> bool:
        """Check if an item is bookmarked."""
        bookmark = await self.get_bookmark(user_id, item_type, item_slug)
        return bookmark is not None

    async def update_bookmark_notes(
        self, user_id: str, bookmark_id: str, notes: str | None
    ) -> Bookmark | None:
        """Update notes for a bookmark."""
        bookmark = await self.get_bookmark_by_id(user_id, bookmark_id)
        if not bookmark:
            return None

        bookmark.notes = notes
        await self.session.commit()
        await self.session.refresh(bookmark)
        return bookmark

    async def toggle_bookmark(
        self,
        user_id: str,
        item_type: ItemType,
        item_slug: str,
        notes: str | None = None,
    ) -> tuple[bool, Bookmark | None]:
        """Toggle a bookmark. Returns (is_now_bookmarked, bookmark_or_none)."""
        if await self.is_bookmarked(user_id, item_type, item_slug):
            await self.delete_bookmark(user_id, item_type, item_slug)
            return False, None
        else:
            bookmark = await self.create_bookmark(user_id, item_type, item_slug, notes)
            return True, bookmark


def get_bookmark_service(session: AsyncSession) -> BookmarkService:
    """Factory function for BookmarkService."""
    return BookmarkService(session)

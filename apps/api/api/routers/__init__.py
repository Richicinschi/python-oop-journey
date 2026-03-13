"""API routers."""

from api.routers.activity import router as activity_router
from api.routers.auth import router as auth_router
from api.routers.bookmarks import router as bookmarks_router
from api.routers.curriculum import router as curriculum_router
from api.routers.drafts import router as drafts_router
from api.routers.execute import router as execute_router
from api.routers.health import router as health_router
from api.routers.progress import router as progress_router
from api.routers.projects import router as projects_router
from api.routers.submissions import router as submissions_router
from api.routers.sync import router as sync_router
from api.routers.user import router as user_router
from api.routers.verification import router as verification_router

__all__ = [
    "activity_router",
    "auth_router",
    "bookmarks_router",
    "curriculum_router",
    "drafts_router",
    "execute_router",
    "health_router",
    "progress_router",
    "projects_router",
    "submissions_router",
    "sync_router",
    "user_router",
    "verification_router",
]

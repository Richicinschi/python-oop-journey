"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from api.config import get_settings
from api.database import close_db, init_db
from api.routers import (
    activity_router,
    ai_router,
    auth_router,
    bookmarks_router,
    curriculum_router,
    drafts_router,
    execute_router,
    progress_router,
    projects_router,
    recommendations_router,
    submissions_router,
    sync_router,
    user_router,
    verification_router,
)
from api.websockets import ProgressWebSocket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting up %s", settings.app_name)
    logger.info("Environment: %s", settings.environment)

    # Initialize database (in production, use Alembic migrations instead)
    if settings.is_development:
        await init_db()
        logger.info("Database initialized")

    yield

    # Shutdown
    logger.info("Shutting down...")
    await close_db()


def create_app() -> FastAPI:
    """Application factory pattern."""
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Backend API for Python OOP Journey - Interactive coding curriculum",
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Gzip compression middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Include routers
    # Health checks (no prefix for load balancer compatibility)
    app.include_router(health_router, tags=["health"])
    
    # API v1 routes
    app.include_router(curriculum_router, prefix="/api/v1", tags=["curriculum"])
    app.include_router(execute_router, prefix="/api/v1", tags=["execution"])
    app.include_router(verification_router, prefix="/api/v1", tags=["verification"])
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(user_router, prefix="/api/v1", tags=["user"])
    
    # Progress and tracking routers
    app.include_router(progress_router, prefix="/api/v1", tags=["progress"])
    app.include_router(drafts_router, prefix="/api/v1", tags=["drafts"])
    app.include_router(bookmarks_router, prefix="/api/v1", tags=["bookmarks"])
    app.include_router(activity_router, prefix="/api/v1", tags=["activity"])
    
    # Project execution router for multi-file projects
    app.include_router(projects_router, prefix="/api/v1", tags=["projects"])
    
    # Submissions and review system
    app.include_router(submissions_router, prefix="/api/v1", tags=["submissions"])
    
    # Sync router for offline/online sync
    app.include_router(sync_router, prefix="/api/v1", tags=["sync"])
    
    # AI hints and assistance router
    app.include_router(ai_router, prefix="/api/v1", tags=["ai"])
    
    # Smart recommendations router
    app.include_router(recommendations_router, prefix="/api/v1", tags=["recommendations"])
    
    # WebSocket endpoint for real-time progress updates
    @app.websocket("/ws/progress")
    async def websocket_progress(websocket: WebSocket):
        """WebSocket endpoint for real-time progress updates."""
        # TODO: Replace with actual user authentication from token
        user_id = websocket.query_params.get("user_id", "anonymous")
        await ProgressWebSocket.handle(websocket, user_id)

    return app


# Create app instance
app = create_app()


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "environment": settings.environment,
        "timestamp": logging.time.time() if hasattr(logging, 'time') else None,
    }


@app.get("/ready", tags=["health"])
async def readiness_check():
    """Readiness probe - checks if app is ready to receive traffic."""
    # Check database connectivity
    try:
        from api.database import get_db
        async with get_db() as db:
            await db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
        return {
            "status": "not_ready",
            "database": db_status,
        }, 503
    
    return {
        "status": "ready",
        "database": db_status,
    }


@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API info."""
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "docs": "/docs" if settings.is_development else None,
        "health": "/health",
    }

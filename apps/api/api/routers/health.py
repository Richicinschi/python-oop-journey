"""Health check endpoints for monitoring and load balancers."""

import logging
import time
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db, engine
from api.middleware.cache import cache_manager
from api.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["health"])
settings = get_settings()


class HealthStatus(BaseModel):
    """Health check response model."""

    status: str
    version: str
    timestamp: str
    uptime_seconds: float
    environment: str


class HealthCheckDetailed(BaseModel):
    """Detailed health check response."""

    status: str
    version: str
    timestamp: str
    uptime_seconds: float
    environment: str
    checks: dict


# Track server start time
START_TIME = time.time()


@router.get("", response_model=HealthStatus)
async def health_check():
    """Basic health check endpoint.

    Returns overall system health status. Used by load balancers
    and monitoring systems for basic health checks.
    """
    uptime = time.time() - START_TIME

    return HealthStatus(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.utcnow().isoformat(),
        uptime_seconds=uptime,
        environment=settings.environment,
    )


@router.get("/detailed", response_model=HealthCheckDetailed)
async def health_check_detailed(db: AsyncSession = Depends(get_db)):
    """Detailed health check with component status.

    Performs health checks on all critical components:
    - Database connectivity
    - Redis cache (if configured)
    - Memory usage
    """
    checks = {}
    overall_status = "healthy"
    uptime = time.time() - START_TIME

    # Check database
    try:
        start_time = time.time()
        await db.execute(text("SELECT 1"))
        db_latency = (time.time() - start_time) * 1000

        checks["database"] = {
            "status": "healthy",
            "latency_ms": round(db_latency, 2),
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        checks["database"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        overall_status = "unhealthy"

    # Check Redis cache
    try:
        cache_stats = await cache_manager.get_stats()
        if cache_stats.get("enabled"):
            checks["cache"] = {
                "status": "healthy",
                "type": "redis",
                "details": cache_stats,
            }
        else:
            checks["cache"] = {
                "status": "degraded",
                "type": "none",
                "message": "Redis cache not available",
            }
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        checks["cache"] = {
            "status": "unhealthy",
            "error": str(e),
        }

    # Memory usage check
    try:
        import psutil

        memory = psutil.virtual_memory()
        checks["memory"] = {
            "status": "healthy" if memory.percent < 90 else "warning",
            "usage_percent": memory.percent,
            "available_mb": memory.available // (1024 * 1024),
            "total_mb": memory.total // (1024 * 1024),
        }

        if memory.percent >= 95:
            overall_status = "unhealthy"
        elif memory.percent >= 90:
            if overall_status == "healthy":
                overall_status = "degraded"
    except ImportError:
        checks["memory"] = {
            "status": "unknown",
            "message": "psutil not installed",
        }
    except Exception as e:
        logger.error(f"Memory health check failed: {e}")
        checks["memory"] = {
            "status": "unhealthy",
            "error": str(e),
        }

    # Disk space check
    try:
        import psutil

        disk = psutil.disk_usage("/")
        checks["disk"] = {
            "status": "healthy" if disk.percent < 90 else "warning",
            "usage_percent": disk.percent,
            "free_gb": disk.free // (1024 * 1024 * 1024),
            "total_gb": disk.total // (1024 * 1024 * 1024),
        }

        if disk.percent >= 95:
            overall_status = "unhealthy"
        elif disk.percent >= 90 and overall_status == "healthy":
            overall_status = "degraded"
    except Exception as e:
        logger.error(f"Disk health check failed: {e}")
        checks["disk"] = {
            "status": "unknown",
            "message": str(e),
        }

    # CPU usage check
    try:
        import psutil

        cpu_percent = psutil.cpu_percent(interval=0.1)
        checks["cpu"] = {
            "status": "healthy" if cpu_percent < 90 else "warning",
            "usage_percent": cpu_percent,
        }

        if cpu_percent >= 95:
            overall_status = "unhealthy"
        elif cpu_percent >= 90 and overall_status == "healthy":
            overall_status = "degraded"
    except Exception as e:
        logger.error(f"CPU health check failed: {e}")
        checks["cpu"] = {
            "status": "unknown",
            "message": str(e),
        }

    response_model = HealthCheckDetailed(
        status=overall_status,
        version="0.1.0",
        timestamp=datetime.utcnow().isoformat(),
        uptime_seconds=uptime,
        environment=settings.environment,
        checks=checks,
    )

    # Return appropriate status code
    if overall_status == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=response_model.dict(),
        )

    return response_model


@router.get("/db")
async def health_check_db(db: AsyncSession = Depends(get_db)):
    """Database-specific health check."""
    try:
        start_time = time.time()
        result = await db.execute(text("SELECT 1 as health"))
        row = result.scalar()
        latency = (time.time() - start_time) * 1000

        if row == 1:
            return {
                "status": "healthy",
                "database": "connected",
                "latency_ms": round(latency, 2),
                "timestamp": datetime.utcnow().isoformat(),
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "status": "unhealthy",
                    "database": "unexpected_response",
                    "timestamp": datetime.utcnow().isoformat(),
                },
            )
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            },
        )


@router.get("/cache")
async def health_check_cache():
    """Cache-specific health check."""
    try:
        stats = await cache_manager.get_stats()

        if stats.get("enabled"):
            return {
                "status": "healthy",
                "cache": "connected",
                "type": "redis",
                "stats": stats,
                "timestamp": datetime.utcnow().isoformat(),
            }
        else:
            return {
                "status": "degraded",
                "cache": "disabled",
                "message": "Redis cache not available, using fallback",
                "timestamp": datetime.utcnow().isoformat(),
            }
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        return {
            "status": "unhealthy",
            "cache": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """Kubernetes-style readiness probe.

    Returns 200 when the service is ready to accept traffic.
    """
    try:
        # Check database
        await db.execute(text("SELECT 1"))

        return {
            "ready": True,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "ready": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            },
        )


@router.get("/live")
async def liveness_check():
    """Kubernetes-style liveness probe.

    Returns 200 if the service is running (doesn't check dependencies).
    """
    return {
        "alive": True,
        "timestamp": datetime.utcnow().isoformat(),
    }

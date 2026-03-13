"""Caching middleware for API responses using Redis."""

import hashlib
import json
import logging
from functools import wraps
from typing import Any, Callable, Optional

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from api.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Cache TTL configurations (in seconds)
CACHE_TTLS = {
    "curriculum": 3600,  # 1 hour - curriculum rarely changes
    "user_progress": 300,  # 5 minutes - user progress changes frequently
    "submissions": 60,  # 1 minute - submissions can change
    "bookmarks": 300,  # 5 minutes
    "activity": 60,  # 1 minute - activity is frequent
    "drafts": 60,  # 1 minute - drafts change often
    "verification": 3600,  # 1 hour - verification results are stable
    "health": 10,  # 10 seconds - health checks should be fresh
}


class CacheManager:
    """Redis-based cache manager."""

    def __init__(self):
        self._redis = None
        self._enabled = False

    async def _get_redis(self):
        """Lazy initialization of Redis connection."""
        if self._redis is None and not self._enabled:
            try:
                import redis.asyncio as aioredis

                self._redis = aioredis.from_url(
                    settings.redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_read_timeout=5,
                    health_check_interval=30,
                )
                self._enabled = True
                logger.info("Redis cache initialized")
            except Exception as e:
                logger.warning(f"Redis cache not available: {e}")
                self._enabled = False
        return self._redis

    def _generate_key(self, prefix: str, identifier: str) -> str:
        """Generate cache key with prefix."""
        return f"oop_journey:{prefix}:{identifier}"

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self._enabled:
            return None

        try:
            redis = await self._get_redis()
            if redis:
                value = await redis.get(key)
                if value:
                    return json.loads(value)
        except Exception as e:
            logger.debug(f"Cache get error: {e}")

        return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 300,
        tags: Optional[list] = None,
    ) -> bool:
        """Set value in cache with TTL."""
        if not self._enabled:
            return False

        try:
            redis = await self._get_redis()
            if redis:
                serialized = json.dumps(value, default=str)
                await redis.setex(key, ttl, serialized)

                # Add to tag sets for cache invalidation
                if tags:
                    for tag in tags:
                        tag_key = f"tag:{tag}"
                        await redis.sadd(tag_key, key)

                return True
        except Exception as e:
            logger.debug(f"Cache set error: {e}")

        return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if not self._enabled:
            return False

        try:
            redis = await self._get_redis()
            if redis:
                await redis.delete(key)
                return True
        except Exception as e:
            logger.debug(f"Cache delete error: {e}")

        return False

    async def invalidate_by_tag(self, tag: str) -> int:
        """Invalidate all cache entries with a given tag."""
        if not self._enabled:
            return 0

        try:
            redis = await self._get_redis()
            if redis:
                tag_key = f"tag:{tag}"
                keys = await redis.smembers(tag_key)
                if keys:
                    await redis.delete(*keys, tag_key)
                    return len(keys)
        except Exception as e:
            logger.debug(f"Cache invalidation error: {e}")

        return 0

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate cache entries matching a pattern."""
        if not self._enabled:
            return 0

        try:
            redis = await self._get_redis()
            if redis:
                keys = []
                async for key in redis.scan_iter(match=pattern):
                    keys.append(key)
                if keys:
                    await redis.delete(*keys)
                    return len(keys)
        except Exception as e:
            logger.debug(f"Cache pattern invalidation error: {e}")

        return 0

    async def clear(self) -> bool:
        """Clear all cache."""
        if not self._enabled:
            return False

        try:
            redis = await self._get_redis()
            if redis:
                await redis.flushdb()
                return True
        except Exception as e:
            logger.debug(f"Cache clear error: {e}")

        return False

    async def get_stats(self) -> dict:
        """Get cache statistics."""
        if not self._enabled:
            return {"enabled": False}

        try:
            redis = await self._get_redis()
            if redis:
                info = await redis.info()
                return {
                    "enabled": True,
                    "used_memory": info.get("used_memory_human", "N/A"),
                    "connected_clients": info.get("connected_clients", 0),
                    "total_keys": await redis.dbsize(),
                }
        except Exception as e:
            logger.debug(f"Cache stats error: {e}")

        return {"enabled": False, "error": str(e)}


# Global cache manager instance
cache_manager = CacheManager()


def generate_request_key(request: Request, user_id: Optional[str] = None) -> str:
    """Generate cache key from request."""
    # Create a unique key based on URL and query parameters
    url = str(request.url)
    method = request.method

    # Include user ID in key if provided (for user-specific caching)
    key_data = f"{method}:{url}"
    if user_id:
        key_data = f"{user_id}:{key_data}"

    return hashlib.md5(key_data.encode()).hexdigest()


def cached(
    prefix: str,
    ttl: Optional[int] = None,
    user_specific: bool = False,
    tags: Optional[list] = None,
):
    """Decorator to cache API responses.

    Args:
        prefix: Cache key prefix
        ttl: Time to live in seconds (uses default if not specified)
        user_specific: Whether to include user ID in cache key
        tags: Tags for cache invalidation
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request from args
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            if request is None:
                # No request object, skip caching
                return await func(*args, **kwargs)

            # Only cache GET requests
            if request.method != "GET":
                return await func(*args, **kwargs)

            # Get user ID if user-specific caching
            user_id = None
            if user_specific:
                # Extract user ID from request state (set by auth middleware)
                user_id = getattr(request.state, "user_id", None)

            # Generate cache key
            cache_key = generate_request_key(request, user_id)
            full_key = cache_manager._generate_key(prefix, cache_key)

            # Try to get from cache
            cached_value = await cache_manager.get(full_key)
            if cached_value is not None:
                logger.debug(f"Cache hit: {full_key}")
                return JSONResponse(content=cached_value)

            # Call the function
            response = await func(*args, **kwargs)

            # Cache the response if it's a successful JSON response
            if isinstance(response, JSONResponse):
                try:
                    content = json.loads(response.body.decode())
                    cache_ttl = ttl or CACHE_TTLS.get(prefix, 300)
                    cache_tags = tags or [prefix]
                    await cache_manager.set(
                        full_key, content, ttl=cache_ttl, tags=cache_tags
                    )
                    logger.debug(f"Cached: {full_key}")
                except Exception as e:
                    logger.debug(f"Error caching response: {e}")

            return response

        return wrapper

    return decorator


async def invalidate_user_cache(user_id: str) -> int:
    """Invalidate all cache entries for a user."""
    pattern = cache_manager._generate_key("*", f"{user_id}:*")
    return await cache_manager.invalidate_pattern(pattern)


async def invalidate_curriculum_cache() -> int:
    """Invalidate all curriculum cache entries."""
    return await cache_manager.invalidate_by_tag("curriculum")


async def invalidate_progress_cache(user_id: str) -> int:
    """Invalidate progress cache for a user."""
    pattern = cache_manager._generate_key("user_progress", f"{user_id}:*")
    return await cache_manager.invalidate_pattern(pattern)


# Response cache middleware
async def cache_middleware(request: Request, call_next):
    """Middleware to add cache headers to responses."""
    response = await call_next(request)

    # Add cache headers based on route
    path = request.url.path

    if path.startswith("/api/v1/curriculum"):
        # Cache curriculum data
        response.headers["Cache-Control"] = "public, max-age=3600, s-maxage=3600"
        response.headers["CDN-Cache-Control"] = "max-age=3600"
    elif path.startswith("/api/v1/progress"):
        # Progress data - short cache with validation
        response.headers["Cache-Control"] = "private, no-cache"
    elif path.startswith("/api/v1/health"):
        # Health checks - no cache
        response.headers["Cache-Control"] = "no-store"
    else:
        # Default API cache policy
        response.headers["Cache-Control"] = "private, max-age=60"

    return response

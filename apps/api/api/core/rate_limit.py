"""Simple in-memory rate limiting with sliding window.

This module provides a reliable DIY rate limiter as a fallback/replacement
for slowapi when it fails to work correctly.
"""

import logging
import time
from collections import defaultdict
from functools import wraps
from typing import Callable, Optional

from fastapi import HTTPException, Request, status

logger = logging.getLogger(__name__)

# In-memory storage: {ip_address: [(timestamp1), (timestamp2), ...]}
_request_counts: defaultdict[str, list[float]] = defaultdict(list)

# Cleanup tracking to prevent memory leaks
_last_cleanup: float = time.time()
_CLEANUP_INTERVAL = 300  # Cleanup every 5 minutes


def _cleanup_old_entries(window_seconds: float = 60):
    """Remove entries older than the window to prevent memory leaks."""
    global _last_cleanup
    now = time.time()
    
    if now - _last_cleanup < _CLEANUP_INTERVAL:
        return
    
    cutoff = now - window_seconds
    ips_to_remove = []
    
    for ip, timestamps in _request_counts.items():
        # Keep only timestamps within the window
        _request_counts[ip] = [ts for ts in timestamps if ts > cutoff]
        if not _request_counts[ip]:
            ips_to_remove.append(ip)
    
    # Remove empty entries
    for ip in ips_to_remove:
        del _request_counts[ip]
    
    _last_cleanup = now
    if ips_to_remove:
        logger.debug(f"Rate limit cleanup: removed {len(ips_to_remove)} empty IP entries")


def check_rate_limit(ip: str, limit: int, window_seconds: float = 60) -> tuple[bool, int, float]:
    """Check if request is within rate limit.
    
    Args:
        ip: Client IP address
        limit: Maximum number of requests allowed
        window_seconds: Time window in seconds
        
    Returns:
        Tuple of (allowed, remaining_requests, retry_after_seconds)
    """
    now = time.time()
    cutoff = now - window_seconds
    
    # Get timestamps for this IP, filtering out old ones
    timestamps = _request_counts.get(ip, [])
    recent_timestamps = [ts for ts in timestamps if ts > cutoff]
    
    # Check if limit exceeded
    if len(recent_timestamps) >= limit:
        # Calculate retry after (time until oldest request expires)
        oldest_request = min(recent_timestamps)
        retry_after = window_seconds - (now - oldest_request)
        return False, 0, max(1, int(retry_after))
    
    # Request is allowed
    return True, limit - len(recent_timestamps) - 1, 0


def record_request(ip: str):
    """Record a request timestamp for an IP."""
    now = time.time()
    _request_counts[ip].append(now)
    
    # Periodic cleanup
    _cleanup_old_entries()


def get_client_ip(request: Request) -> str:
    """Extract client IP from request, handling proxies."""
    # Check for forwarded IP (if behind proxy/load balancer)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # X-Forwarded-For can be a comma-separated list
        return forwarded.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fall back to direct client IP
    if request.client:
        return request.client.host
    
    return "unknown"


def rate_limit(
    requests: int = 30,
    window_seconds: float = 60,
    key_func: Optional[Callable[[Request], str]] = None,
):
    """Rate limiting decorator for FastAPI endpoints.
    
    Args:
        requests: Maximum number of requests allowed in the window
        window_seconds: Time window in seconds
        key_func: Optional function to extract rate limit key from request.
                 Defaults to client IP address.
    
    Example:
        @router.post("/execute/run")
        @rate_limit(requests=30, window_seconds=60)
        async def execute_code(request: Request, ...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Find Request object in args or kwargs
            request: Optional[Request] = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request is None:
                request = kwargs.get('request')
            
            if request is None:
                logger.warning("Rate limit decorator: No Request object found")
                # Allow request through if we can't find the request object
                return await func(*args, **kwargs)
            
            # Get the key (IP or custom)
            if key_func:
                key = key_func(request)
            else:
                key = get_client_ip(request)
            
            # Check rate limit
            allowed, remaining, retry_after = check_rate_limit(key, requests, window_seconds)
            
            if not allowed:
                logger.warning(f"Rate limit exceeded for IP: {key}")
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": f"Too many requests. Limit: {requests} per {int(window_seconds)}s. Please slow down.",
                        "retry_after": retry_after,
                    },
                )
            
            # Record this request
            record_request(key)
            
            return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Find Request object in args or kwargs
            request: Optional[Request] = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request is None:
                request = kwargs.get('request')
            
            if request is None:
                logger.warning("Rate limit decorator: No Request object found")
                return func(*args, **kwargs)
            
            # Get the key (IP or custom)
            if key_func:
                key = key_func(request)
            else:
                key = get_client_ip(request)
            
            # Check rate limit
            allowed, remaining, retry_after = check_rate_limit(key, requests, window_seconds)
            
            if not allowed:
                logger.warning(f"Rate limit exceeded for IP: {key}")
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": f"Too many requests. Limit: {requests} per {int(window_seconds)}s. Please slow down.",
                        "retry_after": retry_after,
                    },
                )
            
            # Record this request
            record_request(key)
            
            return func(*args, **kwargs)
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


# Convenience functions for common limits
def rate_limit_per_minute(requests: int = 30):
    """Rate limit per minute."""
    return rate_limit(requests=requests, window_seconds=60)


def rate_limit_per_hour(requests: int = 100):
    """Rate limit per hour."""
    return rate_limit(requests=requests, window_seconds=3600)


# For testing/debugging
def reset_rate_limits():
    """Reset all rate limit counters (useful for testing)."""
    global _request_counts, _last_cleanup
    _request_counts.clear()
    _last_cleanup = time.time()
    logger.info("Rate limits reset")


def get_rate_limit_status(ip: Optional[str] = None) -> dict:
    """Get current rate limit status for debugging."""
    now = time.time()
    
    if ip:
        timestamps = _request_counts.get(ip, [])
        return {
            "ip": ip,
            "total_requests": len(timestamps),
            "recent_requests": len([ts for ts in timestamps if ts > now - 60]),
        }
    
    return {
        "total_ips_tracked": len(_request_counts),
        "ips": list(_request_counts.keys()),
    }

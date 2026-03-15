"""Python OOP Journey API - FastAPI Backend."""

from slowapi import Limiter
from slowapi.util import get_remote_address

__version__ = "0.1.0"

# Shared rate limiter instance for use across all routers
# Initialized here to avoid circular imports between main.py and routers
limiter = Limiter(key_func=get_remote_address)

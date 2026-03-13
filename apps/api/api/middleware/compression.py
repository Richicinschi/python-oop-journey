"""Response compression middleware for FastAPI."""

import gzip
import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class CompressionMiddleware(BaseHTTPMiddleware):
    """Middleware to compress responses using gzip or brotli."""

    def __init__(
        self,
        app,
        minimum_size: int = 500,  # Minimum response size to compress (bytes)
        compression_level: int = 6,  # Gzip compression level (1-9)
    ):
        super().__init__(app)
        self.minimum_size = minimum_size
        self.compression_level = compression_level
        self._brotli_available = self._check_brotli()

    def _check_brotli(self) -> bool:
        """Check if brotli compression is available."""
        try:
            import brotli

            return True
        except ImportError:
            return False

    def _should_compress(self, request: Request, response: Response) -> bool:
        """Determine if response should be compressed."""
        # Check if response is already encoded
        if response.headers.get("content-encoding"):
            return False

        # Check content type
        content_type = response.headers.get("content-type", "")
        compressible_types = (
            "text/",
            "application/json",
            "application/javascript",
            "application/xml",
            "application/rss+xml",
            "application/atom+xml",
            "image/svg+xml",
        )

        if not any(content_type.startswith(t) for t in compressible_types):
            return False

        # Check if client accepts compression
        accept_encoding = request.headers.get("accept-encoding", "")

        # Prefer brotli, fallback to gzip
        if self._brotli_available and "br" in accept_encoding:
            return True
        if "gzip" in accept_encoding:
            return True

        return False

    def _compress_gzip(self, body: bytes) -> bytes:
        """Compress body using gzip."""
        import gzip

        return gzip.compress(body, compresslevel=self.compression_level)

    def _compress_brotli(self, body: bytes) -> bytes:
        """Compress body using brotli."""
        import brotli

        return brotli.compress(body, quality=4)

    async def dispatch(self, request: Request, call_next: Callable):
        """Process request and compress response if applicable."""
        response = await call_next(request)

        # Check if compression should be applied
        if not self._should_compress(request, response):
            return response

        # Get response body
        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        # Only compress if body is large enough
        if len(body) < self.minimum_size:
            # Return uncompressed with content-length
            response.headers["content-length"] = str(len(body))
            return Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        # Determine compression method
        accept_encoding = request.headers.get("accept-encoding", "")

        if self._brotli_available and "br" in accept_encoding:
            compressed = self._compress_brotli(body)
            encoding = "br"
        else:
            compressed = self._compress_gzip(body)
            encoding = "gzip"

        # Don't compress if compressed size is larger
        if len(compressed) >= len(body):
            response.headers["content-length"] = str(len(body))
            return Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        # Return compressed response
        headers = dict(response.headers)
        headers["content-encoding"] = encoding
        headers["content-length"] = str(len(compressed))
        headers["vary"] = "accept-encoding"

        # Remove content-encoding from headers that shouldn't be there
        headers.pop("content-length", None)

        logger.debug(f"Compressed response: {len(body)} -> {len(compressed)} bytes ({encoding})")

        return Response(
            content=compressed,
            status_code=response.status_code,
            headers=headers,
            media_type=response.media_type,
        )


class BrotliResponder:
    """Streaming brotli response."""

    def __init__(self, app, minimum_size: int = 500):
        self.app = app
        self.minimum_size = minimum_size

    async def __call__(self, scope, receive, send):
        try:
            import brotli

            compressor = brotli.Compressor(quality=4)

            async def compressed_send(message):
                if message["type"] == "http.response.body":
                    body = message.get("body", b"")
                    if body:
                        compressed = compressor.process(body)
                        if compressed:
                            message["body"] = compressed

                    if not message.get("more_body", False):
                        # Finalize compression
                        final = compressor.finish()
                        if final:
                            message["body"] = message.get("body", b"") + final

                await send(message)

            await self.app(scope, receive, compressed_send)
        except ImportError:
            await self.app(scope, receive, send)

# =============================================================================
# API Dockerfile - Multi-stage build for FastAPI
# =============================================================================
# Targets: dependencies, development, production
# =============================================================================

ARG PYTHON_VERSION=3.11

# =============================================================================
# Stage 1: Dependencies
# =============================================================================
FROM python:${PYTHON_VERSION}-slim-bookworm AS dependencies

# Build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create virtual environment
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install Python dependencies
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# Stage 2: Development
# =============================================================================
FROM python:${PYTHON_VERSION}-slim-bookworm AS development

# System dependencies for development
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

WORKDIR /app

# Copy virtual environment from dependencies stage
COPY --from=dependencies /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy source code (will be overridden by volume mounts in compose)
COPY --chown=appuser:appuser apps/api ./apps/api
COPY --chown=appuser:appuser packages ./packages

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Default command for development (overridden in docker-compose)
CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# =============================================================================
# Stage 3: Production
# =============================================================================
FROM python:${PYTHON_VERSION}-slim-bookworm AS production

# Security: Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user with explicit UID/GID
RUN groupadd -r appuser --gid=1000 && \
    useradd -r -g appuser --uid=1000 --home-dir=/app appuser

WORKDIR /app

# Copy virtual environment
COPY --from=dependencies --chown=appuser:appuser /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=production

# Copy only necessary application files
COPY --chown=appuser:appuser apps/api ./apps/api
COPY --chown=appuser:appuser packages ./packages

# Remove any potential development/test files
RUN rm -rf ./apps/api/tests \
    ./apps/api/__pycache__ \
    ./apps/api/**/*.pyc \
    ./apps/api/.pytest_cache

# Set strict permissions
RUN chmod -R 550 /app/apps/api && \
    chmod -R 550 /app/packages

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Production command
CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--proxy-headers"]

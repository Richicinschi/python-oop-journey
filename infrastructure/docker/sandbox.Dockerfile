# =============================================================================
# Sandbox Dockerfile - Secure Python Execution Environment
# =============================================================================
# This container is used to run untrusted learner code with strict isolation.
#
# Security Features:
# - Non-root user execution
# - Read-only filesystem
# - No network access (network_mode: none at runtime)
# - Dropped capabilities
# - Memory and CPU limits
# - Process limits
# - Temporary filesystem isolation
#
# Resource Limits (enforced at runtime by Docker):
# - Memory: 256MB
# - CPU: 0.5 cores
# - PIDs: 50 processes max
# - Execution timeout: 30 seconds (enforced by runner)
# =============================================================================

FROM python:3.11-alpine

# Metadata
LABEL maintainer="OOP Journey Team" \
      description="Secure sandbox for executing learner Python code" \
      security.level="high"

# Create non-root user with explicit IDs
# Using a system user that cannot login
RUN addgroup -g 1000 -S learner && \
    adduser -u 1000 -S learner -G learner \
    --disabled-password \
    --no-create-home

# Install only essential packages
# - pytest: for running tests
# - pytest-timeout: to prevent infinite loops
# - RestrictedPython: for safe code execution (optional, for future use)
RUN pip install --no-cache-dir \
    pytest==8.0.0 \
    pytest-timeout==2.2.0 \
    && rm -rf /root/.cache/pip

# Create sandbox directory with strict permissions
# /sandbox - main working directory
# /sandbox/work - where learner code will be mounted
RUN mkdir -p /sandbox/work && \
    chown -R learner:learner /sandbox && \
    chmod 500 /sandbox && \
    chmod 700 /sandbox/work

# Set working directory
WORKDIR /sandbox/work

# Copy and set up runner script
COPY --chown=learner:learner infrastructure/docker/sandbox_runner.py /sandbox/runner.py
RUN chmod 400 /sandbox/runner.py

# Remove unnecessary tools that could be used maliciously
RUN apk del --no-cache \
    wget \
    curl \
    2>/dev/null || true

# Switch to non-root user
USER learner

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/sandbox/work
ENV HOME=/tmp

# Default command shows sandbox info
CMD ["python", "-c", "
import sys
print('='*50)
print('OOP Journey - Python Execution Sandbox')
print('='*50)
print(f'Python: {sys.version}')
print(f'Sandbox User: {__import__(\"os\").getuid()}')
print(f'Work Directory: {__import__(\"os\").getcwd()}')
print('Status: Ready for code execution')
print('='*50)
"]

# =============================================================================
# Usage Notes:
# =============================================================================
# This image is designed to be run with Docker security options:
#
# docker run --rm \
#   --read-only \
#   --network none \
#   --memory 256m \
#   --memory-swap 256m \
#   --cpus 0.5 \
#   --pids-limit 50 \
#   --security-opt no-new-privileges:true \
#   --cap-drop ALL \
#   --tmpfs /tmp:noexec,nosuid,size=100m \
#   -v /path/to/code:/sandbox/work:ro \
#   oopjourney-sandbox:latest \
#   python /sandbox/runner.py
#
# The API service spawns these containers dynamically using docker-py.
# =============================================================================

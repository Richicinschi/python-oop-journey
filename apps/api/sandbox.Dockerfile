# Secure Python Sandbox for Code Execution
# This Dockerfile creates a minimal, secure environment for running untrusted Python code

FROM python:3.11-slim-bookworm

# Install security updates and required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libseccomp2 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python testing tools
RUN pip install --no-cache-dir \
    pytest==8.3.2 \
    pytest-json-report==1.5.0 \
    unittest-xml-reporting==3.2.0

# Create non-root user for code execution
RUN groupadd -r sandbox && useradd -r -g sandbox -s /bin/false sandbox

# Create workspace directory with proper permissions
RUN mkdir -p /workspace /tmp/sandbox /project && \
    chown -R sandbox:sandbox /workspace /tmp/sandbox /project && \
    chmod 755 /workspace /tmp/sandbox /project

# Set resource limits via ulimit (will be enforced by Docker)
# Note: Actual limits are set at runtime via Docker run flags

# Switch to non-root user
USER sandbox

# Set working directory
WORKDIR /workspace

# Python environment variables for security
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HOME=/tmp/sandbox \
    TMPDIR=/tmp/sandbox \
    PYTHONPATH=/project:/project/src:/workspace

# Default command: execute Python code from mounted file
# The actual code file will be mounted at /workspace/code.py
ENTRYPOINT ["python", "-u"]
CMD ["/workspace/code.py"]

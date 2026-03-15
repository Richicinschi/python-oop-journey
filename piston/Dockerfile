# Piston Code Execution Engine
# Deploy this to Render as a Docker service

FROM ghcr.io/engineer-man/piston:latest

# Switch to root to set up the container
USER root

# Create isolate directories everywhere
RUN mkdir -p /tmp/isolate /var/cache/isolate /piston/runtimes/packages /piston/packages && \
    chmod -R 777 /tmp /var/cache /piston

# The API will be available on port 2000
EXPOSE 2000

# Set environment variables
ENV ISOLATE_ROOT=/tmp/isolate
ENV HOME=/tmp
ENV PISTON_COMPILE_TIMEOUT=60000
ENV PISTON_RUN_TIMEOUT=10000
ENV PISTON_OUTPUT_MAX_SIZE=10240
ENV PISTON_MAX_FILE_SIZE=65536
ENV PISTON_MAX_FILES=25

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:2000/api/v2/runtimes || exit 1

# Use shell form to change to /tmp before starting
SHELL ["/bin/sh", "-c"]
ENTRYPOINT cd /tmp && piston-api

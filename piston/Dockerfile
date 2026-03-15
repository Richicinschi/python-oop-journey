# Piston Code Execution Engine
# Deploy this to Render as a Docker service

FROM ghcr.io/engineer-man/piston:latest

# Stay as root (Render needs this for some operations)
USER root

# Create necessary directories with proper permissions
RUN mkdir -p /tmp/isolate /var/cache/isolate /piston/runtimes/packages /piston/packages && \
    chmod -R 777 /tmp /var/cache /piston

# Pre-create isolate directory structure
RUN cd /tmp && mkdir -p isolate

# Set environment variables
ENV ISOLATE_ROOT=/tmp/isolate
ENV HOME=/tmp
ENV PISTON_COMPILE_TIMEOUT=60000
ENV PISTON_RUN_TIMEOUT=10000
ENV PISTON_OUTPUT_MAX_SIZE=10240
ENV PISTON_MAX_FILE_SIZE=65536
ENV PISTON_MAX_FILES=25

# The API will be available on port 2000
EXPOSE 2000

# Override the startup to change to /tmp directory first
# Use shell form to allow cd command
WORKDIR /tmp
SHELL ["/bin/sh", "-c"]
CMD cd /tmp && piston-api

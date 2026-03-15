# Piston Code Execution Engine for Render
# Fix for read-only filesystem: use /tmp for isolate

FROM ghcr.io/engineer-man/piston:latest

# Fix for Render's read-only root filesystem
# isolate needs to write to a writable directory
WORKDIR /tmp
ENV ISOLATE_ROOT=/tmp/isolate

# Create isolate directory with proper permissions
RUN mkdir -p /tmp/isolate && chmod 777 /tmp/isolate

# Expose the Piston API port
EXPOSE 2000

# Don't override ENTRYPOINT or CMD - base image handles it

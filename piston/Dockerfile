# Piston Code Execution Engine
# Deploy this to Render as a Docker service

FROM ghcr.io/engineer-man/piston:latest

# Install Python 3.12 runtime
# Piston uses "ppman" (Piston Package Manager) to install runtimes
RUN mkdir -p /piston/runtimes

# The API will be available on port 2000
EXPOSE 2000

# Piston API configuration
ENV PISTON_COMPILE_TIMEOUT=60000
ENV PISTON_RUN_TIMEOUT=10000
ENV PISTON_OUTPUT_MAX_SIZE=10240
ENV PISTON_MAX_FILE_SIZE=65536
ENV PISTON_MAX_FILES=25

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:2000/api/v2/runtimes || exit 1

# Start Piston API
CMD ["piston-api"]

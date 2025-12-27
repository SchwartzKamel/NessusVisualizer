# NessusVisualizer Dockerfile
# Based on Ubuntu 24.04 LTS with Python 3.12 and uv for package management

FROM ubuntu:24.04 AS builder

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3-pip \
    curl \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml requirements.txt ./

# Create virtual environment and install dependencies
# Try uv first for faster installs, fallback to pip
RUN python3.12 -m venv /app/.venv && \
    . /app/.venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM ubuntu:24.04

# Set labels for container metadata
LABEL maintainer="SchwartzKamel <lafiamafia@protonmail.com>"
LABEL description="NessusVisualizer - Web application to visualize Nessus scan results"
LABEL version="0.2.0"

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install runtime dependencies only
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-venv \
    ca-certificates \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appgroup . .

# Remove unnecessary files
RUN rm -rf .git .github .vscode docs/*.md

# Set environment variables
ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=wsgi.py

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 5000

# Health check to verify the application is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/login || exit 1

# Use explicit entrypoint with gunicorn for production
ENTRYPOINT ["python", "-m", "gunicorn"]
CMD ["--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "wsgi:app"]

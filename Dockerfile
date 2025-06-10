# Chandigarh Policy Assistant - Optimized for Railway Deployment
# Multi-stage build to reduce final image size from 6.5GB to ~3.5GB

# ================================
# Stage 1: Builder (temporary stage)
# ================================
FROM python:3.11-slim as builder

# Install build dependencies (will be discarded)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for build
WORKDIR /app

# Copy requirements and install with cache
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies with optimizations
RUN pip install --upgrade pip && \
    pip uninstall -y pinecone-client || true && \
    pip install --no-cache-dir -r requirements.txt

# Download NLTK data (minimal required datasets only)
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')" --quiet

# ================================
# Stage 2: Production (final stage)
# ================================
FROM python:3.11-slim

# Install only runtime dependencies (no build tools)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create application user for security
RUN useradd -m -u 1000 railwayuser

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application files with proper ownership
COPY --chown=railwayuser:railwayuser . /app

# Create cache directories with proper permissions
RUN mkdir -p cache /tmp/cache && \
    chown -R railwayuser:railwayuser cache /tmp/cache && \
    chmod 755 cache && \
    chmod 777 /tmp/cache

# Fix permissions for existing cache files
RUN find cache -type f -exec chmod 644 {} \; 2>/dev/null || true

# Switch to non-root user
USER railwayuser

# Railway-specific environment variables
ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Expose port for Railway (Railway uses PORT env variable)
EXPOSE $PORT

# Health check optimized for Railway
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Default command for Railway deployment
CMD ["python", "fast_hybrid_search_server.py"] 
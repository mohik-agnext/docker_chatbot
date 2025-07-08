# Chandigarh Policy Assistant - Render Deployment Optimized
# Ultra-lightweight build with Jina API-only dependencies

# ================================
# Stage 1: Builder (minimal dependencies)
# ================================
FROM python:3.11-slim as builder

# Install only essential build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app
COPY requirements.txt .

# Create optimized virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install lightweight dependencies and NLTK data
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt && \
    python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)" && \
    pip cache purge && \
    # Aggressive cleanup for API-only deployment
    find /opt/venv -name "*.pyc" -delete && \
    find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + || true && \
    find /opt/venv -type d -name "tests" -exec rm -rf {} + || true && \
    find /opt/venv -type d -name "examples" -exec rm -rf {} + || true && \
    find /opt/venv -name "*.pth-*" -delete || true

# ================================  
# Stage 2: Ultra-minimal runtime (API-only)
# ================================
FROM python:3.11-slim

# Install only curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/* /var/tmp/* \
    && apt-get clean && apt-get autoremove -y

# Create non-root user for Render
RUN useradd -m -u 1000 renderuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy only essential application files (API-optimized)
COPY --chown=renderuser:renderuser fast_hybrid_search_server.py .
COPY --chown=renderuser:renderuser performance_fix_hybrid_search.py .
COPY --chown=renderuser:renderuser semantic_namespace_mapper.py .
COPY --chown=renderuser:renderuser config.py .
COPY --chown=renderuser:renderuser hybrid_search_frontend.html .
COPY --chown=renderuser:renderuser index.html .
COPY --chown=renderuser:renderuser cache/ ./cache/

# Create minimal cache structure
RUN mkdir -p /tmp/cache && \
    chown -R renderuser:renderuser . /tmp/cache && \
    chmod -R 755 . && \
    chmod 777 /tmp/cache

USER renderuser

# Render environment variables (Jina v3 optimized)
ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=10000 \
    USE_JINA_API=true \
    JINA_MODEL=jina-embeddings-v3

EXPOSE $PORT

# Optimized health check for Render
HEALTHCHECK --interval=45s --timeout=15s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:$PORT/ready || exit 1

# Use gunicorn for production deployment (Render optimized)
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - fast_hybrid_search_server:app 
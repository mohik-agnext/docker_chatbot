# Chandigarh Policy Assistant - Ultra-Optimized for Railway (<4GB)
# Aggressive multi-stage build with minimal AI models

# ================================
# Stage 1: Builder (temporary stage)
# ================================
FROM python:3.11-slim as builder

# Install minimal build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app
COPY requirements.txt .

# Create optimized virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies with safe optimization
RUN pip install --upgrade pip --no-cache-dir && \
    pip uninstall -y pinecone-client || true && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge && \
    # Conservative cleanup - only remove obviously safe files
    find /opt/venv -name "*.pyc" -delete && \
    find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + || true && \
    find /opt/venv -type d -name "tests" -exec rm -rf {} + || true && \
    find /opt/venv -type d -name "examples" -exec rm -rf {} + || true

# Download only essential NLTK data
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

# ================================  
# Stage 2: Ultra-minimal runtime
# ================================
FROM python:3.11-slim

# Install only curl and clean aggressively
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /usr/share/doc/* \
    && rm -rf /usr/share/man/* \
    && rm -rf /var/cache/apt/* \
    && rm -rf /tmp/*

# Create user
RUN useradd -m -u 1000 railwayuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Final cleanup in runtime stage
RUN find /opt/venv -name "*.pyc" -delete && \
    find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + || true

WORKDIR /app

# Copy only essential application files
COPY --chown=railwayuser:railwayuser fast_hybrid_search_server.py .
COPY --chown=railwayuser:railwayuser performance_fix_hybrid_search.py .
COPY --chown=railwayuser:railwayuser semantic_namespace_mapper.py .
COPY --chown=railwayuser:railwayuser config.py .
COPY --chown=railwayuser:railwayuser hybrid_search_frontend.html .
COPY --chown=railwayuser:railwayuser index.html .
COPY --chown=railwayuser:railwayuser cache/ ./cache/
COPY --chown=railwayuser:railwayuser txt_files/ ./txt_files/

# Create cache directories
RUN mkdir -p /tmp/cache && \
    chown -R railwayuser:railwayuser . /tmp/cache && \
    chmod -R 755 . && \
    chmod 777 /tmp/cache

USER railwayuser

# Railway environment variables
ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    EMBEDDING_MODEL=all-MiniLM-L6-v2

EXPOSE $PORT

# Minimal health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=180s --retries=2 \
    CMD curl -f http://localhost:$PORT/health || exit 1

CMD ["python", "fast_hybrid_search_server.py"] 
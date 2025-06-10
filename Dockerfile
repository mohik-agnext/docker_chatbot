# Chandigarh Policy Assistant Dockerfile for HuggingFace Spaces
FROM python:3.11-slim

# Install system dependencies as root
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create user for HuggingFace Spaces compatibility
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR /app

# Switch to user and update PATH
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Copy requirements first for better caching
COPY --chown=user ./requirements.txt requirements.txt

# Explicitly uninstall old pinecone-client and install dependencies
RUN pip uninstall -y pinecone-client || true
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Copy application files
COPY --chown=user . /app

# Create cache directory with proper permissions
RUN mkdir -p cache && chmod 755 cache
RUN mkdir -p /tmp/cache && chmod 777 /tmp/cache

# Fix any permission issues with existing cache files
RUN find cache -type f -exec chmod 644 {} \; 2>/dev/null || true

# Expose port 7860 for HuggingFace Spaces
EXPOSE 7860

# Set environment variables for production
ENV FLASK_ENV=production
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Add health check for HuggingFace Spaces
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Default command - run the fast hybrid search server
CMD ["python", "fast_hybrid_search_server.py"] 
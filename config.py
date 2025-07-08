"""
Configuration file for API keys and settings.
Uses environment variables for security - set your API keys as environment variables.
Optimized for Jina API embeddings for fast deployment.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Pinecone settings
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "your_pinecone_api_key_here")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "cursor2")
PINECONE_DIMENSION = int(os.getenv("PINECONE_DIMENSION", "1024"))  # Updated for Jina embeddings
PINECONE_HOST = os.getenv("PINECONE_HOST", "cursor2-ikkf5bw.svc.aped-4627-b74a.pinecone.io")

# LLM Provider settings - Using Groq for optimal performance
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # Default: "groq"

# Groq settings (primary LLM provider)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# Jina AI settings (primary embedding provider for fast API-based embeddings)
JINA_API_KEY = os.getenv("JINA_API_KEY", "your_jina_api_key_here")
JINA_MODEL = os.getenv("JINA_MODEL", "jina-embeddings-v3")  # Latest Jina v3 model
DEFAULT_EMBEDDING_PROVIDER = os.getenv("DEFAULT_EMBEDDING_PROVIDER", "jina")

# Embedding configuration
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1024"))  # Jina v3 dimension
USE_JINA_API = os.getenv("USE_JINA_API", "true").lower() == "true"

# Hybrid search configuration
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "4"))
DEFAULT_ALPHA = float(os.getenv("DEFAULT_ALPHA", "0.5"))
DEFAULT_FUSION_METHOD = os.getenv("DEFAULT_FUSION_METHOD", "rrf")
RRF_K_VALUE = int(os.getenv("RRF_K_VALUE", "30"))

# Retrieval Parameters
TOP_K = int(os.getenv("TOP_K", "12"))
RECURSIVE_RETRIEVAL = os.getenv("RECURSIVE_RETRIEVAL", "True").lower() == "true"
RERANKING_ENABLED = os.getenv("RERANKING_ENABLED", "True").lower() == "true"

# Server configuration
PORT = int(os.getenv("PORT", "10000"))  # Render default port
FLASK_ENV = os.getenv("FLASK_ENV", "production")

# Performance optimizations
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "32"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "2")) 
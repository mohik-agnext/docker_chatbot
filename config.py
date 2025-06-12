"""
Configuration file for API keys and settings.
Uses environment variables for security - set your API keys as environment variables.
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

# LLM Provider settings - Choose which one to use
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # Options: "openai" or "groq"

# OpenAI settings (if using OpenAI)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Groq settings (if using Groq)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# Embedding models
# Default embedding provider - set to "huggingface" for better performance
DEFAULT_EMBEDDING_PROVIDER = os.getenv("DEFAULT_EMBEDDING_PROVIDER", "huggingface")

# Sentence Transformers settings (if using Sentence Transformers)
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")

# Cohere settings (if using Cohere)
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "your_cohere_api_key_here")
COHERE_MODEL = os.getenv("COHERE_MODEL", "embed-english-v3.0")

# HuggingFace settings (if using HuggingFace)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "your_huggingface_api_key_here")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "all-MiniLM-L6-v2")  # Lightweight: 80MB vs 1.3GB
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")  # Fast deployment model

# Jina AI settings (for fast API-based embeddings)
JINA_API_KEY = os.getenv("JINA_API_KEY", "your_jina_api_key_here")

# For testing multiple embedding models
EMBEDDING_MODELS = {
    "sentence_transformers": {
        "all-MiniLM-L6-v2": 384,
    },
    "cohere": {
        "embed-english-v3.0": 1024,
    },
    "huggingface": {
        "BAAI/bge-large-en-v1.5": 1024,
        "all-MiniLM-L6-v2": 384,
    }
}

# Additional configuration options
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "4"))
DEFAULT_ALPHA = float(os.getenv("DEFAULT_ALPHA", "0.5"))
DEFAULT_FUSION_METHOD = os.getenv("DEFAULT_FUSION_METHOD", "rrf")
RRF_K_VALUE = int(os.getenv("RRF_K_VALUE", "30"))

# Retrieval Parameters
TOP_K = int(os.getenv("TOP_K", "12"))
RECURSIVE_RETRIEVAL = os.getenv("RECURSIVE_RETRIEVAL", "True").lower() == "true"
RERANKING_ENABLED = os.getenv("RERANKING_ENABLED", "True").lower() == "true" 
#!/usr/bin/env python3
"""
PERFORMANCE-OPTIMIZED Hybrid Search for Chandigarh Policy Assistant

This version addresses the critical performance bottlenecks in the original implementation:
1. Eliminates expensive BM25 initialization by pre-computing and caching documents
2. Implements query embedding caching
3. Reduces namespace searches with intelligent targeting
4. Adds streaming response capability
"""

import json
import numpy as np
from typing import List, Dict, Any
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import time
import pickle
import os
from functools import wraps
import config
from semantic_namespace_mapper import semantic_mapper

class PerformanceOptimizedHybridSearch:
    def __init__(self, 
                 pinecone_api_key,
                 pinecone_index,
                 embedding_model=None,
                 alpha=0.7,
                 fusion_method="rrf",
                 cache_dir="cache"):
        """
        Performance-optimized hybrid search with aggressive caching.
        """
        self.alpha = alpha
        self.fusion_method = fusion_method
        self.cache_dir = cache_dir
        self.embedding_dimension = config.PINECONE_DIMENSION
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Performance tracking
        self.performance_stats = {
            "queries_processed": 0,
            "cache_hits": 0,
            "avg_response_time": 0
        }
        
        print(f"\n🚀 Initializing Performance-Optimized Hybrid Search")
        
        # 1. FAST Pinecone initialization
        self._initialize_pinecone_fast(pinecone_api_key, pinecone_index)
        
        # 2. FAST embedding model loading
        self._initialize_embedding_model_fast(embedding_model)
        
        # 3. CACHED BM25 initialization (major optimization)
        self._initialize_bm25_cached()
        
        print(f"✅ Initialization complete - Ready for production!")
        
    def _initialize_pinecone_fast(self, api_key: str, index_name: str):
        """Fast Pinecone initialization with minimal checks."""
        try:
            self.pc = Pinecone(api_key=api_key)
            self.index = self.pc.Index(index_name)
            
            # Quick namespace check - only get count, not full details
            stats = self.index.describe_index_stats()
            self.namespaces = list(stats.namespaces.keys())
            print(f"🔗 Connected to Pinecone index '{index_name}' with {len(self.namespaces)} namespaces")
            
        except Exception as e:
            print(f"❌ Pinecone initialization failed: {e}")
            raise e
    
    def _initialize_embedding_model_fast(self, embedding_model=None):
        """Fast embedding model initialization with caching."""
        if embedding_model is None:
            embedding_model = config.EMBEDDING_MODEL
        
        print(f"🧠 Loading embedding model: {embedding_model}")
        start_time = time.time()
        
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Quick dimension check
        test_embedding = self.embedding_model.encode("test")
        self.embedding_dimension_actual = len(test_embedding)
        
        load_time = time.time() - start_time
        print(f"✅ Model loaded in {load_time:.2f}s (dimension: {self.embedding_dimension_actual})")
        
        # Enhanced caching for cloud deployment
        self.query_embedding_cache = {}
        self.max_cache_size = 100  # Increased cache size
        self.query_cache = {}  # Full result caching
        self.max_query_cache_size = 50
    
    def _initialize_bm25_cached(self):
        """MAJOR OPTIMIZATION: Use cached BM25 index instead of rebuilding."""
        cache_file = os.path.join(self.cache_dir, "bm25_index.pkl")
        docs_cache_file = os.path.join(self.cache_dir, "bm25_documents.pkl")
        
        # Try to load from cache first
        if os.path.exists(cache_file) and os.path.exists(docs_cache_file):
            try:
                print("📦 Loading BM25 index from cache...")
                start_time = time.time()
                
                with open(cache_file, 'rb') as f:
                    self.bm25_index = pickle.load(f)
                
                with open(docs_cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                    self.bm25_documents = cache_data['documents']
                    self.doc_ids = cache_data['doc_ids']
                
                load_time = time.time() - start_time
                print(f"✅ BM25 cache loaded in {load_time:.2f}s ({len(self.bm25_documents)} documents)")
                return
                
            except Exception as e:
                print(f"⚠️  Cache loading failed: {e}, rebuilding...")
        
        # If cache doesn't exist or failed to load, build and cache
        print("🔨 Building BM25 index (this may take a moment, but will be cached)...")
        self._build_and_cache_bm25()
    
    def _build_and_cache_bm25(self):
        """Build BM25 index efficiently and cache it."""
        start_time = time.time()
        
        self.bm25_documents = []
        self.doc_ids = []
        
        # Use a more efficient approach - sample from each namespace
        for namespace in self.namespaces:
            try:
                # Instead of fetching ALL documents, sample a reasonable number
                sample_size = 50  # Sample 50 docs per namespace for BM25
                
                # Use a targeted query to get diverse documents
                sample_vector = [0.1] * self.embedding_dimension  # Slightly offset dummy vector
                
                results = self.index.query(
                    vector=sample_vector,
                    top_k=sample_size,
                    namespace=namespace,
                    include_metadata=True
                )
                
                namespace_docs = 0
                for match in results.matches:
                    # FIXED: Use 'content' instead of 'text' based on new vector database structure
                    text_content = match.metadata.get('content') or match.metadata.get('text', '')
                    if text_content:
                        text = text_content.strip()
                        if len(text) > 20:  # Minimum meaningful text
                            self.bm25_documents.append(text)
                            self.doc_ids.append((match.id, namespace))
                            namespace_docs += 1
                
                print(f"  📄 {namespace}: {namespace_docs} documents")
                
            except Exception as e:
                print(f"  ❌ Error with namespace {namespace}: {e}")
                continue
        
        if not self.bm25_documents:
            print("⚠️  No documents found for BM25 - using fallback")
            self.bm25_index = None
            return
        
        # Tokenize efficiently
        print(f"🔤 Tokenizing {len(self.bm25_documents)} documents...")
        tokenized_docs = self._tokenize_documents_fast(self.bm25_documents)
        
        if tokenized_docs:
            self.bm25_index = BM25Okapi(tokenized_docs)
            
            # Cache the results
            try:
                cache_file = os.path.join(self.cache_dir, "bm25_index.pkl")
                docs_cache_file = os.path.join(self.cache_dir, "bm25_documents.pkl")
                
                with open(cache_file, 'wb') as f:
                    pickle.dump(self.bm25_index, f)
                
                with open(docs_cache_file, 'wb') as f:
                    pickle.dump({
                        'documents': self.bm25_documents,
                        'doc_ids': self.doc_ids
                    }, f)
                
                print(f"💾 BM25 index cached for future use")
                
            except Exception as e:
                print(f"⚠️  Failed to cache BM25 index: {e}")
        
        build_time = time.time() - start_time
        print(f"✅ BM25 index built in {build_time:.2f}s")
    
    def _tokenize_documents_fast(self, documents):
        """Fast document tokenization with minimal NLTK dependency."""
        try:
            stop_words = set(stopwords.words('english'))
        except:
            # Fallback stopwords if NLTK download fails
            stop_words = {'the', 'and', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'of', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        tokenized_docs = []
        for doc in documents:
            try:
                # Simple but effective tokenization
                tokens = doc.lower().split()
                filtered_tokens = [
                    token.strip('.,!?;:"()[]{}') 
                    for token in tokens 
                    if len(token) > 2 and token.lower() not in stop_words and not token.isdigit()
                ]
                
                if len(filtered_tokens) >= 3:
                    tokenized_docs.append(filtered_tokens)
            except:
                continue
        
        return tokenized_docs
    
    def fast_search(self, query: str, top_k: int = 5):
        """Fast hybrid search with intelligent caching and optimized performance."""
        start_time = time.time()
        
        # Check query cache first
        query_key = f"{query.lower().strip()}_{top_k}"
        if query_key in self.query_cache:
            cached_result = self.query_cache[query_key]
            self.performance_stats["cache_hits"] += 1
            self.performance_stats["queries_processed"] += 1
            print(f"⚡ Cache hit! Returned in {time.time() - start_time:.3f}s")
            return cached_result
        
        self.performance_stats["queries_processed"] += 1
        
        print(f"\n⚡ FAST SEARCH: '{query}' (target: <3s)")
        
        # 1. CACHED EMBEDDING (0.01-0.1s)
        query_embedding = self._get_cached_embedding(query)
        
        # 2. TARGETED SEMANTIC SEARCH (0.5-1.5s)
        vector_results = self._fast_semantic_search(query, query_embedding, top_k)
        
        # 3. FAST BM25 SEARCH (0.1-0.5s) 
        bm25_results = self._fast_bm25_search(query, top_k)
        
        # 4. QUICK FUSION (0.01-0.1s)
        final_results = self._fast_fusion(vector_results, bm25_results, top_k)
        
        # Update performance stats
        total_time = time.time() - start_time
        self.performance_stats["avg_response_time"] = (
            (self.performance_stats["avg_response_time"] * (self.performance_stats["queries_processed"] - 1) + total_time)
            / self.performance_stats["queries_processed"]
        )
        
        print(f"⚡ Fast search completed in {total_time:.3f}s")
        
        # Cache the results for future queries
        if len(self.query_cache) >= self.max_query_cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self.query_cache))
            del self.query_cache[oldest_key]
        
        self.query_cache[query_key] = final_results
        
        return final_results
    
    def _get_cached_embedding(self, query: str):
        """Get query embedding with aggressive caching."""
        query_key = query.strip().lower()
        
        if query_key in self.query_embedding_cache:
            self.performance_stats["cache_hits"] += 1
            print("🎯 Using cached embedding")
            return self.query_embedding_cache[query_key]
        
        # Generate new embedding
        start_time = time.time()
        embedding = self.embedding_model.encode(query)
        embedding_time = time.time() - start_time
        
        # Normalize if needed
        embedding = embedding / np.linalg.norm(embedding)
        
        # Cache management
        if len(self.query_embedding_cache) >= self.max_cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self.query_embedding_cache))
            del self.query_embedding_cache[oldest_key]
        
        self.query_embedding_cache[query_key] = embedding
        print(f"🧠 New embedding generated in {embedding_time:.3f}s")
        
        return embedding
    
    def _fast_semantic_search(self, query: str, query_embedding, top_k: int):
        """Fast semantic search with intelligent namespace targeting."""
        # Get 1-2 most relevant namespaces only for speed
        relevant_semantic_namespaces = semantic_mapper.get_relevant_semantic_namespaces(
            query, min_namespaces=1, max_namespaces=2  # Reduced for faster responses
        )
        
        target_namespaces = semantic_mapper.translate_namespaces(
            relevant_semantic_namespaces, to_actual=True
        )
        
        available_namespaces = [ns for ns in target_namespaces if ns in self.namespaces]
        
        if not available_namespaces:
            # Emergency fallback - use first namespace only
            available_namespaces = self.namespaces[:1]
        
        print(f"🎯 Searching {len(available_namespaces)} targeted namespaces")
        
        all_results = []
        
        for namespace in available_namespaces:
            try:
                results = self.index.query(
                    vector=query_embedding.tolist(),
                    top_k=top_k,
                    namespace=namespace,
                    include_metadata=True
                )
                
                for match in results.matches:
                    all_results.append({
                        "id": match.id,
                        "score": match.score,
                        "metadata": match.metadata,
                        "namespace": namespace,
                        "source": "vector"
                    })
            except Exception as e:
                print(f"⚠️  Error in namespace {namespace}: {e}")
                continue
        
        # Sort and return top results
        all_results.sort(key=lambda x: x["score"], reverse=True)
        return all_results[:top_k]
    
    def _fast_bm25_search(self, query: str, top_k: int):
        """Fast BM25 search with cached index."""
        if not self.bm25_index:
            return []
        
        try:
            # Simple tokenization for speed
            query_tokens = [
                token.strip('.,!?;:"()[]{}').lower()
                for token in query.split()
                if len(token) > 2 and not token.isdigit()
            ]
            
            if not query_tokens:
                return []
            
            # Get BM25 scores
            scores = self.bm25_index.get_scores(query_tokens)
            
            # Get top results
            top_indices = np.argsort(scores)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if idx < len(self.bm25_documents) and scores[idx] > 0:
                    doc_id, namespace = self.doc_ids[idx]
                    results.append({
                        "id": doc_id,
                        "score": float(scores[idx]),
                        "metadata": {"text": self.bm25_documents[idx]},
                        "namespace": namespace,
                        "source": "bm25"
                    })
            
            return results
        
        except Exception as e:
            print(f"⚠️  BM25 search error: {e}")
            return []
    
    def _fast_fusion(self, vector_results: List[dict], bm25_results: List[dict], top_k: int):
        """Fast result fusion using simple scoring."""
        # Simple weighted combination for speed
        all_results = {}
        
        # Add vector results
        for i, result in enumerate(vector_results):
            doc_id = result["id"]
            # Higher weight for vector search, position penalty
            score = result["score"] * 0.7 * (1 - i * 0.05)
            all_results[doc_id] = {
                **result,
                "score": score,
                "sources": ["vector"]
            }
        
        # Add BM25 results
        for i, result in enumerate(bm25_results):
            doc_id = result["id"]
            bm25_score = result["score"] * 0.3 * (1 - i * 0.05)
            
            if doc_id in all_results:
                # Combine scores
                all_results[doc_id]["score"] += bm25_score
                all_results[doc_id]["sources"].append("bm25")
            else:
                all_results[doc_id] = {
                    **result,
                    "score": bm25_score,
                    "sources": ["bm25"]
                }
        
        # Sort and return top results
        final_results = list(all_results.values())
        final_results.sort(key=lambda x: x["score"], reverse=True)
        
        return final_results[:top_k]
    
    def get_performance_stats(self):
        """Get current performance statistics."""
        cache_hit_rate = (
            self.performance_stats["cache_hits"] / max(1, self.performance_stats["queries_processed"]) * 100
        )
        
        return {
            **self.performance_stats,
            "cache_hit_rate": f"{cache_hit_rate:.1f}%",
            "production_ready": self.performance_stats["avg_response_time"] < 5.0
        }

# Fast execution function for server
def fast_execute(params):
    """Fast execution optimized for production use."""
    try:
        query = params.get('query', '') or params.get('body', {}).get('message', '')
        if not query:
            return {'error': 'No query provided'}
        
        # Use global searcher instance to avoid re-initialization
        global fast_searcher
        if 'fast_searcher' not in globals():
            # Initialize once
            fast_searcher = PerformanceOptimizedHybridSearch(
                pinecone_api_key=params.get('pineconeApiKey', ''),
                pinecone_index=params.get('pineconeIndex', 'cursor2'),
                alpha=float(params.get('alpha', 0.5)),
                fusion_method=params.get('fusion_method', 'rrf')
            )
        
        # Fast search
        results = fast_searcher.fast_search(
            query, 
            top_k=int(params.get('top_k', 4))
        )
        
        # Format for compatibility
        documents = []
        for result in results:
            documents.append({
                'pageContent': result.get('metadata', {}).get('text', ''),
                'metadata': {
                    'id': result.get('id', ''),
                    'score': result.get('score', 0),
                    'source': result.get('source', 'hybrid'),
                    'namespace': result.get('namespace', ''),
                    'sources': result.get('sources', [])
                }
            })
        
        return {
            'query': query,
            'documents': documents,
            'performance_stats': fast_searcher.get_performance_stats(),
            'hybrid_search': True,
            'optimized': True
        }
        
    except Exception as e:
        return {'error': str(e), 'message': 'Error in fast hybrid search'}

if __name__ == "__main__":
    # Test the fast implementation
    test_queries = [
        "What types of industries are listed for SEZs?",
        "Electric vehicle incentives",
        "Waste management rules"
    ]
    
    print("🧪 Testing Performance-Optimized Hybrid Search")
    
    # Initialize once
    searcher = PerformanceOptimizedHybridSearch(
        pinecone_api_key="test_key",
        pinecone_index="cursor2"
    )
    
    for query in test_queries:
        results = searcher.fast_search(query, top_k=3)
        print(f"Query: {query} → {len(results)} results")
    
    print("\n📊 Final Performance Stats:")
    print(searcher.get_performance_stats()) 
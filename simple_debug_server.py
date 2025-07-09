#!/usr/bin/env python3
"""
Simple Debug Server - Direct component testing
Tests each API connection individually without complex initialization
"""

import os
import time
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "✅ Simple Debug Server Running",
        "timestamp": time.time(),
        "message": "Direct component testing available"
    })

@app.route('/test-groq')
def test_groq():
    """Test Groq API directly"""
    try:
        import groq
        import config
        
        start_time = time.time()
        
        # Test connection
        client = groq.Groq(api_key=config.GROQ_API_KEY)
        
        # Simple test call
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5,
            timeout=10
        )
        
        test_time = time.time() - start_time
        
        return jsonify({
            "status": "✅ Groq API Working",
            "response_time": f"{test_time:.2f}s",
            "response": response.choices[0].message.content,
            "model": "llama3-70b-8192"
        })
        
    except Exception as e:
        return jsonify({
            "status": "❌ Groq API Failed",
            "error": str(e),
            "api_key_set": bool(getattr(config, 'GROQ_API_KEY', None))
        }), 500

@app.route('/test-pinecone')
def test_pinecone():
    """Test Pinecone connection directly"""
    try:
        from pinecone import Pinecone
        import config
        
        start_time = time.time()
        
        # Test connection
        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        index = pc.Index(config.PINECONE_INDEX)
        
        # Test stats call
        stats = index.describe_index_stats()
        
        test_time = time.time() - start_time
        
        return jsonify({
            "status": "✅ Pinecone Working",
            "response_time": f"{test_time:.2f}s",
            "index": config.PINECONE_INDEX,
            "namespaces": list(stats.namespaces.keys()),
            "total_vectors": stats.total_vector_count
        })
        
    except Exception as e:
        return jsonify({
            "status": "❌ Pinecone Failed", 
            "error": str(e),
            "api_key_set": bool(getattr(config, 'PINECONE_API_KEY', None)),
            "index": getattr(config, 'PINECONE_INDEX', 'not set')
        }), 500

@app.route('/test-jina')
def test_jina():
    """Test Jina API directly"""
    try:
        import requests
        import config
        
        start_time = time.time()
        
        jina_api_key = getattr(config, 'JINA_API_KEY', None) or os.getenv('JINA_API_KEY')
        
        url = "https://api.jina.ai/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jina_api_key}"
        }
        data = {
            "model": "jina-embeddings-v3",
            "task": "retrieval.query", 
            "dimensions": 1024,
            "input": ["test"]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        test_time = time.time() - start_time
        
        return jsonify({
            "status": "✅ Jina API Working",
            "response_time": f"{test_time:.2f}s",
            "model": "jina-embeddings-v3",
            "embedding_dimension": len(result['data'][0]['embedding'])
        })
        
    except Exception as e:
        return jsonify({
            "status": "❌ Jina API Failed",
            "error": str(e),
            "api_key_set": bool(jina_api_key)
        }), 500

@app.route('/test-all')
def test_all():
    """Test all components sequentially"""
    results = {}
    
    # Test each component
    components = ['groq', 'pinecone', 'jina']
    
    for component in components:
        try:
            print(f"Testing {component}...")
            if component == 'groq':
                from groq import Groq
                import config
                client = Groq(api_key=config.GROQ_API_KEY)
                test_resp = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=3,
                    timeout=10
                )
                results[component] = "✅ Working"
                
            elif component == 'pinecone':
                from pinecone import Pinecone
                import config
                pc = Pinecone(api_key=config.PINECONE_API_KEY)
                index = pc.Index(config.PINECONE_INDEX)
                stats = index.describe_index_stats()
                results[component] = f"✅ Working ({len(stats.namespaces)} namespaces)"
                
            elif component == 'jina':
                import requests
                import config
                jina_api_key = getattr(config, 'JINA_API_KEY', None) or os.getenv('JINA_API_KEY')
                url = "https://api.jina.ai/v1/embeddings"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {jina_api_key}"
                }
                data = {
                    "model": "jina-embeddings-v3",
                    "task": "retrieval.query",
                    "dimensions": 1024,
                    "input": ["test"]
                }
                response = requests.post(url, headers=headers, json=data, timeout=10)
                response.raise_for_status()
                results[component] = "✅ Working"
                
        except Exception as e:
            results[component] = f"❌ Failed: {str(e)[:100]}"
    
    return jsonify({
        "test_results": results,
        "summary": "All components tested individually",
        "timestamp": time.time()
    })

@app.route('/manual-hybrid-search')
def manual_hybrid_search():
    """Try to manually create hybrid search without complex initialization"""
    try:
        start_time = time.time()
        
        # Import required modules
        from performance_fix_hybrid_search import PerformanceOptimizedHybridSearch
        import config
        
        print("🔧 Creating minimal hybrid search...")
        
        # Get API keys
        jina_api_key = getattr(config, 'JINA_API_KEY', None) or os.getenv('JINA_API_KEY')
        
        # Create with minimal settings
        searcher = PerformanceOptimizedHybridSearch(
            pinecone_api_key=config.PINECONE_API_KEY,
            pinecone_index=config.PINECONE_INDEX,
            jina_api_key=jina_api_key,
            alpha=0.7,
            fusion_method="rrf",
            cache_dir="/tmp/cache"
        )
        
        # Test a simple search
        results = searcher.fast_search("test query", top_k=2)
        
        init_time = time.time() - start_time
        
        return jsonify({
            "status": "✅ Hybrid Search Created Successfully",
            "initialization_time": f"{init_time:.2f}s",
            "test_results": len(results),
            "message": "Manual creation worked!"
        })
        
    except Exception as e:
        return jsonify({
            "status": "❌ Hybrid Search Failed",
            "error": str(e),
            "traceback": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🔧 Starting Simple Debug Server on port {port}")
    print("Available endpoints:")
    print("  /test-groq - Test Groq API")
    print("  /test-pinecone - Test Pinecone")
    print("  /test-jina - Test Jina API")
    print("  /test-all - Test all components")
    print("  /manual-hybrid-search - Manual hybrid search creation")
    
    app.run(host='0.0.0.0', port=port, debug=True) 
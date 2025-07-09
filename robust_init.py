#!/usr/bin/env python3
"""
Robust Initialization with Step-by-Step Testing
This will help identify exactly where the initialization is failing
"""

import os
import time
import traceback

def test_config_access():
    """Test config loading"""
    print("🔍 Testing config access...")
    try:
        import config
        
        # Test each required config value
        required_configs = {
            'PINECONE_API_KEY': config.PINECONE_API_KEY,
            'JINA_API_KEY': config.JINA_API_KEY,
            'GROQ_API_KEY': config.GROQ_API_KEY,
            'PINECONE_INDEX': config.PINECONE_INDEX,
        }
        
        for key, value in required_configs.items():
            if not value or "your_" in value.lower():
                print(f"❌ config.{key}: Invalid or placeholder")
                return False
            else:
                print(f"✅ config.{key}: Valid")
        
        return True
    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        traceback.print_exc()
        return False

def test_pinecone_connection():
    """Test Pinecone connection independently"""
    print("\n🔍 Testing Pinecone connection...")
    try:
        from pinecone import Pinecone
        import config
        
        print("📡 Connecting to Pinecone...")
        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        
        print("📋 Listing indexes...")
        indexes = pc.list_indexes()
        index_names = [idx.name for idx in indexes]
        print(f"✅ Available indexes: {index_names}")
        
        if config.PINECONE_INDEX in index_names:
            print(f"✅ Target index '{config.PINECONE_INDEX}' found")
            
            # Test index access
            print("🔌 Connecting to index...")
            index = pc.Index(config.PINECONE_INDEX)
            
            print("📊 Getting index stats...")
            stats = index.describe_index_stats()
            print(f"✅ Index stats: {stats.total_vector_count} vectors")
            
            return True
        else:
            print(f"❌ Target index '{config.PINECONE_INDEX}' not found")
            return False
            
    except Exception as e:
        print(f"❌ Pinecone connection failed: {e}")
        traceback.print_exc()
        return False

def test_jina_api():
    """Test Jina API connection"""
    print("\n🔍 Testing Jina API...")
    try:
        import requests
        import config
        
        url = "https://api.jina.ai/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.JINA_API_KEY}"
        }
        data = {
            "model": "jina-embeddings-v3",
            "task": "retrieval.query",
            "dimensions": 1024,
            "input": ["test query"]
        }
        
        print("📡 Making test request to Jina API...")
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            embedding = result['data'][0]['embedding']
            print(f"✅ Jina API working, embedding length: {len(embedding)}")
            return True
        else:
            print(f"❌ Jina API returned {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Jina API test failed: {e}")
        traceback.print_exc()
        return False

def test_groq_client():
    """Test Groq client creation"""
    print("\n🔍 Testing Groq client...")
    try:
        import groq
        import config
        
        print("🤖 Creating Groq client...")
        client = groq.Groq(api_key=config.GROQ_API_KEY)
        
        print("✅ Groq client created successfully")
        
        # Test a simple request
        print("📝 Making test request...")
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": "Say 'test successful' in exactly two words."}],
            max_tokens=10,
            temperature=0
        )
        
        response = completion.choices[0].message.content.strip()
        print(f"✅ Groq test response: '{response}'")
        return True
        
    except Exception as e:
        print(f"❌ Groq test failed: {e}")
        traceback.print_exc()
        return False

def test_hybrid_search_init():
    """Test PerformanceOptimizedHybridSearch initialization"""
    print("\n🔍 Testing Hybrid Search initialization...")
    try:
        from performance_fix_hybrid_search import PerformanceOptimizedHybridSearch
        import config
        
        # Create cache directory
        cache_dir = "/tmp/cache"
        os.makedirs(cache_dir, exist_ok=True)
        print(f"✅ Cache directory ready: {cache_dir}")
        
        print("⚡ Initializing PerformanceOptimizedHybridSearch...")
        searcher = PerformanceOptimizedHybridSearch(
            pinecone_api_key=config.PINECONE_API_KEY,
            pinecone_index=config.PINECONE_INDEX,
            jina_api_key=config.JINA_API_KEY,
            alpha=config.DEFAULT_ALPHA,
            fusion_method=config.DEFAULT_FUSION_METHOD,
            cache_dir=cache_dir
        )
        
        print("✅ Hybrid search initialized successfully")
        
        # Test a simple search
        print("🔍 Testing search functionality...")
        results = searcher.fast_search("test query", top_k=2)
        print(f"✅ Search test completed, {len(results)} results")
        
        return True
        
    except Exception as e:
        print(f"❌ Hybrid search initialization failed: {e}")
        traceback.print_exc()
        return False

def run_complete_initialization():
    """Run the complete initialization process"""
    print("🚀 COMPLETE INITIALIZATION TEST")
    print("=" * 50)
    
    tests = [
        ("Config Access", test_config_access),
        ("Pinecone Connection", test_pinecone_connection),
        ("Jina API", test_jina_api),
        ("Groq Client", test_groq_client),
        ("Hybrid Search", test_hybrid_search_init),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
        
        if not results[test_name]:
            print(f"🛑 Stopping at failed test: {test_name}")
            break
    
    print(f"\n{'='*50}")
    print("📊 INITIALIZATION TEST SUMMARY")
    print("-" * 30)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ ALL TESTS PASSED! Initialization should work.")
        return True
    else:
        print(f"\n❌ FAILED AT: {next((name for name, passed in results.items() if not passed), 'Unknown')}")
        print("Fix the failing component and try again.")
        return False

if __name__ == "__main__":
    success = run_complete_initialization()
    exit(0 if success else 1) 
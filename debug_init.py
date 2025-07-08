#!/usr/bin/env python3
"""
Debug script to identify initialization issues
"""

import os
import sys
import traceback

def debug_environment():
    """Debug environment variables and dependencies"""
    print("🔍 DEBUGGING INITIALIZATION")
    print("=" * 50)
    
    # Check environment variables
    required_vars = ["PINECONE_API_KEY", "JINA_API_KEY", "GROQ_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == f"your_{var.lower()}_here":
            missing_vars.append(var)
            print(f"❌ {var}: NOT SET or using placeholder")
        else:
            print(f"✅ {var}: {value[:10]}...")
    
    # Check optional vars
    optional_vars = ["PINECONE_INDEX", "PORT"]
    for var in optional_vars:
        value = os.getenv(var)
        print(f"📋 {var}: {value or 'Not set'}")
    
    if missing_vars:
        print(f"\n❌ MISSING REQUIRED VARIABLES: {', '.join(missing_vars)}")
        print("Please set these in Render dashboard Environment tab")
        return False
    
    print("\n✅ All required environment variables are set")
    return True

def debug_imports():
    """Debug import issues"""
    print("\n🔍 CHECKING IMPORTS")
    print("-" * 30)
    
    try:
        import pinecone
        print("✅ pinecone imported successfully")
    except Exception as e:
        print(f"❌ pinecone import failed: {e}")
        return False
    
    try:
        import groq
        print("✅ groq imported successfully")
    except Exception as e:
        print(f"❌ groq import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except Exception as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        import config
        print("✅ config imported successfully")
    except Exception as e:
        print(f"❌ config import failed: {e}")
        return False
    
    return True

def debug_api_connections():
    """Test API connections"""
    print("\n🔍 TESTING API CONNECTIONS")
    print("-" * 30)
    
    # Test Jina API
    try:
        import requests
        jina_key = os.getenv("JINA_API_KEY")
        if jina_key:
            headers = {"Authorization": f"Bearer {jina_key}"}
            response = requests.get("https://api.jina.ai/v1/models", headers=headers, timeout=10)
            if response.status_code == 200:
                print("✅ Jina API connection successful")
            else:
                print(f"⚠️ Jina API returned {response.status_code}")
        else:
            print("❌ No Jina API key to test")
    except Exception as e:
        print(f"❌ Jina API test failed: {e}")
    
    # Test Pinecone
    try:
        import pinecone
        from pinecone import Pinecone
        
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        indexes = pc.list_indexes()
        print("✅ Pinecone connection successful")
        print(f"   Available indexes: {[idx.name for idx in indexes]}")
    except Exception as e:
        print(f"❌ Pinecone test failed: {e}")
    
    # Test Groq
    try:
        import groq
        client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        # Simple test - just creating client, not making request
        print("✅ Groq client created successfully")
    except Exception as e:
        print(f"❌ Groq test failed: {e}")

def main():
    """Main debug function"""
    print("🚀 RENDER DEPLOYMENT DEBUG")
    print("=" * 50)
    
    success = True
    
    # Check environment
    if not debug_environment():
        success = False
    
    # Check imports
    if not debug_imports():
        success = False
    
    # Test API connections
    debug_api_connections()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ DEBUG COMPLETE - Environment looks good!")
        print("If API still returns 503, wait 30-60 seconds for background initialization")
    else:
        print("❌ DEBUG COMPLETE - Issues found above")
        print("Fix the issues and redeploy")
    
    return success

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Debug script failed: {e}")
        traceback.print_exc()
        sys.exit(1) 
#!/usr/bin/env python3
"""
Render Environment Variable Checker
This script helps debug environment variable issues on Render
"""

import os

def check_render_env():
    print("🔍 Render Environment Variable Check")
    print("=" * 50)
    
    required_vars = [
        "PINECONE_API_KEY",
        "JINA_API_KEY", 
        "GROQ_API_KEY",
        "PINECONE_INDEX",
        "PORT"
    ]
    
    optional_vars = [
        "PINECONE_ENVIRONMENT",
        "PINECONE_HOST",
        "JINA_MODEL",
        "GROQ_MODEL"
    ]
    
    print("📋 Required Variables:")
    all_required_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Show first 10 chars for security
            display_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET")
            all_required_set = False
    
    print("\n📋 Optional Variables:")
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"⚠️  {var}: Using default")
    
    print("=" * 50)
    if all_required_set:
        print("🚀 All required variables are set! Ready for deployment")
        print("🌐 Using Jina API for embeddings (no local models needed)")
    else:
        print("❌ Missing required variables - check Render dashboard Environment tab")
        print("📝 Required: PINECONE_API_KEY, JINA_API_KEY, GROQ_API_KEY, PINECONE_INDEX")
    
    return all_required_set

if __name__ == "__main__":
    check_render_env() 
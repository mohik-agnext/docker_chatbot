#!/usr/bin/env python3
"""
Railway Environment Variable Checker
This script helps debug environment variable issues on Railway
"""

import os

def check_railway_env():
    print("🔍 Railway Environment Variable Check")
    print("=" * 50)
    
    required_vars = [
        "PINECONE_API_KEY",
        "JINA_API_KEY", 
        "GROQ_API_KEY",
        "PINECONE_INDEX",
        "PINECONE_ENVIRONMENT",
        "PINECONE_HOST"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Show first 10 chars for security
            display_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET")
    
    print("=" * 50)
    print("🚀 If all variables show ✅, Railway config is correct")
    print("📋 If any show ❌, check Railway dashboard Variables tab")

if __name__ == "__main__":
    check_railway_env() 
#!/usr/bin/env python3
"""
Deployment Validation Script for Chandigarh Policy Assistant
Ensures all components are ready for production deployment
"""

import os
import sys
import subprocess
import time
import requests
import json

def check_file_exists(filename, description):
    """Check if a required file exists"""
    if os.path.exists(filename):
        print(f"✅ {description}: {filename}")
        return True
    else:
        print(f"❌ {description}: {filename} (MISSING)")
        return False

def check_imports():
    """Check if all required modules can be imported"""
    print("\n🧪 TESTING IMPORTS")
    print("-" * 40)
    
    imports = [
        ("config", "Configuration module"),
        ("performance_fix_hybrid_search", "Performance-optimized search"),
        ("semantic_namespace_mapper", "Namespace intelligence"),

        ("flask", "Flask web framework"),
        ("sentence_transformers", "Embedding model"),
        ("pinecone", "Pinecone vector database"),
        ("groq", "Groq LLM client")
    ]
    
    all_good = True
    for module, description in imports:
        try:
            __import__(module)
            print(f"✅ {description}")
        except ImportError as e:
            print(f"❌ {description}: {e}")
            all_good = False
    
    return all_good

def check_required_files():
    """Check if all required files are present"""
    print("\n📁 CHECKING REQUIRED FILES")
    print("-" * 40)
    
    files = [
        ("config.py", "Configuration file"),

        ("fast_hybrid_search_server.py", "Custom frontend server"),
        ("performance_fix_hybrid_search.py", "Optimized search engine"),
        ("semantic_namespace_mapper.py", "Namespace mapper"),
        ("hybrid_search_frontend.html", "Custom HTML frontend"),
        ("requirements.txt", "Python dependencies"),
        ("requirements-hf.txt", "HuggingFace dependencies"),
        ("README.md", "Documentation"),
        ("Dockerfile", "Docker configuration"),
        ("docker-compose.yml", "Docker Compose configuration"),
        ("start.py", "Startup script"),
        ("hf_config.yaml", "HuggingFace config")
    ]
    
    all_good = True
    for filename, description in files:
        if not check_file_exists(filename, description):
            all_good = False
    
    return all_good

def test_server_startup():
    """Test if the server can start up successfully"""
    print("\n🚀 TESTING SERVER STARTUP")
    print("-" * 40)
    
    try:
        # Start the server in background
        print("Starting server...")
        process = subprocess.Popen(
            [sys.executable, 'fast_hybrid_search_server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to initialize
        time.sleep(5)
        
        # Test health endpoint
        try:
            response = requests.get('http://localhost:3003/api/health', timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Server is healthy")
                print(f"   • LLM Ready: {data.get('llm_ready', False)}")
                print(f"   • Searcher Ready: {data.get('searcher_ready', False)}")
                
                # Test a simple query
                print("Testing search functionality...")
                search_response = requests.post(
                    'http://localhost:3003/api/search',
                    json={"message": "Hello, test query"},
                    timeout=15
                )
                
                if search_response.status_code == 200:
                    print("✅ Search functionality working")
                    return True
                else:
                    print(f"❌ Search test failed: {search_response.status_code}")
                    return False
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Server connection failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        return False
    finally:
        # Clean up
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()

def check_deployment_readiness():
    """Check if the system is ready for deployment"""
    print("\n🎯 DEPLOYMENT READINESS CHECK")
    print("-" * 40)
    
    checks = []
    
    # Check configuration
    try:
        import config
        if hasattr(config, 'PINECONE_API_KEY') and hasattr(config, 'GROQ_API_KEY'):
            print("✅ Configuration keys defined")
            checks.append(True)
        else:
            print("❌ Missing API keys in configuration")
            checks.append(False)
    except:
        print("❌ Configuration import failed")
        checks.append(False)
    
    # Check cache directory
    if os.path.exists('cache') or os.path.exists('./cache'):
        print("✅ Cache directory exists")
        checks.append(True)
    else:
        print("⚠️  Cache directory missing (will be created automatically)")
        checks.append(True)  # Not critical
    
    # Check txt_files directory
    if os.path.exists('txt_files'):
        print("✅ Text files directory exists")
        checks.append(True)
    else:
        print("⚠️  txt_files directory missing")
        checks.append(False)
    
    return all(checks)

def main():
    """Run complete validation"""
    print("🏛️  CHANDIGARH POLICY ASSISTANT - DEPLOYMENT VALIDATION")
    print("=" * 70)
    
    results = []
    
    # Run all checks
    results.append(check_required_files())
    results.append(check_imports())
    results.append(test_server_startup())
    results.append(check_deployment_readiness())
    
    # Final report
    print("\n" + "=" * 70)
    print("📊 FINAL VALIDATION REPORT")
    print("=" * 70)
    
    if all(results):
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Your Chandigarh Policy Assistant is READY FOR DEPLOYMENT!")
        print("\n🚀 Next Steps:")
        print("   1. Set your API keys in config.py")
        print("   2. Run: python start.py")
        print("   3. Choose option 1 for Local Development or 2 for Docker")
        print("   4. For HuggingFace Spaces: upload all files and use requirements-hf.txt")
        print("   5. For Docker: run docker-compose up --build")
        return 0
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please fix the issues above before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
#!/usr/bin/env python3
"""
Quick Debug Script for Render Deployment Issues
Tests each component independently to identify the root cause
"""

import os
import sys
import time
import traceback

def test_basic_imports():
    """Test if basic imports work"""
    print("🔍 TESTING BASIC IMPORTS")
    print("-" * 40)
    
    try:
        import json
        print("✅ json: OK")
    except Exception as e:
        print(f"❌ json: {e}")
        return False
    
    try:
        import time
        print("✅ time: OK")
    except Exception as e:
        print(f"❌ time: {e}")
        return False
        
    try:
        import os
        print("✅ os: OK")
    except Exception as e:
        print(f"❌ os: {e}")
        return False
    
    try:
        from flask import Flask
        print("✅ flask: OK")
    except Exception as e:
        print(f"❌ flask: {e}")
        return False
        
    return True

def test_environment():
    """Test environment variables"""
    print("\n🔍 TESTING ENVIRONMENT VARIABLES")
    print("-" * 40)
    
    # Critical variables
    critical_vars = {
        "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
        "JINA_API_KEY": os.getenv("JINA_API_KEY"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "PORT": os.getenv("PORT")
    }
    
    all_set = True
    for var, value in critical_vars.items():
        if not value or "your_" in value.lower():
            print(f"❌ {var}: NOT SET or placeholder")
            all_set = False
        else:
            print(f"✅ {var}: {value[:8]}...")
    
    # Optional but important
    optional_vars = {
        "PINECONE_INDEX": os.getenv("PINECONE_INDEX", "cursor2"),
        "PINECONE_HOST": os.getenv("PINECONE_HOST"),
        "FLASK_ENV": os.getenv("FLASK_ENV", "production")
    }
    
    for var, value in optional_vars.items():
        print(f"📋 {var}: {value or 'Not set'}")
    
    return all_set

def test_minimal_flask():
    """Test if a minimal Flask app can start"""
    print("\n🔍 TESTING MINIMAL FLASK APP")
    print("-" * 40)
    
    try:
        from flask import Flask, jsonify
        
        app = Flask(__name__)
        
        @app.route('/')
        def hello():
            return jsonify({"status": "ok", "message": "Minimal Flask is working"})
            
        @app.route('/health')
        def health():
            return jsonify({"status": "healthy", "timestamp": time.time()})
            
        @app.route('/ready')
        def ready():
            return jsonify({
                "status": "ready", 
                "port": os.getenv("PORT", "unknown"),
                "env_vars_set": bool(os.getenv("PINECONE_API_KEY"))
            })
        
        print("✅ Minimal Flask app created successfully")
        
        # Test if we can get the port
        port = int(os.getenv("PORT", 10000))
        print(f"✅ Port configured: {port}")
        
        return app, port
        
    except Exception as e:
        print(f"❌ Minimal Flask failed: {e}")
        traceback.print_exc()
        return None, None

def test_api_dependencies():
    """Test if API dependencies can be imported"""
    print("\n🔍 TESTING API DEPENDENCIES")
    print("-" * 40)
    
    deps = {
        "pinecone": False,
        "groq": False, 
        "requests": False,
        "numpy": False
    }
    
    for dep in deps:
        try:
            __import__(dep)
            print(f"✅ {dep}: OK")
            deps[dep] = True
        except Exception as e:
            print(f"❌ {dep}: {e}")
    
    return all(deps.values())

def test_config_loading():
    """Test if config.py loads properly"""
    print("\n🔍 TESTING CONFIG LOADING")
    print("-" * 40)
    
    try:
        import config
        print("✅ config.py imported")
        
        # Test accessing config values
        attrs = ["PINECONE_API_KEY", "JINA_API_KEY", "GROQ_API_KEY"]
        for attr in attrs:
            value = getattr(config, attr, "NOT_FOUND")
            if "your_" in value.lower():
                print(f"⚠️ config.{attr}: Using placeholder value")
            else:
                print(f"✅ config.{attr}: Set")
        
        return True
    except Exception as e:
        print(f"❌ config loading failed: {e}")
        traceback.print_exc()
        return False

def run_minimal_server():
    """Run a minimal server for testing"""
    print("\n🚀 ATTEMPTING TO START MINIMAL SERVER")
    print("-" * 40)
    
    app, port = test_minimal_flask()
    if not app:
        return False
    
    try:
        print(f"Starting minimal server on port {port}...")
        print(f"This should be accessible at http://localhost:{port}")
        print("Press Ctrl+C to stop")
        
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    print("🚨 RENDER 502 ERROR DEBUG")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Environment: {os.getenv('FLASK_ENV', 'unknown')}")
    
    # Run all tests
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Environment Variables", test_environment),
        ("API Dependencies", test_api_dependencies),
        ("Config Loading", test_config_loading)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 50)
    print("📊 DEBUG SUMMARY")
    print("-" * 30)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ All basic tests passed!")
        print("🚀 Attempting to start minimal server...")
        run_minimal_server()
    else:
        print("\n❌ Some tests failed. Fix these issues first:")
        for test_name, passed in results.items():
            if not passed:
                print(f"   • {test_name}")
        
        print("\n🔧 LIKELY SOLUTIONS:")
        if not results.get("Environment Variables", True):
            print("   1. Set missing API keys in Render dashboard")
        if not results.get("API Dependencies", True):
            print("   2. Check requirements.txt and rebuild")
        if not results.get("Config Loading", True):
            print("   3. Fix config.py file issues")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Minimal Server for Debugging 502 Errors
This server starts immediately without complex initialization
"""

import os
import time
import json
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

# Basic configuration
PORT = int(os.environ.get('PORT', 10000))

@app.route('/')
def home():
    """Simple home page"""
    return jsonify({
        "status": "✅ Minimal server is running!",
        "message": "🏛️ Chandigarh Policy Assistant - Debug Mode",
        "port": PORT,
        "timestamp": time.time(),
        "environment": os.getenv("FLASK_ENV", "unknown"),
        "python_version": os.sys.version.split()[0]
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "server": "minimal_debug",
        "timestamp": time.time()
    })

@app.route('/ready')
def ready():
    """Ready check endpoint"""
    env_status = {}
    required_vars = ["PINECONE_API_KEY", "JINA_API_KEY", "GROQ_API_KEY"]
    
    for var in required_vars:
        value = os.getenv(var)
        if value and "your_" not in value.lower():
            env_status[var] = "✅ Set"
        else:
            env_status[var] = "❌ Missing or placeholder"
    
    return jsonify({
        "status": "ready",
        "message": "Minimal server is ready",
        "environment_variables": env_status,
        "port": PORT,
        "timestamp": time.time()
    })

@app.route('/debug')
def debug():
    """Debug information endpoint"""
    return jsonify({
        "server_info": {
            "type": "minimal_debug_server",
            "port": PORT,
            "working_directory": os.getcwd(),
            "python_version": os.sys.version
        },
        "environment_variables": {
            var: ("✅ Set" if os.getenv(var) and "your_" not in os.getenv(var, "").lower() else "❌ Missing")
            for var in ["PINECONE_API_KEY", "JINA_API_KEY", "GROQ_API_KEY", "PINECONE_INDEX", "PORT", "FLASK_ENV"]
        },
        "files_present": {
            "config.py": os.path.exists("config.py"),
            "fast_hybrid_search_server.py": os.path.exists("fast_hybrid_search_server.py"),
            "performance_fix_hybrid_search.py": os.path.exists("performance_fix_hybrid_search.py"),
            "cache_directory": os.path.exists("cache")
        },
        "timestamp": time.time()
    })

@app.route('/api/test', methods=['POST'])
def api_test():
    """Simple API test endpoint"""
    try:
        data = request.get_json() or {}
        message = data.get('message', 'No message provided')
        
        return jsonify({
            "response": f"✅ API is working! You sent: '{message}'",
            "status": "success",
            "timestamp": time.time(),
            "note": "This is the minimal debug server. Full AI features require proper initialization."
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error",
            "timestamp": time.time()
        }), 500

@app.route('/test-imports')
def test_imports():
    """Test if critical imports work"""
    results = {}
    imports = [
        "json", "time", "os", "sys", 
        "flask", "pinecone", "groq", "requests", "numpy"
    ]
    
    for module in imports:
        try:
            __import__(module)
            results[module] = "✅ OK"
        except Exception as e:
            results[module] = f"❌ Error: {str(e)}"
    
    return jsonify({
        "import_test_results": results,
        "timestamp": time.time(),
        "note": "These are the Python module import test results"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "This endpoint doesn't exist on the minimal debug server",
        "available_endpoints": [
            "/", "/health", "/ready", "/debug", 
            "/api/test", "/test-imports"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "An error occurred in the minimal debug server",
        "timestamp": time.time()
    }), 500

if __name__ == '__main__':
    print("🚨 STARTING MINIMAL DEBUG SERVER")
    print("=" * 50)
    print(f"🌐 Port: {PORT}")
    print(f"🔧 Environment: {os.getenv('FLASK_ENV', 'unknown')}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print("=" * 50)
    print("📋 Available endpoints:")
    print("  • /         - Server status")
    print("  • /health   - Health check")
    print("  • /ready    - Ready check with env vars")
    print("  • /debug    - Full debug information")
    print("  • /api/test - API functionality test")
    print("  • /test-imports - Python imports test")
    print("=" * 50)
    print("🚀 Starting server...")
    
    try:
        app.run(
            host='0.0.0.0',
            port=PORT,
            debug=False,
            threaded=True
        )
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        import traceback
        traceback.print_exc() 
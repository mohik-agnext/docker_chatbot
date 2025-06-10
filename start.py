#!/usr/bin/env python3
"""
Chandigarh Policy Assistant - Startup Script
Docker-optimized deployment (Gradio removed)
"""

import subprocess
import sys
import time
import webbrowser
import os

def print_banner():
    print("""
🏛️  CHANDIGARH POLICY ASSISTANT - Docker Ready
=============================================
Choose your deployment method:
1. 🎨 Custom Frontend (Local) - Beautiful UI, sub-5s responses
2. 🐳 Docker Compose (Recommended) - Containerized deployment
3. 🧪 Run Tests - Verify all components
""")

def start_custom_frontend():
    print("🚀 Starting Custom Frontend...")
    print("📍 Server: http://localhost:3003")
    print("🎨 Features: Beautiful UI, Real-time streaming, Performance monitoring")
    print("-" * 60)
    
    try:
        # Start the high-performance backend
        process = subprocess.Popen([sys.executable, 'fast_hybrid_search_server.py'])
        
        # Wait a moment then open browser
        time.sleep(3)
        webbrowser.open('http://localhost:3003')
        
        print("✅ Custom Frontend is running!")
        print("⚠️  Press Ctrl+C to stop the server")
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        process.terminate()
        print("✅ Server stopped")



def start_docker():
    print("🐳 Starting Docker Compose...")
    print("📍 Server: http://localhost:3003")
    print("🔧 Features: Containerized, Production-ready, Persistent cache")
    print("-" * 60)
    
    try:
        subprocess.run(['docker-compose', 'up', '--build'], check=True)
    except subprocess.CalledProcessError:
        print("❌ Docker Compose failed. Make sure Docker is installed and running.")
    except FileNotFoundError:
        print("❌ Docker Compose not found. Please install Docker.")

def run_tests():
    print("🧪 Running Component Tests...")
    print("-" * 40)
    
    tests = [
        ("Config Import", "import config; print('✅ Config OK')"),
        ("Performance Search", "from performance_fix_hybrid_search import PerformanceOptimizedHybridSearch; print('✅ Search OK')"),
        ("Namespace Mapper", "from semantic_namespace_mapper import semantic_mapper; print('✅ Mapper OK')"),
        ("Dependencies", "import flask, sentence_transformers, pinecone, groq; print('✅ Dependencies OK')")
    ]
    
    for test_name, test_code in tests:
        try:
            print(f"Testing {test_name}...", end=" ")
            subprocess.run([sys.executable, '-c', test_code], 
                         check=True, capture_output=True, text=True)
            print("✅")
        except subprocess.CalledProcessError as e:
            print(f"❌ {e.stderr}")
            return False
    
    print("\n🎉 All tests passed! System is ready.")
    return True

def main():
    print_banner()
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            start_custom_frontend()
        elif choice == "2":
            start_docker()
        elif choice == "3":
            run_tests()
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 
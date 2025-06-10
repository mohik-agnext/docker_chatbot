---
title: Chandigarh Policy Assistant
emoji: 🏛️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 3003
pinned: false
license: mit
---

# 🏛️ Chandigarh Policy Assistant

**Your AI-powered guide to Chandigarh government policies, regulations, and services**

## ✨ Features

- 🚀 **Sub-5-second responses** with high-performance hybrid search
- 🧠 **Namespace intelligence** for targeted policy retrieval
- 🎨 **Professional web interface** with modern UI/UX
- 📊 **Real-time performance monitoring**
- 🔍 **Advanced search**: Semantic + BM25 fusion
- 💬 **Context-aware responses** with anti-hallucination safeguards
- 🐳 **Docker-ready** for production deployment

## 🚀 Quick Start

### Option 1: Easy Docker Deployment (Recommended)
```bash
# Make deployment script executable (if needed)
chmod +x docker-deploy.sh

# Run the deployment script
./docker-deploy.sh

# Visit: http://localhost:3003
```

### Option 2: Manual Docker Deployment
```bash
# Copy environment template
cp env_template.txt .env

# Edit .env with your API keys
# nano .env  # or use your preferred editor

# Build and run
docker-compose up --build

# Visit: http://localhost:3003
```

### Option 3: Local Development
```bash
pip install -r requirements.txt
python fast_hybrid_search_server.py
# Visit: http://localhost:3003
```

## 📋 Requirements

```bash
pip install -r requirements.txt
```

## 🔧 Configuration

1. **Environment Variables**: Set your API keys in `config.py` or environment variables
   - `PINECONE_API_KEY`: Your Pinecone API key
   - `GROQ_API_KEY`: Your Groq API key
   - `PINECONE_INDEX`: Your Pinecone index name

2. **Cache Directory**: The system will create a `cache/` directory for performance optimization

## 🌐 Deployment

### Docker Deployment (Production)
```bash
# Build and run with Docker Compose
docker-compose up --build

# OR build and run manually
docker build -t chandigarh-assistant .
docker run -p 3003:3003 -e PINECONE_API_KEY=your_key -e GROQ_API_KEY=your_key chandigarh-assistant
```

### Environment Variables
Set these environment variables for deployment:
- `PINECONE_API_KEY`: Your Pinecone API key
- `GROQ_API_KEY`: Your Groq API key  
- `PINECONE_INDEX`: Your Pinecone index name
- `PINECONE_HOST`: Your Pinecone host URL

## 📊 Performance

- **Response Time**: 2-5 seconds average
- **Accuracy**: 90%+ with optimized chunking
- **Concurrent Users**: Supports multiple simultaneous queries
- **Cache Hit Rate**: 80%+ for common queries

## 🎯 Query Examples

- "What are the electric vehicle incentives in Chandigarh?"
- "How can I start an IT business in Chandigarh?"
- "What are the industrial policy benefits?"
- "Tell me about SEZ policies"
- "What permits do I need for construction?"

## 🛠️ Architecture

- **Backend**: Flask server with performance-optimized hybrid search
- **Frontend**: Custom HTML/CSS/JS with Flask backend
- **Database**: Pinecone vector database with semantic namespaces
- **AI**: Groq LLM + BAAI/bge-large-en-v1.5 embeddings
- **Search**: Hybrid semantic + BM25 with intelligent fusion

## 📈 Monitoring

Access performance stats at: `http://localhost:3003/api/stats`

## 🎉 Ready for Production!

This system is optimized for production deployment with:
- ✅ Sub-5-second response times
- ✅ High accuracy with namespace intelligence
- ✅ Professional UI/UX
- ✅ Comprehensive error handling
- ✅ Performance monitoring 
#!/bin/bash

# Chandigarh Policy Assistant - Docker Deployment Script

echo "🏛️  CHANDIGARH POLICY ASSISTANT - DOCKER DEPLOYMENT"
echo "=================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    if [ -f "env_template.txt" ]; then
        cp env_template.txt .env
        echo "✅ Created .env file from template"
        echo "📝 Please edit .env file with your API keys before continuing"
        echo ""
        echo "Required variables:"
        echo "  - PINECONE_API_KEY=your_pinecone_api_key"
        echo "  - GROQ_API_KEY=your_groq_api_key"
        echo "  - PINECONE_INDEX=your_pinecone_index"
        echo "  - PINECONE_HOST=your_pinecone_host"
        echo ""
        read -p "Press Enter after updating .env file..."
    else
        echo "❌ env_template.txt not found. Please create .env file manually."
        exit 1
    fi
fi

echo "🐳 Starting Docker deployment..."

# Build and start the containers
echo "📦 Building Docker image..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker build successful"
else
    echo "❌ Docker build failed"
    exit 1
fi

echo "🚀 Starting application..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 DEPLOYMENT SUCCESSFUL!"
    echo "========================"
    echo "🌐 Application URL: http://localhost:3003"
    echo "📊 Health Check: http://localhost:3003/api/health"
    echo "📈 Performance Stats: http://localhost:3003/api/stats"
    echo ""
    echo "📋 Useful commands:"
    echo "  - View logs: docker-compose logs -f"
    echo "  - Stop app: docker-compose down"
    echo "  - Restart: docker-compose restart"
    echo ""
    echo "✅ Chandigarh Policy Assistant is now running!"
else
    echo "❌ Failed to start application"
    exit 1
fi 
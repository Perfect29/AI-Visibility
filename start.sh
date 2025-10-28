#!/bin/bash

# AI Visibility Tool - Docker Setup Script

echo "🚀 Starting AI Visibility Tool with Docker..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "📝 Created .env from template"
    else
        cat > .env << EOF
# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Override default settings
# HOST=0.0.0.0
# PORT=8000
# DEBUG=false
EOF
        echo "📝 Created .env template"
    fi
    echo "📝 Please edit .env file and add your OpenAI API key"
    echo "   Then run this script again"
    exit 1
fi

# Check if OPENAI_API_KEY is set
if grep -q "your_openai_api_key_here" .env; then
    echo "❌ Please set your OpenAI API key in .env file"
    exit 1
fi

echo "🔧 Building Docker image..."
docker-compose build

echo "🚀 Starting application..."
docker-compose up -d

echo "✅ Application is starting up!"
echo "🌐 Frontend: http://localhost:8000"
echo "🔗 API: http://localhost:8000/api"
echo ""
echo "📊 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"

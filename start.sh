#!/bin/bash

# Nova Reel MCP Server Quick Start Script

set -e

echo "🎬 Amazon Nova Reel MCP Server Quick Start"
echo "=========================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo "Please copy .env.example to .env and configure your AWS credentials:"
    echo ""
    echo "  cp .env.example .env"
    echo "  # Edit .env with your AWS credentials"
    echo ""
    exit 1
fi

# Source environment variables
echo "📋 Loading environment variables..."
export $(cat .env | grep -v '^#' | xargs)

# Check required variables
if [ -z "$S3_BUCKET" ]; then
    echo "❌ Missing required S3_BUCKET environment variable!"
    echo "Please ensure .env contains S3_BUCKET"
    exit 1
fi

# Check if we have valid credential configuration
if [ -n "$AWS_PROFILE" ]; then
    echo "✅ Using AWS Profile: $AWS_PROFILE"
elif [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "✅ Using explicit AWS credentials"
    if [ -n "$AWS_SESSION_TOKEN" ]; then
        echo "   (with session token for temporary credentials)"
    fi
else
    echo "❌ Missing AWS credentials configuration!"
    echo "Please ensure .env contains either:"
    echo "  Option 1: AWS_PROFILE=your-profile-name"
    echo "  Option 2: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
    echo "           (optionally with AWS_SESSION_TOKEN for temporary credentials)"
    exit 1
fi

echo "✅ Environment configured:"
echo "   AWS Region: ${AWS_REGION:-us-east-1}"
echo "   S3 Bucket: $S3_BUCKET"
echo ""

# Check if we should run stdio or sse version
MODE=${1:-stdio}

case $MODE in
    stdio)
        echo "🚀 Starting Nova Reel MCP Server (STDIO mode)..."
        echo "   This mode is for direct MCP client connections."
        echo ""
        # Build command with conditional parameters
        CMD="python main.py --aws-region ${AWS_REGION:-us-east-1} --s3-bucket $S3_BUCKET"
        if [ -n "$AWS_PROFILE" ]; then
            CMD="$CMD --aws-profile $AWS_PROFILE"
        elif [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
            CMD="$CMD --aws-access-key-id $AWS_ACCESS_KEY_ID --aws-secret-access-key $AWS_SECRET_ACCESS_KEY"
            if [ -n "$AWS_SESSION_TOKEN" ]; then
                CMD="$CMD --aws-session-token $AWS_SESSION_TOKEN"
            fi
        fi
        eval $CMD
        ;;
    sse)
        echo "🚀 Starting Nova Reel MCP Server (SSE mode)..."
        echo "   This mode provides a web interface."
        echo "   Access: http://localhost:8000"
        echo ""
        # Build command with conditional parameters
        CMD="python -m novareel_mcp_server.server_sse --aws-region ${AWS_REGION:-us-east-1} --s3-bucket $S3_BUCKET --host 0.0.0.0 --port 8000"
        if [ -n "$AWS_PROFILE" ]; then
            CMD="$CMD --aws-profile $AWS_PROFILE"
        elif [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
            CMD="$CMD --aws-access-key-id $AWS_ACCESS_KEY_ID --aws-secret-access-key $AWS_SECRET_ACCESS_KEY"
            if [ -n "$AWS_SESSION_TOKEN" ]; then
                CMD="$CMD --aws-session-token $AWS_SESSION_TOKEN"
            fi
        fi
        eval $CMD
        ;;
    http)
        echo "🚀 Starting Nova Reel MCP Server (HTTP Streaming mode)..."
        echo "   This mode provides HTTP streaming transport."
        echo "   Access: http://localhost:8001"
        echo ""
        # Build command with conditional parameters
        CMD="python -m novareel_mcp_server.server_http --aws-region ${AWS_REGION:-us-east-1} --s3-bucket $S3_BUCKET --host 0.0.0.0 --port 8001"
        if [ -n "$AWS_PROFILE" ]; then
            CMD="$CMD --aws-profile $AWS_PROFILE"
        elif [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
            CMD="$CMD --aws-access-key-id $AWS_ACCESS_KEY_ID --aws-secret-access-key $AWS_SECRET_ACCESS_KEY"
            if [ -n "$AWS_SESSION_TOKEN" ]; then
                CMD="$CMD --aws-session-token $AWS_SESSION_TOKEN"
            fi
        fi
        eval $CMD
        ;;
    docker-stdio)
        echo "🐳 Starting Nova Reel MCP Server (Docker STDIO)..."
        docker-compose up novareel-stdio
        ;;
    docker-sse)
        echo "🐳 Starting Nova Reel MCP Server (Docker SSE)..."
        echo "   Access: http://localhost:8000"
        docker-compose up novareel-sse
        ;;
    docker-http)
        echo "🐳 Starting Nova Reel MCP Server (Docker HTTP Streaming)..."
        echo "   Access: http://localhost:8001"
        docker-compose up novareel-http
        ;;
    docker-all)
        echo "🐳 Starting all Nova Reel MCP Servers (Docker)..."
        echo "   SSE Access: http://localhost:8000"
        echo "   HTTP Access: http://localhost:8001"
        docker-compose up -d
        echo "✅ All servers started in background"
        echo "   Use 'docker-compose logs -f' to view logs"
        echo "   Use 'docker-compose down' to stop"
        ;;
    docker-both)
        echo "🐳 Starting both Nova Reel MCP Servers (Docker - legacy)..."
        echo "   SSE Access: http://localhost:8000"
        docker-compose up -d novareel-stdio novareel-sse
        echo "✅ Both servers started in background"
        echo "   Use 'docker-compose logs -f' to view logs"
        echo "   Use 'docker-compose down' to stop"
        ;;
    build)
        echo "🔨 Building all Docker images..."
        ./build-all.sh
        ;;
    build-stdio)
        echo "🔨 Building STDIO Docker image..."
        ./build-stdio.sh
        ;;
    build-sse)
        echo "🔨 Building SSE Docker image..."
        ./build-sse.sh
        ;;
    build-http)
        echo "🔨 Building HTTP Streaming Docker image..."
        ./build-http.sh
        ;;
    build-package)
        echo "🔨 Building Python package..."
        ./build.sh
        ;;
    *)
        echo "❌ Invalid mode: $MODE"
        echo ""
        echo "Usage: $0 [mode]"
        echo ""
        echo "Available modes:"
        echo "  stdio         - Run STDIO version locally (default)"
        echo "  sse           - Run SSE version locally"
        echo "  http          - Run HTTP Streaming version locally"
        echo "  docker-stdio  - Run STDIO version in Docker"
        echo "  docker-sse    - Run SSE version in Docker"
        echo "  docker-http   - Run HTTP Streaming version in Docker"
        echo "  docker-both   - Run STDIO + SSE versions in Docker (legacy)"
        echo "  docker-all    - Run all three versions in Docker"
        echo "  build         - Build all Docker images"
        echo "  build-stdio   - Build STDIO Docker image"
        echo "  build-sse     - Build SSE Docker image"
        echo "  build-http    - Build HTTP Streaming Docker image"
        echo "  build-package - Build Python package (wheel)"
        echo ""
        echo "Examples:"
        echo "  $0                 # Run STDIO version locally"
        echo "  $0 sse            # Run SSE version locally"
        echo "  $0 http           # Run HTTP Streaming version locally"
        echo "  $0 build-package  # Build Python wheel for uvx"
        echo "  $0 build          # Build all Docker images"
        echo "  $0 docker-all     # Run all three versions in Docker"
        exit 1
        ;;
esac

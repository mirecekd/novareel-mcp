#!/bin/bash

# Build script for NovaReel MCP Server - HTTP Streaming version

set -e

echo "Building NovaReel MCP Server - HTTP Streaming version..."

# Build Docker image
docker build -f Dockerfile.http -t mirecekd/novareel-mcp-server:http .

echo "Build completed successfully!"
echo "Image: mirecekd/novareel-mcp-server:http"
echo ""
echo "To run the HTTP streaming server:"
echo "docker run -p 8001:8001 -e AWS_ACCESS_KEY_ID=your_key -e AWS_SECRET_ACCESS_KEY=your_secret -e S3_BUCKET=your_bucket mirecekd/novareel-mcp-server:http"
echo ""
echo "Or with command line arguments:"
echo "docker run -p 8001:8001 mirecekd/novareel-mcp-server:http --aws-access-key-id your_key --aws-secret-access-key your_secret --s3-bucket your_bucket"

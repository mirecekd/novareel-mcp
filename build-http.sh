#!/bin/bash

# Build script for NovaReel MCP Server - HTTP Streaming version

set -e

echo "Building NovaReel MCP Server - HTTP Streaming version..."

# Build Docker image
docker build -f Dockerfile.http -t mirecekd/novareel-mcp-server:http .

echo "Build completed successfully!"
echo "Image: mirecekd/novareel-mcp-server:http"
echo ""
echo "Usage examples:"
echo ""
echo "  Environment variables:"
echo "    docker run -p 8001:8001 -e AWS_ACCESS_KEY_ID=your_key -e AWS_SECRET_ACCESS_KEY=your_secret -e S3_BUCKET=your_bucket mirecekd/novareel-mcp-server:http"
echo ""
echo "  With session token (temporary credentials):"
echo "    docker run -p 8001:8001 -e AWS_ACCESS_KEY_ID=your_key -e AWS_SECRET_ACCESS_KEY=your_secret -e AWS_SESSION_TOKEN=your_token -e S3_BUCKET=your_bucket mirecekd/novareel-mcp-server:http"
echo ""
echo "  With AWS profile:"
echo "    docker run -p 8001:8001 -v ~/.aws:/root/.aws -e AWS_PROFILE=my-profile -e S3_BUCKET=your_bucket mirecekd/novareel-mcp-server:http"
echo ""
echo "  Command line arguments:"
echo "    docker run -p 8001:8001 mirecekd/novareel-mcp-server:http --aws-access-key-id your_key --aws-secret-access-key your_secret --s3-bucket your_bucket"
echo ""
echo "  Command line with session token:"
echo "    docker run -p 8001:8001 mirecekd/novareel-mcp-server:http --aws-access-key-id your_key --aws-secret-access-key your_secret --aws-session-token your_token --s3-bucket your_bucket"
echo ""
echo "  Command line with AWS profile:"
echo "    docker run -p 8001:8001 -v ~/.aws:/root/.aws mirecekd/novareel-mcp-server:http --aws-profile my-profile --s3-bucket your_bucket"
echo ""
echo "HTTP streaming server will be available at: http://localhost:8001"

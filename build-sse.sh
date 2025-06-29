#!/bin/bash

echo "Building Nova Reel MCP Server - SSE Version (HTTP transport)"
echo "============================================================"

docker build -f Dockerfile.sse -t mirecekd/novareel-mcp-server:sse -t mirecekd/novareel-mcp-sse .

echo ""
echo "Build completed!"
echo "SSE Version tags:"
echo "  - mirecekd/novareel-mcp-server:sse"
echo "  - mirecekd/novareel-mcp-sse"
echo ""
echo "Usage examples:"
echo ""
echo "  Environment variables:"
echo "    docker run -e AWS_ACCESS_KEY_ID=YOUR_KEY -e AWS_SECRET_ACCESS_KEY=YOUR_SECRET -e S3_BUCKET=YOUR_BUCKET -p 8000:8000 mirecekd/novareel-mcp-server:sse"
echo ""
echo "  With session token (temporary credentials):"
echo "    docker run -e AWS_ACCESS_KEY_ID=YOUR_KEY -e AWS_SECRET_ACCESS_KEY=YOUR_SECRET -e AWS_SESSION_TOKEN=YOUR_TOKEN -e S3_BUCKET=YOUR_BUCKET -p 8000:8000 mirecekd/novareel-mcp-server:sse"
echo ""
echo "  With AWS profile:"
echo "    docker run -v ~/.aws:/root/.aws -e AWS_PROFILE=my-profile -e S3_BUCKET=YOUR_BUCKET -p 8000:8000 mirecekd/novareel-mcp-server:sse"
echo ""
echo "SSE server will be available at: http://localhost:8000"

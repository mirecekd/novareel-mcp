#!/bin/bash

echo "Building All Nova Reel MCP Server Versions"
echo "=========================================="
echo ""

echo "1. Building STDIO Version (stdio transport)..."
echo "---------------------------------------------"
docker build -f Dockerfile.stdio -t mirecekd/novareel-mcp-server:stdio -t mirecekd/novareel-mcp-server:latest .

echo ""
echo "2. Building SSE Version (Server-Sent Events transport)..."
echo "--------------------------------------------------------"
docker build -f Dockerfile.sse -t mirecekd/novareel-mcp-server:sse -t mirecekd/novareel-mcp-sse .

echo ""
echo "3. Building HTTP Version (HTTP Streaming transport)..."
echo "-----------------------------------------------------"
docker build -f Dockerfile.http -t mirecekd/novareel-mcp-server:http .

echo ""
echo "✅ All builds completed!"
echo "========================"
echo ""
echo "Available images:"
echo "  STDIO Version:"
echo "    - mirecekd/novareel-mcp-server:stdio"
echo "    - mirecekd/novareel-mcp-server:latest"
echo "  SSE Version:"
echo "    - mirecekd/novareel-mcp-server:sse"
echo "    - mirecekd/novareel-mcp-sse"
echo "  HTTP Streaming Version:"
echo "    - mirecekd/novareel-mcp-server:http"
echo ""
echo "Usage examples:"
echo "  STDIO:  docker run --rm -i mirecekd/novareel-mcp-server:stdio --aws-access-key-id KEY --aws-secret-access-key SECRET --s3-bucket BUCKET"
echo "  SSE:    docker run -e AWS_ACCESS_KEY_ID=KEY -e AWS_SECRET_ACCESS_KEY=SECRET -e S3_BUCKET=BUCKET -p 8000:8000 mirecekd/novareel-mcp-server:sse"
echo "  HTTP:   docker run -e AWS_ACCESS_KEY_ID=KEY -e AWS_SECRET_ACCESS_KEY=SECRET -e S3_BUCKET=BUCKET -p 8001:8001 mirecekd/novareel-mcp-server:http"

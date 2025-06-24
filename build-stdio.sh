#!/bin/bash

echo "Building Nova Reel MCP Server - STDIO Version (stdio transport)"
echo "================================================================"

docker build -f Dockerfile.stdio -t mirecekd/novareel-mcp-server:stdio -t mirecekd/novareel-mcp-server:latest .

echo ""
echo "Build completed!"
echo "STDIO Version tags:"
echo "  - mirecekd/novareel-mcp-server:stdio"
echo "  - mirecekd/novareel-mcp-server:latest"
echo ""
echo "Usage:"
echo "  docker run --rm -i mirecekd/novareel-mcp-server:stdio --aws-access-key-id YOUR_KEY --aws-secret-access-key YOUR_SECRET --s3-bucket YOUR_BUCKET"

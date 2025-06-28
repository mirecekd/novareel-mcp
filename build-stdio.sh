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
echo "Usage examples:"
echo ""
echo "  Explicit credentials:"
echo "    docker run --rm -i mirecekd/novareel-mcp-server:stdio --aws-access-key-id YOUR_KEY --aws-secret-access-key YOUR_SECRET --s3-bucket YOUR_BUCKET"
echo ""
echo "  With session token (temporary credentials):"
echo "    docker run --rm -i mirecekd/novareel-mcp-server:stdio --aws-access-key-id YOUR_KEY --aws-secret-access-key YOUR_SECRET --aws-session-token YOUR_TOKEN --s3-bucket YOUR_BUCKET"
echo ""
echo "  With AWS profile:"
echo "    docker run --rm -i -v ~/.aws:/root/.aws mirecekd/novareel-mcp-server:stdio --aws-profile my-profile --s3-bucket YOUR_BUCKET"

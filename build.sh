#!/bin/bash

echo "Building Nova Reel MCP Server Python Package"
echo "============================================"

# Check if build module is installed
if ! python3 -c "import build" 2>/dev/null; then
    echo "Installing build module..."
    pip install build
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "Building package..."
python3 -m build

echo ""
echo "✅ Build completed!"
echo "Generated files:"
ls -la dist/

echo ""
echo "Usage with uvx:"
echo "  uvx --from ./dist/novareel_mcp-1.0.0-py3-none-any.whl novareel-mcp-server --help"
echo ""
echo "Or install locally:"
echo "  pip install ./dist/novareel_mcp-1.0.0-py3-none-any.whl"

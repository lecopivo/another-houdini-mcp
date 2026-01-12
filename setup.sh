#!/bin/bash
# Setup script for Houdini MCP
# Automatically detects Houdini installation and configures Claude Code

echo "🔧 Setting up Houdini MCP Server..."

# Get the absolute path to this script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_PATH="$SCRIPT_DIR/houdini_mcp_server.py"

echo "📂 Project directory: $SCRIPT_DIR"

# Detect Houdini Python
if [ -d "/Applications/Houdini/Current" ]; then
    HOUDINI_PYTHON="/Applications/Houdini/Current/Frameworks/Python.framework/Versions/Current/bin/python3"
    echo "🐍 Found Houdini Python: $HOUDINI_PYTHON"
elif [ -d "/opt/hfs/current" ]; then
    # Linux path
    HOUDINI_PYTHON="/opt/hfs/current/python/bin/python3"
    echo "🐍 Found Houdini Python: $HOUDINI_PYTHON"
else
    echo "❌ Could not find Houdini installation"
    echo "Please set HOUDINI_PYTHON environment variable to your Houdini Python path"
    exit 1
fi

# Verify Python exists
if [ ! -f "$HOUDINI_PYTHON" ]; then
    echo "❌ Houdini Python not found at: $HOUDINI_PYTHON"
    echo "Please check your Houdini installation"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$("$HOUDINI_PYTHON" --version 2>&1)
echo "Python version: $PYTHON_VERSION"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
"$HOUDINI_PYTHON" -m pip install -r "$SCRIPT_DIR/requirements.txt" --user

# Check if Claude Code CLI is available
if ! command -v claude &> /dev/null; then
    echo ""
    echo "⚠️  Claude Code CLI not found"
    echo "Please install Claude Code from: https://claude.com/claude-code"
    exit 1
fi

# Add to Claude Code
echo ""
echo "🤖 Adding Houdini MCP to Claude Code..."
claude mcp add houdini --transport stdio -- "$HOUDINI_PYTHON" "$SERVER_PATH"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Open Houdini"
echo "2. Go to Windows → Python Shell"
echo "3. Run the following commands:"
echo ""
echo "   import sys"
echo "   sys.path.append('$SCRIPT_DIR')"
echo "   from houdini_plugin import HoudiniMCPServer"
echo "   server = HoudiniMCPServer()"
echo "   server.start()"
echo ""
echo "4. Start using Claude Code to control Houdini!"
echo ""
echo "Verify installation:"
echo "  claude mcp list"
echo "  claude mcp get houdini"
echo ""

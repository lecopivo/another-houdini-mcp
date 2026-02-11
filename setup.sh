#!/bin/bash
# Setup script for Houdini MCP
# Automatically detects Houdini installation and configures Claude Code

echo "🔧 Setting up Houdini MCP Server..."

# Get the absolute path to this script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_PATH="$SCRIPT_DIR/houdini_mcp_server.py"

echo "📂 Project directory: $SCRIPT_DIR"

# Detect Houdini Python
detect_houdini_python() {
    # 1. Check if HOUDINI_PYTHON is already set
    if [ -n "$HOUDINI_PYTHON" ] && [ -f "$HOUDINI_PYTHON" ]; then
        echo "🐍 Using HOUDINI_PYTHON from environment: $HOUDINI_PYTHON"
        return 0
    fi

    # 2. Try to find hython in PATH
    if command -v hython &> /dev/null; then
        HOUDINI_PYTHON=$(command -v hython)
        echo "🐍 Found hython in PATH: $HOUDINI_PYTHON"
        return 0
    fi

    # 3. Check macOS paths
    if [ "$(uname)" = "Darwin" ]; then
        # Check for Houdini Current symlink
        if [ -d "/Applications/Houdini/Current" ]; then
            HOUDINI_PYTHON="/Applications/Houdini/Current/Frameworks/Python.framework/Versions/Current/bin/python3"
            if [ -f "$HOUDINI_PYTHON" ]; then
                echo "🐍 Found Houdini Python (macOS): $HOUDINI_PYTHON"
                return 0
            fi
        fi

        # Check all Houdini versions in /Applications/Houdini/
        for version_dir in /Applications/Houdini/Houdini*/; do
            if [ -d "$version_dir" ]; then
                HOUDINI_PYTHON="$version_dir/Frameworks/Python.framework/Versions/Current/bin/python3"
                if [ -f "$HOUDINI_PYTHON" ]; then
                    echo "🐍 Found Houdini Python (macOS): $HOUDINI_PYTHON"
                    return 0
                fi
            fi
        done
    fi

    # 4. Check Linux paths
    if [ "$(uname)" = "Linux" ]; then
        # Check for HFS environment variable (standard Houdini setup)
        if [ -n "$HFS" ] && [ -d "$HFS" ]; then
            HOUDINI_PYTHON="$HFS/python/bin/python3"
            if [ -f "$HOUDINI_PYTHON" ]; then
                echo "🐍 Found Houdini Python via HFS: $HOUDINI_PYTHON"
                return 0
            fi
        fi

        # Check all versions in /opt/hfs*
        for version_dir in /opt/hfs*; do
            if [ -d "$version_dir" ]; then
                HOUDINI_PYTHON="$version_dir/python/bin/python3"
                if [ -f "$HOUDINI_PYTHON" ]; then
                    echo "🐍 Found Houdini Python (Linux): $HOUDINI_PYTHON"
                    return 0
                fi
            fi
        done

        # Check /opt/houdini* as well
        for version_dir in /opt/houdini*; do
            if [ -d "$version_dir" ]; then
                HOUDINI_PYTHON="$version_dir/python/bin/python3"
                if [ -f "$HOUDINI_PYTHON" ]; then
                    echo "🐍 Found Houdini Python (Linux alt): $HOUDINI_PYTHON"
                    return 0
                fi
            fi
        done

        # Check user home directory installations
        if [ -d "$HOME/houdini" ]; then
            for version_dir in "$HOME/houdini"*; do
                if [ -d "$version_dir" ]; then
                    HOUDINI_PYTHON="$version_dir/python/bin/python3"
                    if [ -f "$HOUDINI_PYTHON" ]; then
                        echo "🐍 Found Houdini Python (user install): $HOUDINI_PYTHON"
                        return 0
                    fi
                fi
            done
        fi
    fi

    # 5. Windows/WSL paths
    if [ "$(uname -o 2>/dev/null)" = "Msys" ] || [ -n "$WINDIR" ]; then
        for version_dir in /c/Program\ Files/Side\ Effects\ Software/Houdini*/; do
            if [ -d "$version_dir" ]; then
                HOUDINI_PYTHON="$version_dir/python39/python3.exe"
                if [ -f "$HOUDINI_PYTHON" ]; then
                    echo "🐍 Found Houdini Python (Windows): $HOUDINI_PYTHON"
                    return 0
                fi
            fi
        done
    fi

    return 1
}

# Run detection
if ! detect_houdini_python; then
    echo ""
    echo "❌ Could not find Houdini installation"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Make sure Houdini is installed"
    echo "  2. Try sourcing Houdini environment:"
    echo "     source /opt/hfsXX.X/houdini_setup (Linux)"
    echo "     source /Applications/Houdini/HoudiniXX.X/Frameworks/Houdini.framework/Versions/Current/Resources/houdini_setup (macOS)"
    echo "  3. Set HOUDINI_PYTHON manually:"
    echo "     export HOUDINI_PYTHON=/path/to/houdini/python/bin/python3"
    echo "     ./setup.sh"
    echo ""
    echo "Common paths:"
    echo "  Linux:  /opt/hfs20.5/python/bin/python3"
    echo "  macOS:  /Applications/Houdini/Current/Frameworks/Python.framework/Versions/Current/bin/python3"
    echo "  Windows: C:/Program Files/Side Effects Software/Houdini 20.5/python39/python3.exe"
    echo ""
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

# Detect Houdini installation directory
detect_houdini_dir() {
    # Get directory from HOUDINI_PYTHON path
    local python_path="$HOUDINI_PYTHON"

    # For HFS environment variable
    if [ -n "$HFS" ]; then
        echo "$HFS"
        return 0
    fi

    # Extract from python path
    if [[ "$python_path" == *"/hfs"* ]]; then
        # Linux: /opt/hfs20.5/python/bin/python3 -> /opt/hfs20.5
        echo "$python_path" | sed -E 's|(.*hfs[^/]*)/.*|\1|'
        return 0
    elif [[ "$python_path" == *"Houdini"* ]]; then
        # macOS: /Applications/Houdini/Houdini20.5/... -> find houdini dir
        echo "$python_path" | sed -E 's|(.*Houdini[^/]*)/.*|\1|'
        return 0
    elif [[ "$python_path" == *"Side Effects Software"* ]]; then
        # Windows: C:/Program Files/Side Effects Software/Houdini 20.5/...
        echo "$python_path" | sed -E 's|(.*Houdini[^/]*)/.*|\1|'
        return 0
    fi

    return 1
}

# Check for documentation
HOUDINI_DIR=$(detect_houdini_dir)

if [ -n "$HOUDINI_DIR" ]; then
    echo ""
    echo "📚 Checking for Houdini documentation..."
    echo "Houdini directory: $HOUDINI_DIR"

    NODES_ZIP="$HOUDINI_DIR/houdini/help/nodes.zip"
    HOM_ZIP="$HOUDINI_DIR/houdini/help/hom.zip"

    if [ -f "$NODES_ZIP" ] || [ -f "$HOM_ZIP" ]; then
        echo ""
        echo "📖 Houdini documentation archives found!"
        echo ""

        if [ -f "$NODES_ZIP" ]; then
            echo "  ✓ nodes.zip: $NODES_ZIP"
        fi
        if [ -f "$HOM_ZIP" ]; then
            echo "  ✓ hom.zip: $HOM_ZIP"
        fi

        echo ""
        echo "Would you like to unpack the documentation? (y/n)"
        read -r response

        if [[ "$response" =~ ^[Yy]$ ]]; then
            echo ""
            echo "📦 Unpacking documentation to $SCRIPT_DIR/help..."

            # Create help directory
            mkdir -p "$SCRIPT_DIR/help"

            # Unpack nodes.zip
            if [ -f "$NODES_ZIP" ]; then
                echo "Unpacking nodes documentation..."
                unzip -q -o "$NODES_ZIP" -d "$SCRIPT_DIR/help"
                echo "  ✓ Nodes documentation unpacked"
            fi

            # Unpack hom.zip
            if [ -f "$HOM_ZIP" ]; then
                echo "Unpacking Python HOM documentation..."
                unzip -q -o "$HOM_ZIP" -d "$SCRIPT_DIR/help"
                echo "  ✓ HOM documentation unpacked"
            fi

            echo ""
            echo "✅ Documentation unpacked successfully!"
        else
            echo ""
            echo "ℹ️  Skipping documentation unpacking."
            echo "   You can unpack manually later with these commands:"
            echo ""
            if [ -f "$NODES_ZIP" ]; then
                echo "   unzip -o \"$NODES_ZIP\" -d \"$SCRIPT_DIR/help\""
            fi
            if [ -f "$HOM_ZIP" ]; then
                echo "   unzip -o \"$HOM_ZIP\" -d \"$SCRIPT_DIR/help\""
            fi
            echo ""
        fi
    else
        echo "⚠️  Documentation archives not found at expected locations:"
        echo "   Expected: $HOUDINI_DIR/houdini/help/nodes.zip"
        echo "   Expected: $HOUDINI_DIR/houdini/help/hom.zip"
        echo ""
        echo "   You can manually unpack if they're in a different location:"
        echo "   unzip -o /path/to/nodes.zip -d \"$SCRIPT_DIR/help\""
        echo "   unzip -o /path/to/hom.zip -d \"$SCRIPT_DIR/help\""
    fi
fi

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

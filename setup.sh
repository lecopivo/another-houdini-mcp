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

    HOUDINI_HELP_DIR="$HOUDINI_DIR/houdini/help"

    if [ -d "$HOUDINI_HELP_DIR" ]; then
        echo ""
        echo "📖 Houdini help directory found!"
        echo ""
        echo "  ✓ help directory: $HOUDINI_HELP_DIR"
        echo "  Excluding from copy: videos/, files/, images.zip"

        echo ""
        echo "Would you like to copy and unpack the documentation? (y/n)"
        read -r response

        if [[ "$response" =~ ^[Yy]$ ]]; then
            echo ""
            echo "📦 Copying documentation to $SCRIPT_DIR/help..."

            # Create help directory
            mkdir -p "$SCRIPT_DIR/help"

            # Copy help directory while excluding large/non-essential content
            if command -v rsync &> /dev/null; then
                rsync -a \
                    --exclude 'videos/' \
                    --exclude 'files/' \
                    --exclude 'images.zip' \
                    "$HOUDINI_HELP_DIR/" "$SCRIPT_DIR/help/"
            else
                cp -a "$HOUDINI_HELP_DIR/." "$SCRIPT_DIR/help/"
                rm -rf "$SCRIPT_DIR/help/videos" "$SCRIPT_DIR/help/examples" "$SCRIPT_DIR/help/files"
                rm -f "$SCRIPT_DIR/help/images.zip"
            fi

            echo "  ✓ Help directory copied"

            # Unpack all top-level zip files in help/
            ZIP_COUNT=0
            for zip_file in "$SCRIPT_DIR/help"/*.zip; do
                if [ -f "$zip_file" ]; then
                    zip_name="$(basename "$zip_file" .zip)"
                    zip_target_dir="$SCRIPT_DIR/help/$zip_name"
                    mkdir -p "$zip_target_dir"
                    echo "Unpacking $(basename "$zip_file") into $zip_name/..."
                    unzip -q -o "$zip_file" -d "$zip_target_dir"
                    rm -f "$zip_file"
                    ZIP_COUNT=$((ZIP_COUNT + 1))
                fi
            done

            if [ "$ZIP_COUNT" -gt 0 ]; then
                echo "  ✓ Unpacked and removed $ZIP_COUNT zip file(s)"
            else
                echo "  ℹ️  No zip files found in $SCRIPT_DIR/help"
            fi

            echo ""
            echo "✅ Documentation copied and unpacked successfully!"
        else
            echo ""
            echo "ℹ️  Skipping documentation copy/unpack."
            echo "   You can do it manually later with these commands:"
            echo ""
            echo "   mkdir -p \"$SCRIPT_DIR/help\""
            echo "   rsync -a --exclude 'videos/' --exclude 'examples/' --exclude 'files/' --exclude 'images.zip' \"$HOUDINI_HELP_DIR/\" \"$SCRIPT_DIR/help/\""
            echo "   for z in \"$SCRIPT_DIR/help\"/*.zip; do [ -f \"$z\" ] && d=\"$SCRIPT_DIR/help/$(basename \"$z\" .zip)\" && mkdir -p \"$d\" && unzip -o \"$z\" -d \"$d\"; done"
            echo ""
        fi
    else
        echo "⚠️  Houdini help directory not found at expected location:"
        echo "   Expected: $HOUDINI_DIR/houdini/help"
        echo ""
        echo "   You can manually copy/unpack if it's in a different location:"
        echo "   rsync -a --exclude 'videos/' --exclude 'examples/' --exclude 'files/' --exclude 'images.zip' /path/to/help/ \"$SCRIPT_DIR/help/\""
        echo "   for z in \"$SCRIPT_DIR/help\"/*.zip; do [ -f \"$z\" ] && d=\"$SCRIPT_DIR/help/$(basename \"$z\" .zip)\" && mkdir -p \"$d\" && unzip -o \"$z\" -d \"$d\"; done"
    fi
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
PIP_INSTALL_LOG="$(mktemp)"
if "$HOUDINI_PYTHON" -m pip install -r "$SCRIPT_DIR/requirements.txt" --user --disable-pip-version-check >"$PIP_INSTALL_LOG" 2>&1; then
    echo "✅ Python dependencies are up to date."
else
    echo "❌ Failed to install Python dependencies"
    echo ""
    echo "Pip output:"
    cat "$PIP_INSTALL_LOG"
    rm -f "$PIP_INSTALL_LOG"
    exit 1
fi
rm -f "$PIP_INSTALL_LOG"

# Prompt helper
prompt_yes_no() {
    local prompt="$1"
    local response
    while true; do
        echo "$prompt (y/n)"
        read -r response
        case "$response" in
            [Yy]|[Yy][Ee][Ss]) return 0 ;;
            [Nn]|[Nn][Oo]) return 1 ;;
            *) echo "Please answer y or n." ;;
        esac
    done
}

# Install optional Houdini shelf tool
install_shelf_tool() {
    local script_dir="$1"
    local houdini_dir="$2"
    shift 2
    local client_pairs=("$@")
    local version
    local base
    local pref_dir
    local shelf_dir
    local shelf_file
    local installed_paths=()
    local candidate_pref_dirs=()

    # Prefer explicit Houdini user pref dir if present
    if [ -n "$HOUDINI_USER_PREF_DIR" ]; then
        candidate_pref_dirs+=("$HOUDINI_USER_PREF_DIR")
    fi

    # Try to infer version-specific pref dir from Houdini install path
    base="$(basename "$houdini_dir")"
    if [[ "$base" =~ ([0-9]+\.[0-9]+) ]]; then
        version="${BASH_REMATCH[1]}"
        candidate_pref_dirs+=("$HOME/houdini$version")
    fi

    # Include existing Houdini preference dirs
    for pref_dir in "$HOME"/houdini*; do
        if [ -d "$pref_dir" ]; then
            candidate_pref_dirs+=("$pref_dir")
        fi
    done

    # If still nothing, fall back to generic home location
    if [ ${#candidate_pref_dirs[@]} -eq 0 ]; then
        candidate_pref_dirs+=("$HOME/houdini")
    fi

    for pref_dir in "${candidate_pref_dirs[@]}"; do
        shelf_dir="$pref_dir/toolbar"
        shelf_file="$shelf_dir/ai_chat.shelf"

        mkdir -p "$shelf_dir"
        rm -f "$shelf_dir/mcp.shelf"
        rm -f "$shelf_dir/ai.shelf"

        cat > "$shelf_file" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<shelfDocument>
  <toolshelf name="ai_chat" label="AI Chat">
    <memberTool name="Restart Server"/>
EOF

        for pair in "${client_pairs[@]}"; do
            local client_cmd
            local client_title
            local client_exec
            IFS=':' read -r client_cmd client_title client_exec <<< "$pair"
            cat >> "$shelf_file" <<EOF
    <memberTool name="Start $client_title"/>
EOF
        done

        cat >> "$shelf_file" <<EOF
  </toolshelf>

  <tool name="Restart Server" label="Restart Server" icon="PLASMA_App">
    <script scriptType="python"><![CDATA[import sys
import time
import __main__

import hou

sys.path.append('$script_dir')
from houdini_plugin import HoudiniMCPServer

def stop_server_instance(instance):
    if instance is None:
        return
    stopped = False
    try:
        instance.stop()
        stopped = True
    except Exception:
        pass

    if not stopped:
        try:
            instance.running = False
        except Exception:
            pass
        try:
            if getattr(instance, 'socket', None) is not None:
                instance.socket.close()
        except Exception:
            pass

seen = set()
candidates = [
    getattr(hou.session, 'houdini_mcp_server', None),
    getattr(hou.session, 'server', None),
    getattr(__main__, 'server', None),
    getattr(HoudiniMCPServer, '_active_server', None),
]

for instance in candidates:
    if instance is None:
        continue
    key = id(instance)
    if key in seen:
        continue
    seen.add(key)
    stop_server_instance(instance)

time.sleep(0.2)

server = HoudiniMCPServer()
server.start()
hou.session.houdini_mcp_server = server
try:
    hou.session.server = server
except Exception:
    pass
try:
    __main__.server = server
except Exception:
    pass
]]></script>
  </tool>
EOF

        for pair in "${client_pairs[@]}"; do
            local client_cmd
            local client_title
            local client_exec
            IFS=':' read -r client_cmd client_title client_exec <<< "$pair"
            local client_icon="MISC_python"

            case "$client_cmd" in
                claude)
                    if [ -f "$script_dir/icons/claude-icon.png" ]; then
                        client_icon="$script_dir/icons/claude-icon.png"
                    fi
                    ;;
                codex|openai)
                    if [ -f "$script_dir/icons/openai-icon.png" ]; then
                        client_icon="$script_dir/icons/openai-icon.png"
                    fi
                    ;;
                opencode)
                    if [ -f "$script_dir/icons/opencode.png" ]; then
                        client_icon="$script_dir/icons/opencode.png"
                    fi
                    ;;
                *)
                    if [ -f "$script_dir/icons/$client_cmd.png" ]; then
                        client_icon="$script_dir/icons/$client_cmd.png"
                    fi
                    ;;
            esac

            cat >> "$shelf_file" <<EOF

  <tool name="Start $client_title" label="$client_title" icon="$client_icon">
    <script scriptType="python"><![CDATA[import os
import platform
import shlex
import shutil
import subprocess
import time
import __main__

import hou

import sys
sys.path.append('$script_dir')
from houdini_plugin import HoudiniMCPServer

project_dir = '$script_dir'
client_cmd = '$client_cmd'
client_exec_path = '$client_exec'

project_dir = os.path.abspath(project_dir)
if not os.path.isdir(project_dir):
    message = f"Project directory not found: {project_dir}"
    try:
        hou.ui.displayMessage(message)
    except Exception:
        print(message)
    raise SystemExit(1)

def restart_server():
    def stop_server_instance(instance):
        if instance is None:
            return
        stopped = False
        try:
            instance.stop()
            stopped = True
        except Exception:
            pass

        if not stopped:
            try:
                instance.running = False
            except Exception:
                pass
            try:
                if getattr(instance, 'socket', None) is not None:
                    instance.socket.close()
            except Exception:
                pass

    existing = getattr(hou.session, 'houdini_mcp_server', None)
    active = getattr(HoudiniMCPServer, '_active_server', None)

    seen = set()
    candidates = [
        existing,
        getattr(hou.session, 'server', None),
        getattr(__main__, 'server', None),
        active,
    ]

    for instance in candidates:
        if instance is None:
            continue
        key = id(instance)
        if key in seen:
            continue
        seen.add(key)
        stop_server_instance(instance)

    time.sleep(0.2)

    server = HoudiniMCPServer()
    server.start()
    hou.session.houdini_mcp_server = server
    try:
        hou.session.server = server
    except Exception:
        pass
    try:
        __main__.server = server
    except Exception:
        pass

restart_server()

resolved_client = None
if client_exec_path and os.path.isfile(client_exec_path):
    resolved_client = client_exec_path
elif shutil.which(client_cmd):
    resolved_client = shutil.which(client_cmd)

if resolved_client is None:
    message = f"{client_cmd} not found in PATH"
    try:
        hou.ui.displayMessage(message)
    except Exception:
        print(message)
    raise SystemExit(1)

launch_script = os.path.join(project_dir, f".launch_{client_cmd}.sh")
with open(launch_script, "w", encoding="utf-8") as f:
    f.write("#!/usr/bin/env bash\n")
    f.write("set -e\n")
    f.write(f"cd {shlex.quote(project_dir)}\n")
    f.write(f"{shlex.quote(resolved_client)}\n")
    f.write("exec bash\n")
os.chmod(launch_script, 0o755)

system = platform.system()
launch_env = os.environ.copy()
launch_env.pop('PYTHONHOME', None)
launch_env.pop('PYTHONPATH', None)

launched = False
launch_errors = []

try:
    if system == 'Darwin':
        mac_cmd = f"bash {shlex.quote(launch_script)}"
        escaped = mac_cmd.replace('"', '\\"')
        applescript = f'tell application "Terminal"\\nactivate\\ndo script "{escaped}"\\nend tell'
        subprocess.Popen(['osascript', '-e', applescript], env=launch_env)
        launched = True
    elif system == 'Windows':
        subprocess.Popen(['cmd', '/k', f'cd /d "{project_dir}" && {client_cmd}'], env=launch_env)
        launched = True
    else:
        linux_launchers = [
            ['/usr/bin/gnome-terminal', '--disable-factory', '--', 'bash', launch_script],
            ['x-terminal-emulator', '-e', 'bash', launch_script],
            ['gnome-terminal', '--', 'bash', launch_script],
            ['konsole', '-e', 'bash', launch_script],
            ['xfce4-terminal', '--hold', '-e', f'bash {shlex.quote(launch_script)}'],
            ['alacritty', '-e', 'bash', launch_script],
            ['kitty', 'bash', launch_script],
            ['xterm', '-hold', '-e', 'bash', launch_script],
            ['terminator', '-x', 'bash', launch_script],
        ]

        for launch_cmd in linux_launchers:
            if shutil.which(launch_cmd[0]):
                try:
                    subprocess.Popen(launch_cmd, cwd=project_dir, start_new_session=True, env=launch_env)
                    launched = True
                    break
                except Exception as e:
                    launch_errors.append(f"{launch_cmd[0]}: {e}")
except Exception as e:
    launch_errors.append(str(e))
    launched = False

if not launched:
    details = ""
    if launch_errors:
        details = "\n\nLaunch errors:\n" + "\n".join(launch_errors)
    try:
        hou.ui.displayMessage(
            f"Could not open a terminal automatically.\nRun manually:\ncd {project_dir} && {client_cmd}{details}"
        )
    except Exception:
        print(f"Could not open a terminal automatically. Run manually: cd {project_dir} && {client_cmd}{details}")
]]></script>
  </tool>
EOF
        done

        cat >> "$shelf_file" <<EOF
</shelfDocument>
EOF

        installed_paths+=("$shelf_file")
    done

    if [ ${#installed_paths[@]} -gt 0 ]; then
        echo ""
        echo "🧰 Installed AI Chat shelf tools to:"
        for path in "${installed_paths[@]}"; do
            echo "  • $path"
        done
        echo ""
        echo "   Includes: Restart Server + client launcher tools."
        echo "   Restart Houdini to load updated shelf definitions."
    fi
}

# Detect available MCP clients
AVAILABLE_AGENTS=()
AVAILABLE_AGENT_TITLES=()
AVAILABLE_AGENT_EXECS=()
DETECTED_CLIENTS=()
DETECTED_CLIENT_TITLES=()
DETECTED_CLIENT_EXECS=()
DETECTED_BUT_UNSUPPORTED=()
INSTALLED_AGENTS=()
FAILED_AGENTS=()

resolve_client_executable() {
    local agent="$1"
    local exe_path

    if exe_path="$(command -v "$agent" 2>/dev/null)" && [ -n "$exe_path" ]; then
        echo "$exe_path"
        return 0
    fi

    if [ "$agent" = "opencode" ] && command -v whereis &> /dev/null; then
        local whereis_output token
        whereis_output="$(whereis "$agent" 2>/dev/null)"
        for token in $whereis_output; do
            if [[ "$token" == *":" ]]; then
                continue
            fi
            if [ -x "$token" ] && [ ! -d "$token" ]; then
                echo "$token"
                return 0
            fi
        done
    fi

    return 1
}

# command:title pairs for known AI client CLIs
CLIENT_CANDIDATES=(
    "claude:Claude Code"
    "codex:Codex"
    "opencode:OpenCode"
    "gemini:Gemini CLI"
    "qwen:Qwen Code"
    "cursor:Cursor"
    "cursor-agent:Cursor Agent"
    "windsurf:Windsurf"
)

for candidate in "${CLIENT_CANDIDATES[@]}"; do
    agent="${candidate%%:*}"
    agent_title="${candidate#*:}"
    agent_exec=""

    if agent_exec="$(resolve_client_executable "$agent")"; then
        DETECTED_CLIENTS+=("$agent")
        DETECTED_CLIENT_TITLES+=("$agent_title")
        DETECTED_CLIENT_EXECS+=("$agent_exec")

        if "$agent_exec" mcp --help &> /dev/null; then
            AVAILABLE_AGENTS+=("$agent")
            AVAILABLE_AGENT_TITLES+=("$agent_title")
            AVAILABLE_AGENT_EXECS+=("$agent_exec")
        else
            DETECTED_BUT_UNSUPPORTED+=("$agent")
        fi
    fi
done

SHELF_CLIENT_PAIRS=()
for i in "${!DETECTED_CLIENTS[@]}"; do
    SHELF_CLIENT_PAIRS+=("${DETECTED_CLIENTS[$i]}:${DETECTED_CLIENT_TITLES[$i]}:${DETECTED_CLIENT_EXECS[$i]}")
done

if prompt_yes_no "Install Houdini shelf tool (AI Chat tab with Restart Server and client launchers)?"; then
    install_shelf_tool "$SCRIPT_DIR" "$HOUDINI_DIR" "${SHELF_CLIENT_PAIRS[@]}"
else
    echo "ℹ️  Skipped shelf tool installation."
fi

# Install Houdini MCP into OpenCode by writing project config
install_opencode_mcp() {
    local script_dir="$1"
    local houdini_python="$2"
    local server_path="$3"
    local config_path="$script_dir/opencode.json"
    local python_bin

    if command -v python3 &> /dev/null; then
        python_bin="python3"
    else
        python_bin="$houdini_python"
    fi

    "$python_bin" - "$config_path" "$houdini_python" "$server_path" <<'PY'
import json
import os
import sys

config_path, houdini_python, server_path = sys.argv[1:]

if os.path.exists(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {}

if not isinstance(data, dict):
    raise SystemExit(f"Invalid OpenCode config format at {config_path}")

if "$schema" not in data:
    data["$schema"] = "https://opencode.ai/config.json"

mcp = data.get("mcp")
if not isinstance(mcp, dict):
    mcp = {}
    data["mcp"] = mcp

mcp["houdini"] = {
    "type": "local",
    "command": [houdini_python, server_path],
    "enabled": True,
}

with open(config_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print(config_path)
PY
}

# Install Houdini MCP into a specific client
install_mcp_for_agent() {
    local agent="$1"
    local agent_exec="$2"
    local output

    case "$agent" in
        claude)
            output=$("$agent_exec" mcp add houdini --transport stdio -- "$HOUDINI_PYTHON" "$SERVER_PATH" 2>&1)
            ;;
        codex)
            output=$("$agent_exec" mcp add houdini -- "$HOUDINI_PYTHON" "$SERVER_PATH" 2>&1)
            ;;
        opencode)
            output=$(install_opencode_mcp "$SCRIPT_DIR" "$HOUDINI_PYTHON" "$SERVER_PATH" 2>&1)
            ;;
        *)
            output=$("$agent_exec" mcp add houdini -- "$HOUDINI_PYTHON" "$SERVER_PATH" 2>&1)
            ;;
    esac
    local status=$?

    if [ -n "$output" ]; then
        echo "$output"
    fi

    if [ $status -eq 0 ]; then
        return 0
    fi

    # Treat existing configuration as success for CLIs that fail on duplicates
    if [[ "$output" == *"already exists"* ]]; then
        echo "ℹ️  MCP server already configured for $agent."
        return 0
    fi

    return 1
}

if [ ${#AVAILABLE_AGENTS[@]} -eq 0 ]; then
    echo ""
    echo "⚠️  No supported MCP client CLI found in PATH."
    echo "Detected and checked these client commands:"
    echo "  • claude"
    echo "  • codex"
    echo "  • opencode"
    echo "  • gemini"
    echo "  • qwen"
    echo "  • cursor"
    echo "  • cursor-agent"
    echo "  • windsurf"

    if [ ${#DETECTED_BUT_UNSUPPORTED[@]} -gt 0 ]; then
        echo ""
        echo "Found CLIs without MCP subcommands: ${DETECTED_BUT_UNSUPPORTED[*]}"
    fi
else
    echo ""
    echo "🧭 Detected MCP-capable AI client CLIs:"
    for i in "${!AVAILABLE_AGENTS[@]}"; do
        echo "  • ${AVAILABLE_AGENT_TITLES[$i]} (command: ${AVAILABLE_AGENTS[$i]}, exec: ${AVAILABLE_AGENT_EXECS[$i]})"
    done

    if [ ${#DETECTED_BUT_UNSUPPORTED[@]} -gt 0 ]; then
        echo ""
        echo "ℹ️  Installed but missing MCP support: ${DETECTED_BUT_UNSUPPORTED[*]}"
    fi

    for i in "${!AVAILABLE_AGENTS[@]}"; do
        agent="${AVAILABLE_AGENTS[$i]}"
        agent_exec="${AVAILABLE_AGENT_EXECS[$i]}"
        AGENT_TITLE="${AVAILABLE_AGENT_TITLES[$i]}"
        if prompt_yes_no "Install Houdini MCP into $AGENT_TITLE now?"; then
            echo "🤖 Adding Houdini MCP to $AGENT_TITLE..."
            if install_mcp_for_agent "$agent" "$agent_exec"; then
                INSTALLED_AGENTS+=("$agent")
            else
                echo "❌ Failed to add MCP to $AGENT_TITLE"
                FAILED_AGENTS+=("$agent")
            fi
        else
            echo "ℹ️  Skipped MCP install for $AGENT_TITLE."
        fi
    done
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Open Houdini"
echo "2. In the AI Chat shelf tab, click 'Restart Server'"
echo "3. In the AI Chat shelf tab, click your client launcher (Claude/Codex/OpenCode/etc.)"
echo ""
echo "Manual fallback (if shelf tools are not available):"
echo "  • Go to Windows → Python Shell and run:"
echo ""
echo "      import sys"
echo "      sys.path.append('$SCRIPT_DIR')"
echo "      from houdini_plugin import HoudiniMCPServer"
echo "      server = HoudiniMCPServer()"
echo "      server.start()"
echo ""
echo "  • Then start your MCP client from a terminal in: $SCRIPT_DIR"
echo ""
if [ ${#INSTALLED_AGENTS[@]} -gt 0 ]; then
    echo "Verify installation (for each client you installed):"
    for agent in "${INSTALLED_AGENTS[@]}"; do
        echo "  $agent mcp list"
        if [ "$agent" = "claude" ] || [ "$agent" = "codex" ]; then
            echo "  $agent mcp get houdini"
        fi
    done
elif [ ${#AVAILABLE_AGENTS[@]} -gt 0 ]; then
    echo "No MCP client installations were selected."
fi

if [ ${#FAILED_AGENTS[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  MCP install failed for: ${FAILED_AGENTS[*]}"
fi
echo ""

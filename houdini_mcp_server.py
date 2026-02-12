#!/usr/bin/env python3
"""
Houdini MCP Server
Connects Claude Code to Houdini via the Model Context Protocol

Run with: python houdini_mcp_server.py
Or configure in Claude Code settings

IMPORTANT FOR AI AGENTS:
When exploring a Houdini scene, ALWAYS start with get_folder_info() to understand
the scene structure. Start with get_folder_info("/obj") or get_folder_info("/")
and navigate from there. This is the primary entry point for scene exploration.
"""

import json
import socket
import sys
from typing import Any, Dict, Optional

from tool_modules.registry import register_mcp_tools

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("ERROR: MCP not installed. Run: pip install fastmcp", file=sys.stderr)
    sys.exit(1)

# Initialize MCP server
mcp = FastMCP(
    "houdini",
    instructions="""
    When exploring a Houdini scene:
    1. ALWAYS start with get_folder_info("/obj") to see the scene structure
    2. Navigate deeper by calling get_folder_info() on specific nodes (e.g., "/obj/geo1")
    3. Use get_node_info() only when you need details about a specific node
    4. Avoid get_scene_info() for complex scenes - it returns ALL nodes recursively

    The get_folder_info() tool is your PRIMARY ENTRY POINT for understanding scenes.
    """
)

_real_mcp_tool_decorator = mcp.tool

# Configuration
HOUDINI_HOST = "localhost"
HOUDINI_PORT = 9876
houdini_socket: Optional[socket.socket] = None

def connect_to_houdini():
    """Connect to Houdini plugin"""
    global houdini_socket

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOUDINI_HOST, HOUDINI_PORT))
        houdini_socket = sock
        return sock
    except ConnectionRefusedError:
        raise RuntimeError(
            f"Cannot connect to Houdini on {HOUDINI_HOST}:{HOUDINI_PORT}. "
            "Make sure Houdini is running with the MCP plugin loaded."
        )

def send_command(command: Dict[str, Any]) -> Dict[str, Any]:
    """Send command to Houdini"""
    global houdini_socket

    if not houdini_socket:
        houdini_socket = connect_to_houdini()

    try:
        # Send command with length prefix
        command_json = json.dumps(command)
        message = command_json.encode('utf-8')
        # Send length as 4-byte integer, then the message
        length = len(message)
        houdini_socket.send(length.to_bytes(4, byteorder='big'))
        houdini_socket.send(message)

        # Receive response (read length first, then full message)
        length_bytes = houdini_socket.recv(4)
        if not length_bytes:
            raise RuntimeError("Connection closed by Houdini")

        response_length = int.from_bytes(length_bytes, byteorder='big')

        # Read the full response in chunks
        response_data = b''
        while len(response_data) < response_length:
            chunk = houdini_socket.recv(min(4096, response_length - len(response_data)))
            if not chunk:
                raise RuntimeError("Connection closed while reading response")
            response_data += chunk

        response = json.loads(response_data.decode('utf-8'))

        if response.get("status") == "error":
            raise RuntimeError(response.get("error", "Unknown error"))

        return response.get("result", {})

    except (ConnectionRefusedError, BrokenPipeError):
        houdini_socket = None
        raise RuntimeError("Lost connection to Houdini")

# ============================================================================
# MCP Tools
# ============================================================================

from tool_modules.legacy_bridge_functions import get_legacy_bridge_functions
# Register all tools via per-tool modules using legacy wrappers where needed.
register_mcp_tools(
    mcp,
    send_command,
    legacy_bridge_functions=get_legacy_bridge_functions(send_command),
    tool_decorator=_real_mcp_tool_decorator,
)

# ============================================================================
# Server Entry Point
# ============================================================================

if __name__ == "__main__":
    print("Starting Houdini MCP Server...", file=sys.stderr)
    print("Connecting to Houdini on localhost:9876...", file=sys.stderr)
    mcp.run(transport="stdio")

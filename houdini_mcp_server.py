#!/usr/bin/env python3
"""
Houdini MCP Server
Connects Claude Code to Houdini via the Model Context Protocol

Run with: python houdini_mcp_server.py
Or configure in Claude Code settings
"""

import json
import socket
import sys
from typing import Any, Dict, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("ERROR: MCP not installed. Run: pip install fastmcp", file=sys.stderr)
    sys.exit(1)

# Initialize MCP server
mcp = FastMCP("houdini")

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
        # Send command
        command_json = json.dumps(command)
        houdini_socket.send(command_json.encode('utf-8'))

        # Receive response
        response_data = houdini_socket.recv(4096).decode('utf-8')
        response = json.loads(response_data)

        if response.get("status") == "error":
            raise RuntimeError(response.get("error", "Unknown error"))

        return response.get("result", {})

    except (ConnectionRefusedError, BrokenPipeError):
        houdini_socket = None
        raise RuntimeError("Lost connection to Houdini")

# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool()
def create_node(node_type: str, node_name: str = "", parent: str = "/obj") -> str:
    """
    Create a new node in Houdini

    Args:
        node_type: Type of node (e.g., 'geo', 'null', 'light', 'camera')
        node_name: Optional name for the node
        parent: Parent path (default: /obj)

    Returns:
        Path to the created node
    """
    result = send_command({
        "type": "create_node",
        "params": {
            "node_type": node_type,
            "node_name": node_name,
            "parent": parent
        }
    })
    return f"✅ Created: {result['node_path']} (type: {result['node_type']})"

@mcp.tool()
def delete_node(node_path: str) -> str:
    """
    Delete a node from Houdini

    Args:
        node_path: Full path to the node (e.g., '/obj/geo1')

    Returns:
        Confirmation message
    """
    result = send_command({
        "type": "delete_node",
        "params": {"node_path": node_path}
    })
    return result.get("message", "Node deleted")

@mcp.tool()
def connect_nodes(source_path: str, dest_path: str, source_index: int = 0, dest_index: int = 0) -> str:
    """
    Connect one node's output to another node's input

    Args:
        source_path: Source node path
        dest_path: Destination node path
        source_index: Output index (default: 0)
        dest_index: Input index (default: 0)

    Returns:
        Confirmation message
    """
    result = send_command({
        "type": "connect_nodes",
        "params": {
            "source_path": source_path,
            "dest_path": dest_path,
            "source_index": source_index,
            "dest_index": dest_index
        }
    })
    return result.get("message", "Nodes connected")

@mcp.tool()
def set_parameter(node_path: str, param_name: str, param_value: Any) -> str:
    """
    Set a parameter on a node

    Args:
        node_path: Path to node (e.g., '/obj/geo1')
        param_name: Parameter name (e.g., 'tx', 'ty', 'tz')
        param_value: Value to set

    Returns:
        Confirmation message
    """
    result = send_command({
        "type": "set_parameter",
        "params": {
            "node_path": node_path,
            "param_name": param_name,
            "param_value": param_value
        }
    })
    return result.get("message", "Parameter set")

@mcp.tool()
def get_scene_info() -> str:
    """
    Get information about the current Houdini scene

    Returns:
        Scene structure with all nodes
    """
    result = send_command({
        "type": "get_scene_info",
        "params": {}
    })

    output = f"📁 Scene: {result['file_path']}\n"
    output += f"📊 Total nodes: {result['num_nodes']}\n\n"
    output += "Nodes:\n"

    for node in result['nodes'][:20]:
        output += f"  • {node['path']} ({node['type']})\n"

    if result['num_nodes'] > 20:
        output += f"\n... and {result['num_nodes'] - 20} more nodes\n"

    return output

@mcp.tool()
def execute_hscript(code: str) -> str:
    """
    Execute HScript commands in Houdini

    WARNING: Use carefully - executes directly in Houdini

    Args:
        code: HScript code to execute

    Returns:
        Output from execution
    """
    result = send_command({
        "type": "execute_hscript",
        "params": {"code": code}
    })

    output = result.get("output", "")
    error = result.get("error", "")

    if error:
        return f"Output:\n{output}\n\nErrors:\n{error}"
    return output

# ============================================================================
# Server Entry Point
# ============================================================================

if __name__ == "__main__":
    print("Starting Houdini MCP Server...", file=sys.stderr)
    print("Connecting to Houdini on localhost:9876...", file=sys.stderr)
    mcp.run(transport="stdio")

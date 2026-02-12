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


def _noop_tool_decorator(*args, **kwargs):
    def _decorator(fn):
        return fn
    return _decorator


# Keep legacy tool functions defined but prevent immediate registration.
mcp.tool = _noop_tool_decorator

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
    Connect one node's output to another node's input with specific indices

    Args:
        source_path: Source node path
        dest_path: Destination node path
        source_index: Output index of source node (default: 0)
        dest_index: Input index of destination node (default: 0)

    Returns:
        Confirmation message with connection details
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
def remove_connection(dest_path: str, dest_index: int = 0) -> str:
    """
    Remove a specific connection from a node's input

    This removes the connection at a specific input index. If two nodes have multiple
    connections between them, you must specify the exact input index to disconnect.

    Args:
        dest_path: Destination node path
        dest_index: Input index to disconnect (default: 0)

    Returns:
        Confirmation message with details of the removed connection
    """
    result = send_command({
        "type": "remove_connection",
        "params": {
            "dest_path": dest_path,
            "dest_index": dest_index
        }
    })
    return result.get("message", "Connection removed")

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
    Get high-level information about the current Houdini scene

    WARNING: This returns ALL nodes in the scene (recursive), which can be
    overwhelming for complex scenes with hundreds or thousands of nodes.

    RECOMMENDED: Use get_folder_info() instead to explore the scene
    step-by-step, starting with get_folder_info("/obj") or get_folder_info("/").

    Only use this tool if you need a quick overview of a simple scene.

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
def get_node_info(node_path: str) -> str:
    """
    Get detailed information about a specific node

    Use this when you already know a node's path and want details about it.
    To discover nodes first, use get_folder_info() to explore the scene.

    Args:
        node_path: Full path to the node (e.g., '/obj/geo1')

    Returns:
        Node information including type, inputs, outputs, position, etc.
    """
    result = send_command({
        "type": "get_node_info",
        "params": {"node_path": node_path}
    })

    output = f"📦 Node: {result['path']}\n"
    output += f"   Type: {result['type']} ({result['type_category']})\n"
    output += f"   Inputs: {result['num_inputs']}, Outputs: {result['num_outputs']}\n"
    output += f"   Position: {result['position']}\n"
    output += f"   Locked: {result['is_locked']}, Template: {result['is_template']}\n"
    if result.get('comment'):
        output += f"   Comment: {result['comment']}\n"

    return output

@mcp.tool()
def get_node_parameters(node_path: str, show_defaults: bool = False) -> str:
    """
    Get all parameters and their current values from a node

    Args:
        node_path: Full path to the node (e.g., '/obj/geo1/sphere1')
        show_defaults: Whether to show default values (default: False)

    Returns:
        List of all parameters with their values
    """
    result = send_command({
        "type": "get_node_parameters",
        "params": {"node_path": node_path}
    })

    output = f"🔧 Parameters for {result['node_path']}\n"
    output += f"   Type: {result['node_type']}\n"
    output += f"   Total parameters: {result['num_parameters']}\n\n"

    # Group parameters by type for better readability
    for parm in result['parameters'][:50]:  # Limit to first 50 to avoid overwhelming output
        status = ""
        if parm.get('is_locked'):
            status += " 🔒"
        if parm.get('has_expression'):
            status += " 📐"

        output += f"   • {parm['name']} ({parm['type']}): {parm['value']}{status}\n"

        if show_defaults and parm.get('default_value') is not None:
            output += f"     Default: {parm['default_value']}\n"

    if result['num_parameters'] > 50:
        output += f"\n... and {result['num_parameters'] - 50} more parameters\n"

    return output

@mcp.tool()
def get_parameter_info(node_type: str, category: str = "Sop") -> str:
    """
    Get information about available parameters for a node type
    Useful for understanding what parameters you can set before creating a node

    Args:
        node_type: Type of node (e.g., 'sphere', 'box', 'tube')
        category: Node category - 'Sop' for geometry, 'Obj' for objects, 'Dop' for dynamics (default: 'Sop')

    Returns:
        Information about available parameters for this node type
    """
    result = send_command({
        "type": "get_parameter_info",
        "params": {
            "node_type": node_type,
            "category": category
        }
    })

    output = f"📘 Parameter Info for {result['node_type']} ({result['category']})\n"
    if result.get('description'):
        output += f"   Description: {result['description']}\n"
    output += f"   Total parameters: {result['num_parameters']}\n\n"

    # Show key parameters (limited to 30 for readability)
    for parm in result['parameters'][:30]:
        output += f"   • {parm['name']} ({parm['type']})\n"
        output += f"     Label: {parm['label']}\n"

        if parm.get('default_value'):
            output += f"     Default: {parm['default_value']}\n"

        if parm.get('help') and len(parm['help']) < 100:
            output += f"     Help: {parm['help']}\n"

        output += "\n"

    if result['num_parameters'] > 30:
        output += f"... and {result['num_parameters'] - 30} more parameters\n"

    return output

@mcp.tool()
def list_node_categories() -> str:
    """
    List all node categories (contexts) available in Houdini

    Returns a list of all contexts like Sop, Object, Dop, Chop, etc.

    Returns:
        List of all available node categories
    """
    result = send_command({
        "type": "list_node_categories",
        "params": {}
    })

    output = f"📂 Available Node Categories: {result['num_categories']}\n\n"

    for cat in result['categories']:
        output += f"  • {cat['name']}: {cat['label']}\n"

    return output

@mcp.tool()
def list_node_types(category: str = "Sop") -> str:
    """
    List all node types available in a specific category

    Args:
        category: Node category (e.g., 'Sop', 'Object', 'Dop', 'Chop', 'Cop2', 'Vop', 'Lop', 'Top')

    Returns:
        List of all node types in the category with descriptions
    """
    result = send_command({
        "type": "list_node_types",
        "params": {"category": category}
    })

    output = f"📦 Node Types in {result['category']}: {result['num_node_types']}\n\n"

    # Show first 50 node types
    for node_type in result['node_types'][:50]:
        desc = node_type['description'][:60] + "..." if len(node_type['description']) > 60 else node_type['description']
        output += f"  • {node_type['name']}: {desc}\n"

    if result['num_node_types'] > 50:
        output += f"\n... and {result['num_node_types'] - 50} more node types\n"
        output += "\nTip: Use get_node_documentation() to see detailed info for a specific node type\n"

    return output

@mcp.tool()
def get_node_documentation(node_type: str, category: str = "sop") -> str:
    """
    Get detailed documentation for a specific node type

    Reads documentation from the help/nodes directory containing official Houdini docs

    Args:
        node_type: Type of node (e.g., 'sphere', 'box', 'merge')
        category: Node category (default: 'sop')

    Returns:
        Full documentation text for the node type
    """
    result = send_command({
        "type": "get_node_documentation",
        "params": {
            "node_type": node_type,
            "category": category
        }
    })

    if result.get("error"):
        return f"❌ {result['error']}\n\nNode: {node_type}\nCategory: {category}"

    output = f"📖 Documentation for {node_type} ({category})\n"
    output += "="*60 + "\n\n"
    output += result['documentation']
    output += f"\n\n{'='*60}\n"
    output += f"Source: {result['file_path']}\n"

    return output

@mcp.tool()
def list_python_commands() -> str:
    """
    List all available Python HOM (Houdini Object Model) commands

    Returns a list of all hou module functions and classes available in the
    Python API documentation.

    Returns:
        List of all Python commands in the hou module
    """
    result = send_command({
        "type": "list_python_commands",
        "params": {}
    })

    output = f"🐍 Python HOM Commands: {result['num_commands']}\n\n"

    # Group commands by category if available
    if result.get('categories'):
        for category, commands in result['categories'].items():
            output += f"\n{category}:\n"
            for cmd in commands[:20]:  # Limit per category
                output += f"  • hou.{cmd}\n"
            if len(commands) > 20:
                output += f"  ... and {len(commands) - 20} more\n"
    else:
        # Fallback to flat list
        for cmd in result['commands'][:100]:
            output += f"  • hou.{cmd}\n"
        if result['num_commands'] > 100:
            output += f"\n... and {result['num_commands'] - 100} more commands\n"

    output += "\nTip: Use get_python_documentation('command_name') for detailed info\n"

    return output

@mcp.tool()
def get_python_documentation(command_name: str) -> str:
    """
    Get documentation for a specific Python HOM command or class

    The Houdini Object Model (HOM) documentation includes:
    - Classes: OpNode, Geometry, Parm, SopNode, Vector3, Matrix3, etc.
    - Functions: pwd(), node(), cd(), parent(), ch(), etc.
    - Enums: nodeType, parmTemplateType, etc.

    Use this to look up:
    - How to use specific HOM classes (e.g., "Geometry", "OpNode")
    - Function signatures and return types (e.g., "pwd", "node")
    - Method documentation (Note: for methods, look up the class name)

    Examples:
    - "OpNode" - Get docs for the base node class
    - "Geometry" - Learn about geometry manipulation
    - "pwd" - Understand current node context
    - "SopNode" - SOP-specific node operations

    Args:
        command_name: Name of the command (e.g., 'OpNode', 'Geometry', 'pwd')

    Returns:
        Full documentation text for the Python command
    """
    result = send_command({
        "type": "get_python_documentation",
        "params": {"command_name": command_name}
    })

    if result.get("error"):
        return f"❌ {result['error']}\n\nCommand: hou.{command_name}"

    output = f"📘 Python Documentation: hou.{command_name}\n"
    output += "="*60 + "\n\n"
    output += result['documentation']
    output += f"\n\n{'='*60}\n"
    output += f"Source: {result['file_path']}\n"

    return output

@mcp.tool()
def execute_python(code: str) -> str:
    """
    Execute Python code in Houdini using the Houdini Object Model (HOM)

    IMPORTANT TOOL-USAGE RULE:
    For usual scene tasks (creating nodes, connecting nodes, setting parameters,
    and inspecting scene structure), use dedicated MCP tools first:
    - create_node
    - connect_nodes / remove_connection
    - set_parameter
    - get_folder_info / get_node_info / get_node_parameters

    Use execute_python only when no dedicated tool can do the task.
    If a custom snippet is reusable and generic, propose creating a new
    dedicated MCP tool instead of repeating ad-hoc code execution.

    The Houdini Object Model (HOM) is Houdini's Python API. The 'hou' module
    is automatically available and provides access to all Houdini functionality.

    Key HOM concepts:
    - hou.node(path) - Get a node by path
    - hou.pwd() - Get current node context
    - hou.OpNode - Base class for all nodes (objects, SOPs, COPs, etc.)
    - hou.Geometry - Represents 3D geometry (points, primitives)
    - hou.Parm - Node parameters
    - node.createNode(type, name) - Create new nodes
    - node.parm(name) - Get parameter by name
    - node.geometry() - Get geometry from SOP nodes

    Common patterns:
    - Get node: hou.node("/obj/geo1")
    - Create node: parent.createNode("geo", "my_geo")
    - Set parameter: node.parm("tx").set(5.0)
    - Get geometry: geo_node.geometry()

    WARNING: Use carefully - executes directly in Houdini

    Args:
        code: Python code to execute (hou module is available)

    Returns:
        Output from execution
    """
    result = send_command({
        "type": "execute_python",
        "params": {"code": code}
    })

    output = ""

    if result.get("return_value") is not None:
        output += f"Return value: {result['return_value']}\n\n"

    if result.get("output"):
        output += f"Output:\n{result['output']}\n"

    if result.get("error"):
        output += f"\n❌ Error:\n{result['error']}"

    if not output:
        output = "✅ Executed successfully (no output)"

    return output

@mcp.tool()
def search_python_documentation(search_term: str, search_type: str = "all") -> str:
    """
    Search through HOM documentation for classes, functions, or keywords

    This tool searches the Houdini Object Model (HOM) documentation to help you
    find the right class or function when you don't know the exact name.

    Use this when you need to:
    - Find what classes/functions are available for a task
    - Discover HOM APIs by keyword (e.g., "geometry", "parameter", "render")
    - Look up related functionality

    Search types:
    - "all" - Search all documentation (default)
    - "class" - Search only class names
    - "function" - Search only function names
    - "content" - Search documentation content

    Examples:
    - search_term="geometry" - Find all geometry-related classes/functions
    - search_term="node", search_type="class" - Find node-related classes
    - search_term="parameter" - Find parameter manipulation APIs
    - search_term="vector" - Find vector/math classes

    Args:
        search_term: Keyword to search for
        search_type: Type of search ("all", "class", "function", "content")

    Returns:
        List of matching documentation entries with brief descriptions
    """
    result = send_command({
        "type": "search_python_documentation",
        "params": {
            "search_term": search_term,
            "search_type": search_type
        }
    })

    if result.get("error"):
        return f"❌ {result['error']}"

    output = f"🔍 Search results for '{search_term}' (type: {search_type})\n"
    output += f"Found {result['num_results']} matches\n\n"

    if result['num_results'] == 0:
        output += "No matches found. Try:\n"
        output += "- Using different keywords\n"
        output += "- Searching with search_type='all'\n"
        output += "- Using list_python_commands() to browse all available commands\n"
        return output

    for match in result['matches'][:30]:  # Limit to 30 results
        output += f"  • hou.{match['name']}"
        if match.get('type'):
            output += f" ({match['type']})"
        if match.get('description'):
            desc = match['description'][:80] + "..." if len(match['description']) > 80 else match['description']
            output += f"\n    {desc}"
        output += "\n\n"

    if result['num_results'] > 30:
        output += f"... and {result['num_results'] - 30} more matches\n"

    output += "\nUse get_python_documentation('name') to see full documentation\n"

    return output

@mcp.tool()
def get_node_connections(node_path: str) -> str:
    """
    Get all input and output connections for a specific node

    Use this for detailed connection analysis of a specific node.
    For a broader view of connections in a folder, use get_folder_info() instead.

    Args:
        node_path: Full path to the node (e.g., '/obj/geo1/box1')

    Returns:
        Information about node's input and output connections
    """
    result = send_command({
        "type": "get_node_connections",
        "params": {"node_path": node_path}
    })

    output = f"🔗 Connections for {result['node_path']}\n"
    output += f"   Type: {result['node_type']}\n\n"

    output += f"Inputs ({result['num_inputs']}):\n"
    if result['inputs']:
        for idx, inp in enumerate(result['inputs']):
            if inp:
                output += f"  [{idx}] ← {inp['source_node']} (output {inp['source_index']})\n"
            else:
                output += f"  [{idx}] (not connected)\n"
    else:
        output += "  (no inputs)\n"

    output += f"\nOutputs ({result['num_outputs']}):\n"
    if result['outputs']:
        for idx, outputs_list in enumerate(result['outputs']):
            if outputs_list:
                output += f"  [{idx}] → "
                connections = [f"{conn['dest_node']} (input {conn['dest_index']})" for conn in outputs_list]
                output += ", ".join(connections) + "\n"
            else:
                output += f"  [{idx}] (not connected)\n"
    else:
        output += "  (no outputs)\n"

    return output

@mcp.tool()
def execute_hscript(code: str) -> str:
    """
    Execute HScript commands in Houdini

    IMPORTANT TOOL-USAGE RULE:
    For usual scene tasks (creating nodes, connecting nodes, setting parameters,
    and inspecting scene structure), use dedicated MCP tools first.
    Use execute_hscript only when no dedicated tool can do the task.
    If the command solves a reusable/general workflow, suggest adding a
    dedicated MCP tool for it instead of relying on custom HScript.

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


@mcp.tool()
def search_documentation_files(query: str, file_pattern: str = "*.txt", search_content: bool = True, max_results: int = 30) -> str:
    """
    Search local Houdini documentation files under the project help directory.

    This searches by file path and (optionally) file content. Use it to locate
    relevant docs before reading a specific file with read_documentation_file().

    Args:
        query: Search term to match in path/content
        file_pattern: Glob filter for filenames (default: '*.txt')
        search_content: Whether to search within file contents (default: True)
        max_results: Maximum number of results (default: 30, max: 200)

    Returns:
        Matching documentation file paths and metadata
    """
    result = send_command({
        "type": "search_documentation_files",
        "params": {
            "query": query,
            "file_pattern": file_pattern,
            "search_content": search_content,
            "max_results": max_results,
        }
    })

    if result.get("error"):
        return f"❌ {result['error']}"

    output = f"🔎 Documentation search: '{query}'\n"
    output += f"   Pattern: {result.get('file_pattern', file_pattern)}\n"
    output += f"   Content search: {result.get('search_content', search_content)}\n"
    output += f"   Matches: {result.get('num_results', 0)}\n\n"

    matches = result.get("results", [])
    if not matches:
        output += "No matching documentation files found."
        return output

    for match in matches:
        output += f"  • {match['rel_path']} ({match['matched_in']}, {match['size_bytes']} bytes)\n"

    output += "\nUse read_documentation_file(path) to read a specific file."
    return output


@mcp.tool()
def read_documentation_file(path: str, max_chars: int = 20000) -> str:
    """
    Read a documentation file from the local project help directory.

    Use search_documentation_files() first to find the exact file path, then
    pass the relative path here.

    Args:
        path: Relative path under help/ (e.g., 'nodes/sop/box.txt')
        max_chars: Maximum characters to return (default: 20000)

    Returns:
        Documentation file contents
    """
    result = send_command({
        "type": "read_documentation_file",
        "params": {
            "path": path,
            "max_chars": max_chars,
        }
    })

    if result.get("error"):
        return f"❌ {result['error']}"

    output = f"📄 Documentation file: {result['path']}\n"
    output += f"   Size: {result['size_bytes']} bytes\n"
    if result.get("truncated"):
        output += f"   Note: output truncated to {result['max_chars']} chars\n"
    output += "\n"
    output += result.get("content", "")
    return output


@mcp.tool()
def create_digital_asset(
    node_path: str,
    definition_name: str,
    description: str,
    hda_file_path: str,
    min_inputs: int = 0,
    max_inputs: int = 0,
) -> str:
    """Create a digital asset from a node or export/update an existing HDA definition."""
    result = send_command({
        "type": "create_digital_asset",
        "params": {
            "node_path": node_path,
            "definition_name": definition_name,
            "description": description,
            "hda_file_path": hda_file_path,
            "min_inputs": min_inputs,
            "max_inputs": max_inputs,
        }
    })
    return (
        f"✅ Digital asset ready\n"
        f"Node: {result.get('node_path')}\n"
        f"Type: {result.get('node_type')}\n"
        f"Definition: {result.get('definition_name')}\n"
        f"File: {result.get('hda_file_path')}"
    )


@mcp.tool()
def set_hda_lock_state(node_path: str, locked: bool = True) -> str:
    """Lock or unlock an HDA instance."""
    result = send_command({
        "type": "set_hda_lock_state",
        "params": {
            "node_path": node_path,
            "locked": locked,
        }
    })
    return (
        f"✅ Lock state updated\n"
        f"Node: {result.get('node_path')}\n"
        f"Requested locked: {result.get('requested_locked')}\n"
        f"Matches definition: {result.get('matches_current_definition')}"
    )


@mcp.tool()
def save_hda_definition(node_path: str) -> str:
    """Save an HDA definition from an instance."""
    result = send_command({
        "type": "save_hda_definition",
        "params": {"node_path": node_path}
    })
    return (
        f"✅ Definition saved\n"
        f"Node: {result.get('node_path')}\n"
        f"Definition: {result.get('definition_name')}\n"
        f"File: {result.get('hda_file_path')}"
    )


@mcp.tool()
def get_hda_definition_info(node_path: str) -> str:
    """Get definition information for an HDA instance."""
    result = send_command({
        "type": "get_hda_definition_info",
        "params": {"node_path": node_path}
    })
    if not result.get("is_hda_instance"):
        return f"Node is not an HDA instance: {result.get('node_path')}"
    return (
        f"📦 HDA Definition Info\n"
        f"Node: {result.get('node_path')}\n"
        f"Node Type: {result.get('node_type')}\n"
        f"Definition: {result.get('definition_name')}\n"
        f"Description: {result.get('description')}\n"
        f"Library: {result.get('library_file_path')}\n"
        f"Matches definition: {result.get('matches_current_definition')}\n"
        f"Editable inside locked HDA: {result.get('is_editable_inside_locked_hda')}"
    )


@mcp.tool()
def edit_parameter_interface(
    node_path: str,
    parameters: Any,
    folder_name: str = "custom_controls",
    folder_label: str = "Custom Controls",
    clear_folder: bool = True,
    append_at_end: bool = True,
) -> str:
    """Edit a node's parameter interface from a declarative schema."""
    result = send_command({
        "type": "edit_parameter_interface",
        "params": {
            "node_path": node_path,
            "folder_name": folder_name,
            "folder_label": folder_label,
            "clear_folder": clear_folder,
            "append_at_end": append_at_end,
            "parameters": parameters,
        }
    })
    return (
        f"✅ Parameter interface updated\n"
        f"Node: {result.get('node_path')}\n"
        f"Folder: {result.get('folder_name')} ({result.get('folder_label')})\n"
        f"Parameters added: {result.get('num_parameters_added')}"
    )


@mcp.tool()
def set_parameter_conditionals(
    node_path: str,
    param_name: str,
    hide_when: Optional[str] = None,
    disable_when: Optional[str] = None,
) -> str:
    """Set hide/disable conditionals on an existing parameter template."""
    result = send_command({
        "type": "set_parameter_conditionals",
        "params": {
            "node_path": node_path,
            "param_name": param_name,
            "hide_when": hide_when,
            "disable_when": disable_when,
        }
    })
    return (
        f"✅ Conditionals updated\n"
        f"Node: {result.get('node_path')}\n"
        f"Parameter: {result.get('param_name')}\n"
        f"Hide when: {result.get('hide_when')}\n"
        f"Disable when: {result.get('disable_when')}"
    )


@mcp.tool()
def bind_internal_parameters(node_path: str, bindings: Any) -> str:
    """Bind internal parameters using expression mappings."""
    result = send_command({
        "type": "bind_internal_parameters",
        "params": {
            "node_path": node_path,
            "bindings": bindings,
        }
    })
    return (
        f"✅ Bindings applied\n"
        f"Node: {result.get('node_path')}\n"
        f"Applied: {result.get('num_bindings_applied')}"
    )


@mcp.tool()
def set_primitive_type_by_token(node_path: str, token: str) -> str:
    """Set a primitive node type parameter by menu token."""
    result = send_command({
        "type": "set_primitive_type_by_token",
        "params": {
            "node_path": node_path,
            "token": token,
        }
    })
    return (
        f"✅ Primitive type set\n"
        f"Node: {result.get('node_path')}\n"
        f"Token: {result.get('token')}\n"
        f"Label: {result.get('label')}"
    )


@mcp.tool()
def set_output_node_index(node_path: str, output_index: int = 0) -> str:
    """Set output index on an output node."""
    result = send_command({
        "type": "set_output_node_index",
        "params": {
            "node_path": node_path,
            "output_index": output_index,
        }
    })
    return f"✅ Output index set: {result.get('node_path')} -> {result.get('output_index')}"


@mcp.tool()
def validate_hda(node_path: str, rules: Any) -> str:
    """Validate HDA structure and expectations."""
    result = send_command({
        "type": "validate_hda",
        "params": {
            "node_path": node_path,
            "rules": rules,
        }
    })
    output = (
        f"🧪 validate_hda\n"
        f"Node: {result.get('node_path')}\n"
        f"Valid: {result.get('valid')}\n"
        f"Checks: {len(result.get('checks', []))}\n"
        f"Errors: {len(result.get('errors', []))}\n"
        f"Warnings: {len(result.get('warnings', []))}\n"
    )
    if result.get("errors"):
        output += "\nError details:\n"
        for err in result["errors"]:
            output += f"- {err}\n"
    if result.get("warnings"):
        output += "\nWarnings:\n"
        for warning in result["warnings"]:
            output += f"- {warning}\n"
    return output.strip()


@mcp.tool()
def get_hda_parm_templates(
    node_path: Optional[str] = None,
    type_name: Optional[str] = None,
    definition_name: Optional[str] = None,
) -> str:
    """Get parameter templates from an HDA definition."""
    result = send_command({
        "type": "get_hda_parm_templates",
        "params": {
            "node_path": node_path,
            "type_name": type_name,
            "definition_name": definition_name,
        }
    })
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def set_hda_parm_templates(
    templates: Any,
    node_path: Optional[str] = None,
    type_name: Optional[str] = None,
    definition_name: Optional[str] = None,
    replace_all: bool = True,
    sync_instance: bool = True,
) -> str:
    """Set parameter templates on an HDA definition."""
    result = send_command({
        "type": "set_hda_parm_templates",
        "params": {
            "node_path": node_path,
            "type_name": type_name,
            "definition_name": definition_name,
            "templates": templates,
            "replace_all": replace_all,
            "sync_instance": sync_instance,
        }
    })
    return (
        f"✅ HDA templates updated\n"
        f"Definition: {result.get('definition_name')}\n"
        f"File: {result.get('library_file_path')}\n"
        f"Top-level templates: {result.get('num_top_level_templates')}\n"
        f"replace_all: {result.get('replace_all')}"
    )


@mcp.tool()
def set_hda_parm_default(
    param_name: str,
    default_value: Any,
    node_path: Optional[str] = None,
    type_name: Optional[str] = None,
    definition_name: Optional[str] = None,
    sync_instance: bool = True,
) -> str:
    """Set a default value for an HDA parameter template."""
    result = send_command({
        "type": "set_hda_parm_default",
        "params": {
            "node_path": node_path,
            "type_name": type_name,
            "definition_name": definition_name,
            "param_name": param_name,
            "default_value": default_value,
            "sync_instance": sync_instance,
        }
    })
    return (
        f"✅ HDA default updated\n"
        f"Definition: {result.get('definition_name')}\n"
        f"Parameter: {result.get('param_name')}\n"
        f"Default: {result.get('default_value')}"
    )


@mcp.tool()
def set_hda_internal_binding(
    hda_node_path: str,
    internal_node: str,
    internal_parm: str,
    source_parm: Optional[str] = None,
    expression: Optional[str] = None,
    language: str = "hscript",
    unlock: bool = True,
    save_definition: bool = True,
    relock: bool = True,
) -> str:
    """Set an expression binding on an internal parameter of an HDA instance."""
    result = send_command({
        "type": "set_hda_internal_binding",
        "params": {
            "hda_node_path": hda_node_path,
            "internal_node": internal_node,
            "internal_parm": internal_parm,
            "source_parm": source_parm,
            "expression": expression,
            "language": language,
            "unlock": unlock,
            "save_definition": save_definition,
            "relock": relock,
        }
    })
    return (
        f"✅ Internal binding updated\n"
        f"HDA: {result.get('hda_node_path')}\n"
        f"Target: {result.get('target_parm_path')}\n"
        f"Expression: {result.get('expression')}\n"
        f"Language: {result.get('language')}"
    )


@mcp.tool()
def set_hda_internal_parm(
    hda_node_path: str,
    internal_node: str,
    internal_parm: str,
    param_value: Any = None,
    expression: Optional[str] = None,
    language: str = "hscript",
    unlock: bool = True,
    save_definition: bool = True,
    relock: bool = True,
) -> str:
    """Set value or expression on an internal parameter of an HDA instance."""
    result = send_command({
        "type": "set_hda_internal_parm",
        "params": {
            "hda_node_path": hda_node_path,
            "internal_node": internal_node,
            "internal_parm": internal_parm,
            "param_value": param_value,
            "expression": expression,
            "language": language,
            "unlock": unlock,
            "save_definition": save_definition,
            "relock": relock,
        }
    })
    return (
        f"✅ Internal parameter updated\n"
        f"HDA: {result.get('hda_node_path')}\n"
        f"Target: {result.get('target_parm_path')}\n"
        f"Value: {result.get('value')}"
    )


@mcp.tool()
def save_hda_from_instance(node_path: str, relock: bool = True) -> str:
    """Save HDA definition from an instance and optionally relock."""
    result = send_command({
        "type": "save_hda_from_instance",
        "params": {
            "node_path": node_path,
            "relock": relock,
        }
    })
    return (
        f"✅ HDA saved from instance\n"
        f"Node: {result.get('node_path')}\n"
        f"Definition: {result.get('definition_name')}\n"
        f"File: {result.get('library_file_path')}\n"
        f"Matches definition: {result.get('matches_current_definition')}"
    )


@mcp.tool()
def instantiate_hda(
    type_name: Optional[str] = None,
    definition_name: Optional[str] = None,
    parent_path: str = "/obj",
    node_name: str = "",
    set_display: bool = False,
) -> str:
    """Instantiate an HDA node in a given parent network."""
    result = send_command({
        "type": "instantiate_hda",
        "params": {
            "type_name": type_name,
            "definition_name": definition_name,
            "parent_path": parent_path,
            "node_name": node_name,
            "set_display": set_display,
        }
    })
    return (
        f"✅ HDA instantiated\n"
        f"Node: {result.get('node_path')}\n"
        f"Type: {result.get('node_type')}\n"
        f"Definition: {result.get('definition_name')}"
    )


@mcp.tool()
def probe_geometry(node_path: str) -> str:
    """Probe geometry output metrics for a SOP node."""
    result = send_command({
        "type": "probe_geometry",
        "params": {"node_path": node_path}
    })
    stats = result.get("stats", {})
    output = f"📊 Geometry probe: {result.get('node_path')}\n"
    output += f"Points: {stats.get('points')}\n"
    output += f"Prims: {stats.get('prims')}\n"
    output += f"Vertices: {stats.get('vertices')}\n"
    output += f"Point attribs: {stats.get('point_attributes')}\n"
    output += f"Prim attribs: {stats.get('prim_attributes')}\n"
    output += f"Detail attribs: {stats.get('detail_attributes')}"
    return output


@mcp.tool()
def validate_hda_behavior(
    node_path: str,
    cases: Any,
    comparisons: Optional[Any] = None,
    require_point_attributes: Optional[Any] = None,
) -> str:
    """Validate HDA behavior across parameterized geometry test cases."""
    result = send_command({
        "type": "validate_hda_behavior",
        "params": {
            "node_path": node_path,
            "cases": cases,
            "comparisons": comparisons or [],
            "require_point_attributes": require_point_attributes or [],
        }
    })
    output = (
        f"🧪 validate_hda_behavior\n"
        f"Node: {result.get('node_path')}\n"
        f"Valid: {result.get('valid')}\n"
        f"Cases: {len(result.get('case_results', {}))}\n"
        f"Checks: {len(result.get('checks', []))}\n"
        f"Errors: {len(result.get('errors', []))}\n"
    )
    if result.get("errors"):
        output += "\nError details:\n"
        for err in result["errors"]:
            output += f"- {err}\n"
    return output.strip()


# Register all tools via per-tool modules using legacy wrappers where needed.
register_mcp_tools(
    mcp,
    send_command,
    legacy_bridge_functions=globals(),
    tool_decorator=_real_mcp_tool_decorator,
)

# ============================================================================
# Server Entry Point
# ============================================================================

if __name__ == "__main__":
    print("Starting Houdini MCP Server...", file=sys.stderr)
    print("Connecting to Houdini on localhost:9876...", file=sys.stderr)
    mcp.run(transport="stdio")

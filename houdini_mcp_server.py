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
def get_folder_info(folder_path: str = "/obj") -> str:
    """
    **PRIMARY ENTRY POINT** - Get information about nodes in a specific folder

    THIS IS THE MAIN TOOL TO EXPLORE AND UNDERSTAND THE HOUDINI SCENE.
    Always start here when you need to understand what's in a scene.

    This tool shows you all nodes in a specific location with their connections,
    allowing you to navigate the scene hierarchy step by step.

    Navigation guide:
    - Start with "/" to see the root level
    - Use "/obj" to see all object-level nodes (default)
    - Use "/obj/geo1" to see inside a geometry node
    - Use "/stage" for USD/Solaris nodes
    - Use "/ch" for channel operators

    This is NON-RECURSIVE - it only shows direct children, making it fast
    and easy to navigate complex scenes level by level.

    Args:
        folder_path: Path to folder/node (e.g., '/', '/obj', '/obj/geo1')

    Returns:
        List of all nodes in the folder with their connections
    """
    result = send_command({
        "type": "get_folder_info",
        "params": {"folder_path": folder_path}
    })

    output = f"📁 Folder: {result['folder_path']}\n"
    output += f"   Type: {result['folder_type']}\n"
    output += f"   Children: {result['num_children']}\n\n"

    if result['num_children'] == 0:
        output += "   (empty)\n"
        return output

    output += "Nodes:\n"
    for node in result['children']:
        output += f"\n  📦 {node['name']} ({node['type']})\n"
        output += f"     Path: {node['path']}\n"

        # Show inputs
        if node.get('inputs'):
            output += f"     Inputs: "
            input_strs = []
            for idx, inp in enumerate(node['inputs']):
                if inp:
                    input_strs.append(f"[{idx}]←{inp['source_node']}")
            output += ", ".join(input_strs) if input_strs else "(none connected)"
            output += "\n"

        # Show outputs
        if node.get('outputs'):
            has_outputs = any(node['outputs'])
            if has_outputs:
                output += f"     Outputs: "
                output_strs = []
                for idx, outputs_list in enumerate(node['outputs']):
                    if outputs_list:
                        for conn in outputs_list:
                            output_strs.append(f"[{idx}]→{conn['dest_node']}")
                output += ", ".join(output_strs)
                output += "\n"

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

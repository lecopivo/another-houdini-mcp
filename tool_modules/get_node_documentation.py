from typing import Any, Optional
import json

TOOL_NAME = "get_node_documentation"
IS_MUTATING = False

send_command = None

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


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(get_node_documentation)


def execute_plugin(params, server, hou):
    """Get documentation for a specific node type from the help/nodes directory"""
    node_type = params.get("node_type", "")
    category = params.get("category", "sop").lower()

    import os

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct path to documentation file
    doc_file = os.path.join(script_dir, "help", "nodes", category, f"{node_type}.txt")

    if not os.path.exists(doc_file):
        return {
            "node_type": node_type,
            "category": category,
            "documentation": None,
            "error": f"Documentation file not found: {doc_file}"
        }

    try:
        with open(doc_file, 'r', encoding='utf-8') as f:
            documentation = f.read()

        return {
            "node_type": node_type,
            "category": category,
            "documentation": documentation,
            "file_path": doc_file
        }
    except Exception as e:
        return {
            "node_type": node_type,
            "category": category,
            "documentation": None,
            "error": f"Failed to read documentation: {str(e)}"
        }

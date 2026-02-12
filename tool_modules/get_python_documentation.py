from typing import Any, Optional
import json

TOOL_NAME = "get_python_documentation"
IS_MUTATING = False

send_command = None

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


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(get_python_documentation)


def execute_plugin(params, server, hou):
    """Get documentation for a specific Python HOM command"""
    command_name = params.get("command_name", "")

    import os

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct path to documentation file
    doc_file = os.path.join(script_dir, "help", "hom", "hou", f"{command_name}.txt")

    if not os.path.exists(doc_file):
        return {
            "command_name": command_name,
            "documentation": None,
            "error": f"Documentation file not found: {doc_file}"
        }

    try:
        with open(doc_file, 'r', encoding='utf-8') as f:
            documentation = f.read()

        return {
            "command_name": command_name,
            "documentation": documentation,
            "file_path": doc_file
        }
    except Exception as e:
        return {
            "command_name": command_name,
            "documentation": None,
            "error": f"Failed to read documentation: {str(e)}"
        }

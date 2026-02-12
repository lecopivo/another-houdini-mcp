from typing import Any, Optional
import json

TOOL_NAME = "save_hda_from_instance"
IS_MUTATING = True

send_command = None

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


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(save_hda_from_instance)


def execute_plugin(params, server, hou):
    """Save the HDA definition from an instance, with optional relock."""
    node_path = params.get("node_path", "")
    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")
    definition = node.type().definition()
    if definition is None:
        raise ValueError(f"Node is not an HDA instance: {node_path}")

    definition.updateFromNode(node)
    if bool(params.get("relock", True)):
        node.matchCurrentDefinition()

    return {
        "node_path": node.path(),
        "definition_name": definition.nodeTypeName(),
        "library_file_path": definition.libraryFilePath(),
        "matches_current_definition": node.matchesCurrentDefinition(),
    }

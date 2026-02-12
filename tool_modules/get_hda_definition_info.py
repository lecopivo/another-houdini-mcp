from typing import Any, Optional
import json

TOOL_NAME = "get_hda_definition_info"
IS_MUTATING = False

send_command = None

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


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(get_hda_definition_info)


def execute_plugin(params, server, hou):
    """Get definition information for an HDA instance."""
    node_path = params.get("node_path", "")

    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")

    definition = node.type().definition()
    if definition is None:
        return {
            "node_path": node.path(),
            "is_hda_instance": False,
        }

    return {
        "node_path": node.path(),
        "is_hda_instance": True,
        "node_type": node.type().nameWithCategory(),
        "definition_name": definition.nodeTypeName(),
        "description": definition.description(),
        "library_file_path": definition.libraryFilePath(),
        "matches_current_definition": node.matchesCurrentDefinition(),
        "is_editable_inside_locked_hda": node.isEditableInsideLockedHDA(),
    }

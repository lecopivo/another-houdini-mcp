from typing import Any, Optional
import json

TOOL_NAME = "save_hda_definition"
IS_MUTATING = True

send_command = None

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


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(save_hda_definition)


def execute_plugin(params, server, hou):
    """Save the current node contents/parameters back into its HDA definition."""
    node_path = params.get("node_path", "")

    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")

    definition = node.type().definition()
    if definition is None:
        raise ValueError(f"Node is not a digital asset instance: {node_path}")

    definition.updateFromNode(node)

    return {
        "node_path": node.path(),
        "definition_name": definition.nodeTypeName(),
        "hda_file_path": definition.libraryFilePath(),
    }

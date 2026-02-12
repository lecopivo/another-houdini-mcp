from typing import Any, Optional
import json

TOOL_NAME = "create_digital_asset"
IS_MUTATING = True

send_command = None

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


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(create_digital_asset)


def execute_plugin(params, server, hou):
    """Create a digital asset from an existing node or export/update an existing HDA definition."""
    import os

    node_path = params.get("node_path", "")
    definition_name = params.get("definition_name", "")
    description = params.get("description", "")
    hda_file_path = params.get("hda_file_path", "")
    min_inputs = int(params.get("min_inputs", 0))
    max_inputs = int(params.get("max_inputs", 0))

    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")

    if not definition_name:
        raise ValueError("definition_name is required")

    if not hda_file_path:
        raise ValueError("hda_file_path is required")

    hda_file_path = os.path.abspath(hda_file_path)
    os.makedirs(os.path.dirname(hda_file_path), exist_ok=True)

    existing_def = node.type().definition()

    if existing_def is None:
        node = node.createDigitalAsset(
            name=definition_name,
            hda_file_name=hda_file_path,
            description=description if description else node.name(),
            min_num_inputs=min_inputs,
            max_num_inputs=max_inputs,
        )
    else:
        # Existing HDA node: export/copy definition to requested target.
        existing_def.copyToHDAFile(
            hda_file_path,
            new_name=definition_name,
            new_menu_name=description if description else existing_def.description(),
        )

    definition = node.type().definition()
    definition.updateFromNode(node)

    return {
        "node_path": node.path(),
        "node_type": node.type().nameWithCategory(),
        "definition_name": definition.nodeTypeName(),
        "description": definition.description(),
        "hda_file_path": definition.libraryFilePath(),
    }

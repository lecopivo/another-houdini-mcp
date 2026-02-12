from typing import Any, Optional
import json

TOOL_NAME = "instantiate_hda"
IS_MUTATING = True

send_command = None

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


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(instantiate_hda)


def execute_plugin(params, server, hou):
    """Instantiate an HDA node in a given parent network."""
    type_name = params.get("type_name") or params.get("definition_name")
    parent_path = params.get("parent_path", "/obj")
    node_name = params.get("node_name", "")

    parent = hou.node(parent_path)
    if not parent:
        raise ValueError(f"Parent not found: {parent_path}")

    node_type = self._find_node_type(type_name)
    if node_type is None:
        raise ValueError(f"HDA type not found: {type_name}")

    node = parent.createNode(node_type.name(), node_name)

    if bool(params.get("set_display", False)) and hasattr(node, "setDisplayFlag"):
        try:
            node.setDisplayFlag(True)
            node.setRenderFlag(True)
        except Exception:
            pass

    return {
        "node_path": node.path(),
        "node_type": node.type().nameWithCategory(),
        "definition_name": node.type().definition().nodeTypeName() if node.type().definition() else None,
    }

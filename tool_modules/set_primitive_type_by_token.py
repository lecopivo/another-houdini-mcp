from typing import Any, Optional
import json

TOOL_NAME = "set_primitive_type_by_token"
IS_MUTATING = True

send_command = None

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


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(set_primitive_type_by_token)


def execute_plugin(params, server, hou):
    """Set primitive node 'type' parameter using a menu token (e.g. polymesh)."""
    node_path = params.get("node_path", "")
    token = str(params.get("token", ""))

    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")
    if not token:
        raise ValueError("token is required")

    type_parm = node.parm("type")
    if type_parm is None:
        raise ValueError(f"Node has no 'type' parameter: {node_path}")

    valid_tokens = tuple(type_parm.menuItems())
    if token not in valid_tokens:
        raise ValueError(f"Invalid token '{token}'. Valid tokens: {valid_tokens}")

    type_parm.set(token)

    return {
        "node_path": node.path(),
        "token": type_parm.evalAsString(),
        "label": type_parm.menuLabels()[type_parm.eval()],
    }

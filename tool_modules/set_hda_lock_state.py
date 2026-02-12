from typing import Any, Optional
import json

TOOL_NAME = "set_hda_lock_state"
IS_MUTATING = True

send_command = None

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


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(set_hda_lock_state)


def execute_plugin(params, server, hou):
    """Lock or unlock an HDA instance."""
    node_path = params.get("node_path", "")
    locked = bool(params.get("locked", True))

    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")

    definition = node.type().definition()
    if definition is None:
        raise ValueError(f"Node is not a digital asset instance: {node_path}")

    if locked:
        node.matchCurrentDefinition()
    else:
        node.allowEditingOfContents()

    return {
        "node_path": node.path(),
        "requested_locked": locked,
        "matches_current_definition": node.matchesCurrentDefinition(),
    }

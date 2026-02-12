from typing import Any, Optional
import json

TOOL_NAME = "set_output_node_index"
IS_MUTATING = True

send_command = None

def set_output_node_index(node_path: str, output_index: int = 0) -> str:
    """Set output index on an output node."""
    result = send_command({
        "type": "set_output_node_index",
        "params": {
            "node_path": node_path,
            "output_index": output_index,
        }
    })
    return f"✅ Output index set: {result.get('node_path')} -> {result.get('output_index')}"


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(set_output_node_index)


def execute_plugin(params, server, hou):
    """Set the output index for an output node."""
    node_path = params.get("node_path", "")
    output_index = int(params.get("output_index", 0))

    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")

    parm = node.parm("outputidx")
    if parm is None:
        raise ValueError(f"Node has no outputidx parameter: {node_path}")

    parm.set(output_index)

    return {
        "node_path": node.path(),
        "output_index": parm.eval(),
    }

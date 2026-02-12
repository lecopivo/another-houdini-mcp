from typing import Any, Optional
import json

TOOL_NAME = "probe_geometry"
IS_MUTATING = False

send_command = None

def probe_geometry(node_path: str) -> str:
    """Probe geometry output metrics for a SOP node."""
    result = send_command({
        "type": "probe_geometry",
        "params": {"node_path": node_path}
    })
    stats = result.get("stats", {})
    output = f"📊 Geometry probe: {result.get('node_path')}\n"
    output += f"Points: {stats.get('points')}\n"
    output += f"Prims: {stats.get('prims')}\n"
    output += f"Vertices: {stats.get('vertices')}\n"
    output += f"Point attribs: {stats.get('point_attributes')}\n"
    output += f"Prim attribs: {stats.get('prim_attributes')}\n"
    output += f"Detail attribs: {stats.get('detail_attributes')}"
    return output


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(probe_geometry)


def execute_plugin(params, server, hou):
    """Probe geometry output metrics for a node."""
    node_path = params.get("node_path", "")
    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")

    stats = self._geometry_stats(node)
    return {
        "node_path": node.path(),
        "stats": stats,
    }

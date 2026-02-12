from typing import Any, Optional
import json

TOOL_NAME = "get_scene_info"
IS_MUTATING = False

send_command = None

def get_scene_info() -> str:
    """
    Get high-level information about the current Houdini scene

    WARNING: This returns ALL nodes in the scene (recursive), which can be
    overwhelming for complex scenes with hundreds or thousands of nodes.

    RECOMMENDED: Use get_folder_info() instead to explore the scene
    step-by-step, starting with get_folder_info("/obj") or get_folder_info("/").

    Only use this tool if you need a quick overview of a simple scene.

    Returns:
        Scene structure with all nodes
    """
    result = send_command({
        "type": "get_scene_info",
        "params": {}
    })

    output = f"📁 Scene: {result['file_path']}\n"
    output += f"📊 Total nodes: {result['num_nodes']}\n\n"
    output += "Nodes:\n"

    for node in result['nodes'][:20]:
        output += f"  • {node['path']} ({node['type']})\n"

    if result['num_nodes'] > 20:
        output += f"\n... and {result['num_nodes'] - 20} more nodes\n"

    return output


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(get_scene_info)


def execute_plugin(params, server, hou):
    """Get scene information"""
    scene = hou.node("/")
    nodes = []

    for node in scene.allSubChildren():
        nodes.append({
            "path": node.path(),
            "name": node.name(),
            "type": node.type().name()
        })

    return {
        "num_nodes": len(nodes),
        "nodes": nodes,
        "file_path": hou.hipFile.path() if hou.hipFile.path() else "untitled"
    }

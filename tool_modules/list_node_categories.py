from typing import Any, Optional
import json

TOOL_NAME = "list_node_categories"
IS_MUTATING = False

send_command = None

def list_node_categories() -> str:
    """
    List all node categories (contexts) available in Houdini

    Returns a list of all contexts like Sop, Object, Dop, Chop, etc.

    Returns:
        List of all available node categories
    """
    result = send_command({
        "type": "list_node_categories",
        "params": {}
    })

    output = f"📂 Available Node Categories: {result['num_categories']}\n\n"

    for cat in result['categories']:
        output += f"  • {cat['name']}: {cat['label']}\n"

    return output


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(list_node_categories)


def execute_plugin(params, server, hou):
    """List all node categories (contexts) available in Houdini"""
    categories = hou.nodeTypeCategories()

    category_list = []
    for name, category in categories.items():
        category_list.append({
            "name": name,
            "label": category.label() if hasattr(category, 'label') else name
        })

    return {
        "num_categories": len(category_list),
        "categories": category_list
    }

from typing import Any, Optional
import json

TOOL_NAME = "list_node_types"
IS_MUTATING = False

send_command = None

def list_node_types(category: str = "Sop") -> str:
    """
    List all node types available in a specific category

    Args:
        category: Node category (e.g., 'Sop', 'Object', 'Dop', 'Chop', 'Cop2', 'Vop', 'Lop', 'Top')

    Returns:
        List of all node types in the category with descriptions
    """
    result = send_command({
        "type": "list_node_types",
        "params": {"category": category}
    })

    output = f"📦 Node Types in {result['category']}: {result['num_node_types']}\n\n"

    # Show first 50 node types
    for node_type in result['node_types'][:50]:
        desc = node_type['description'][:60] + "..." if len(node_type['description']) > 60 else node_type['description']
        output += f"  • {node_type['name']}: {desc}\n"

    if result['num_node_types'] > 50:
        output += f"\n... and {result['num_node_types'] - 50} more node types\n"
        output += "\nTip: Use get_node_documentation() to see detailed info for a specific node type\n"

    return output


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(list_node_types)


def execute_plugin(params, server, hou):
    """List all node types in a specific category"""
    category_name = params.get("category", "Sop")

    try:
        # Get the category
        if category_name.lower() == "sop":
            category = hou.sopNodeTypeCategory()
        elif category_name.lower() == "obj" or category_name.lower() == "object":
            category = hou.objNodeTypeCategory()
        elif category_name.lower() == "dop":
            category = hou.dopNodeTypeCategory()
        elif category_name.lower() == "cop2" or category_name.lower() == "cop":
            category = hou.cop2NodeTypeCategory()
        elif category_name.lower() == "chop":
            category = hou.chopNodeTypeCategory()
        elif category_name.lower() == "vop":
            category = hou.vopNodeTypeCategory()
        elif category_name.lower() == "lop":
            category = hou.lopNodeTypeCategory()
        elif category_name.lower() == "top":
            category = hou.topNodeTypeCategory()
        else:
            # Try to get it from the categories dict
            categories = hou.nodeTypeCategories()
            category = categories.get(category_name)
            if not category:
                raise ValueError(f"Unknown category: {category_name}")

        # Get all node types
        node_types = category.nodeTypes()

        node_type_list = []
        for name, node_type in node_types.items():
            node_type_list.append({
                "name": name,
                "description": node_type.description() if node_type.description() else "",
                "category": category.name()
            })

        return {
            "category": category.name(),
            "num_node_types": len(node_type_list),
            "node_types": node_type_list
        }

    except Exception as e:
        raise ValueError(f"Failed to list node types: {str(e)}")

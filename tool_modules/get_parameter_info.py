from typing import Any, Optional
import json

TOOL_NAME = "get_parameter_info"
IS_MUTATING = False

send_command = None

def get_parameter_info(node_type: str, category: str = "Sop") -> str:
    """
    Get information about available parameters for a node type
    Useful for understanding what parameters you can set before creating a node

    Args:
        node_type: Type of node (e.g., 'sphere', 'box', 'tube')
        category: Node category - 'Sop' for geometry, 'Obj' for objects, 'Dop' for dynamics (default: 'Sop')

    Returns:
        Information about available parameters for this node type
    """
    result = send_command({
        "type": "get_parameter_info",
        "params": {
            "node_type": node_type,
            "category": category
        }
    })

    output = f"📘 Parameter Info for {result['node_type']} ({result['category']})\n"
    if result.get('description'):
        output += f"   Description: {result['description']}\n"
    output += f"   Total parameters: {result['num_parameters']}\n\n"

    # Show key parameters (limited to 30 for readability)
    for parm in result['parameters'][:30]:
        output += f"   • {parm['name']} ({parm['type']})\n"
        output += f"     Label: {parm['label']}\n"

        if parm.get('default_value'):
            output += f"     Default: {parm['default_value']}\n"

        if parm.get('help') and len(parm['help']) < 100:
            output += f"     Help: {parm['help']}\n"

        output += "\n"

    if result['num_parameters'] > 30:
        output += f"... and {result['num_parameters'] - 30} more parameters\n"

    return output


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(get_parameter_info)


def execute_plugin(params, server, hou):
    """Get information about available parameters for a node type"""
    node_type = params.get("node_type", "")
    category = params.get("category", "Sop")  # Default to SOP (geometry)

    try:
        # Get the node type definition
        if category.lower() == "sop":
            type_category = hou.sopNodeTypeCategory()
        elif category.lower() == "obj":
            type_category = hou.objNodeTypeCategory()
        elif category.lower() == "dop":
            type_category = hou.dopNodeTypeCategory()
        else:
            type_category = hou.sopNodeTypeCategory()

        node_type_def = type_category.nodeType(node_type)
        if not node_type_def:
            raise ValueError(f"Node type not found: {node_type}")

        # Get parameter templates
        parm_templates = node_type_def.parmTemplates()
        parameters = []

        for parm_template in parm_templates:
            parm_info = {
                "name": parm_template.name(),
                "label": parm_template.label(),
                "type": parm_template.type().name(),
                "help": parm_template.help() if parm_template.help() else "",
                "num_components": parm_template.numComponents(),
                "default_value": parm_template.defaultValue() if hasattr(parm_template, 'defaultValue') else None
            }
            parameters.append(parm_info)

        return {
            "node_type": node_type,
            "category": category,
            "description": node_type_def.description() if node_type_def.description() else "",
            "num_parameters": len(parameters),
            "parameters": parameters
        }
    except Exception as e:
        raise ValueError(f"Failed to get parameter info: {str(e)}")

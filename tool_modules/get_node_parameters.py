TOOL_NAME = "get_node_parameters"
IS_MUTATING = False


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def get_node_parameters(
        node_path: str,
        show_defaults: bool = False,
        only_overrides: bool = False,
    ) -> str:
        """Get all parameters and their current values from a node."""
        result = send_command({
            "type": TOOL_NAME,
            "params": {
                "node_path": node_path,
                "only_overrides": only_overrides,
            }
        })

        output = f"🔧 Parameters for {result['node_path']}\n"
        output += f"   Type: {result['node_type']}\n"
        output += f"   Total parameters: {result['num_parameters']}\n"
        if only_overrides:
            output += "   Mode: overrides only\n"
        output += "\n"

        for parm in result['parameters'][:50]:
            status = ""
            if parm.get('is_locked'):
                status += " 🔒"
            if parm.get('has_expression'):
                status += " 📐"

            output += f"   • {parm['name']} ({parm['type']}): {parm['value']}{status}\n"

            if show_defaults and parm.get('default_value') is not None:
                output += f"     Default: {parm['default_value']}\n"

        if result['num_parameters'] > 50:
            output += f"\n... and {result['num_parameters'] - 50} more parameters\n"

        return output


def execute_plugin(params, server, hou):
    node_path = params.get("node_path", "")
    only_overrides = bool(params.get("only_overrides", False))
    node = hou.node(node_path)

    if not node:
        raise ValueError(f"Node not found: {node_path}")

    parameters = []
    for parm in node.parms():
        parm_template = parm.parmTemplate()
        try:
            has_keyframes = len(parm.keyframes()) > 0
        except Exception:
            has_keyframes = False
        try:
            has_expression = bool(parm.expression())
        except Exception:
            has_expression = False
        try:
            is_non_default = not parm.isAtDefault()
        except Exception:
            is_non_default = False

        if only_overrides and not (is_non_default or has_keyframes or has_expression):
            continue

        parm_info = {
            "name": parm.name(),
            "label": parm_template.label(),
            "type": parm_template.type().name(),
            "value": None,
            "default_value": None,
            "has_expression": has_expression,
            "has_keyframes": has_keyframes,
            "is_non_default": is_non_default,
            "is_locked": parm.isLocked(),
        }

        try:
            parm_type = parm_template.type()
            if parm_type in (hou.parmTemplateType.Toggle, hou.parmTemplateType.Int, hou.parmTemplateType.Float, hou.parmTemplateType.String):
                parm_info["value"] = parm.eval()
            else:
                parm_info["value"] = str(parm.eval())

            parm_info["default_value"] = parm_template.defaultValue()[0] if parm_template.defaultValue() else None
        except Exception:
            parm_info["value"] = "N/A"
            parm_info["default_value"] = "N/A"

        parameters.append(parm_info)

    return {
        "node_path": node_path,
        "node_type": node.type().name(),
        "num_parameters": len(parameters),
        "parameters": parameters,
    }

from typing import Any, Optional
import json

TOOL_NAME = "set_hda_parm_default"
IS_MUTATING = True

send_command = None

def set_hda_parm_default(
    param_name: str,
    default_value: Any,
    node_path: Optional[str] = None,
    type_name: Optional[str] = None,
    definition_name: Optional[str] = None,
    sync_instance: bool = True,
) -> str:
    """Set a default value for an HDA parameter template."""
    result = send_command({
        "type": "set_hda_parm_default",
        "params": {
            "node_path": node_path,
            "type_name": type_name,
            "definition_name": definition_name,
            "param_name": param_name,
            "default_value": default_value,
            "sync_instance": sync_instance,
        }
    })
    return (
        f"✅ HDA default updated\n"
        f"Definition: {result.get('definition_name')}\n"
        f"Parameter: {result.get('param_name')}\n"
        f"Default: {result.get('default_value')}"
    )


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(set_hda_parm_default)


def execute_plugin(params, server, hou):
    """Set a single default value on an HDA definition parameter template."""
    node, definition = self._resolve_hda_definition(params)
    param_name = params.get("param_name", "")
    default_value = params.get("default_value")

    if not param_name:
        raise ValueError("param_name is required")
    if default_value is None:
        raise ValueError("default_value is required")

    ptg = definition.parmTemplateGroup()
    template = ptg.find(param_name)
    if template is None:
        raise ValueError(f"Parameter template not found: {param_name}")

    parm_type = template.type()
    if parm_type == hou.parmTemplateType.Toggle:
        template.setDefaultValue(bool(default_value))
    elif parm_type == hou.parmTemplateType.Menu:
        template.setDefaultValue(int(default_value))
    else:
        num_components = template.numComponents() if hasattr(template, "numComponents") else 1
        if isinstance(default_value, (list, tuple)):
            value_tuple = tuple(default_value)
        else:
            value_tuple = tuple(default_value for _ in range(num_components))
        if len(value_tuple) != num_components:
            raise ValueError(
                f"default_value length mismatch for {param_name}. "
                f"Expected {num_components}, got {len(value_tuple)}"
            )
        template.setDefaultValue(value_tuple)

    ptg.replace(param_name, template)
    definition.setParmTemplateGroup(ptg)

    if node is not None and bool(params.get("sync_instance", True)):
        node.matchCurrentDefinition()

    return {
        "definition_name": definition.nodeTypeName(),
        "param_name": param_name,
        "default_value": default_value,
    }

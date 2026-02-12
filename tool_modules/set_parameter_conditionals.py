from typing import Any, Optional
import json

TOOL_NAME = "set_parameter_conditionals"
IS_MUTATING = True

send_command = None

def set_parameter_conditionals(
    node_path: str,
    param_name: str,
    hide_when: Optional[str] = None,
    disable_when: Optional[str] = None,
) -> str:
    """Set hide/disable conditionals on an existing parameter template."""
    result = send_command({
        "type": "set_parameter_conditionals",
        "params": {
            "node_path": node_path,
            "param_name": param_name,
            "hide_when": hide_when,
            "disable_when": disable_when,
        }
    })
    return (
        f"✅ Conditionals updated\n"
        f"Node: {result.get('node_path')}\n"
        f"Parameter: {result.get('param_name')}\n"
        f"Hide when: {result.get('hide_when')}\n"
        f"Disable when: {result.get('disable_when')}"
    )


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(set_parameter_conditionals)


def execute_plugin(params, server, hou):
    """Set hide/disable conditionals on an existing parameter template."""
    node_path = params.get("node_path", "")
    param_name = params.get("param_name", "")
    hide_when = params.get("hide_when")
    disable_when = params.get("disable_when")

    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")
    if not param_name:
        raise ValueError("param_name is required")

    ptg = node.parmTemplateGroup()
    parm_template = ptg.find(param_name)
    if parm_template is None:
        raise ValueError(f"Parameter template not found: {param_name}")

    if hide_when is not None:
        parm_template.setConditional(hou.parmCondType.HideWhen, str(hide_when))
    if disable_when is not None:
        parm_template.setConditional(hou.parmCondType.DisableWhen, str(disable_when))

    ptg.replace(param_name, parm_template)
    node.setParmTemplateGroup(ptg)

    return {
        "node_path": node.path(),
        "param_name": param_name,
        "hide_when": hide_when,
        "disable_when": disable_when,
    }

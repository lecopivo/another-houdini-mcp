from typing import Any, Optional
import json

TOOL_NAME = "bind_internal_parameters"
IS_MUTATING = True

send_command = None

def bind_internal_parameters(node_path: str, bindings: Any) -> str:
    """Bind internal parameters using expression mappings."""
    result = send_command({
        "type": "bind_internal_parameters",
        "params": {
            "node_path": node_path,
            "bindings": bindings,
        }
    })
    return (
        f"✅ Bindings applied\n"
        f"Node: {result.get('node_path')}\n"
        f"Applied: {result.get('num_bindings_applied')}"
    )


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(bind_internal_parameters)


def execute_plugin(params, server, hou):
    """Bind internal parameters to controller parameters via expressions."""
    node_path = params.get("node_path", "")
    bindings = params.get("bindings", [])

    root = hou.node(node_path) if node_path else None
    if node_path and root is None:
        raise ValueError(f"Node not found: {node_path}")
    if not isinstance(bindings, list):
        raise ValueError("bindings must be a list")

    applied = 0
    for binding in bindings:
        target_node_ref = binding.get("target_node", "")
        target_parm_name = binding.get("target_parm", "")
        expression = binding.get("expression")
        language_raw = str(binding.get("language", "hscript")).lower()
        source_parm = binding.get("source_parm", "")

        if not target_node_ref or not target_parm_name:
            raise ValueError("Each binding requires target_node and target_parm")

        if target_node_ref.startswith("/"):
            target_node = hou.node(target_node_ref)
        elif root:
            target_node = root.node(target_node_ref)
        else:
            target_node = None

        if target_node is None:
            raise ValueError(f"Target node not found: {target_node_ref}")

        target_parm = target_node.parm(target_parm_name)
        if target_parm is None:
            raise ValueError(f"Target parameter not found: {target_node.path()}.{target_parm_name}")

        if expression is None:
            if not source_parm:
                raise ValueError("Each binding requires either expression or source_parm")
            expression = f'ch("../{source_parm}")'

        if language_raw == "python":
            language = hou.exprLanguage.Python
        else:
            language = hou.exprLanguage.Hscript

        target_parm.setExpression(str(expression), language)
        applied += 1

    return {
        "node_path": root.path() if root else None,
        "num_bindings_applied": applied,
    }

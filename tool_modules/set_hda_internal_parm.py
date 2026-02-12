from typing import Any, Optional
import json

TOOL_NAME = "set_hda_internal_parm"
IS_MUTATING = True

send_command = None

def set_hda_internal_parm(
    hda_node_path: str,
    internal_node: str,
    internal_parm: str,
    param_value: Any = None,
    expression: Optional[str] = None,
    language: str = "hscript",
    unlock: bool = True,
    save_definition: bool = True,
    relock: bool = True,
) -> str:
    """Set value or expression on an internal parameter of an HDA instance."""
    result = send_command({
        "type": "set_hda_internal_parm",
        "params": {
            "hda_node_path": hda_node_path,
            "internal_node": internal_node,
            "internal_parm": internal_parm,
            "param_value": param_value,
            "expression": expression,
            "language": language,
            "unlock": unlock,
            "save_definition": save_definition,
            "relock": relock,
        }
    })
    return (
        f"✅ Internal parameter updated\n"
        f"HDA: {result.get('hda_node_path')}\n"
        f"Target: {result.get('target_parm_path')}\n"
        f"Value: {result.get('value')}"
    )


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(set_hda_internal_parm)


def execute_plugin(params, server, hou):
    """Set a value or expression on an internal parameter of an HDA instance."""
    hda_node_path = params.get("hda_node_path", "")
    internal_node = params.get("internal_node", "")
    internal_parm = params.get("internal_parm", "")
    param_value = params.get("param_value")
    expression = params.get("expression")
    language_raw = str(params.get("language", "hscript")).lower()

    hda_node = hou.node(hda_node_path)
    if not hda_node:
        raise ValueError(f"HDA node not found: {hda_node_path}")
    if hda_node.type().definition() is None:
        raise ValueError(f"Node is not an HDA instance: {hda_node_path}")
    if not internal_node or not internal_parm:
        raise ValueError("internal_node and internal_parm are required")

    if bool(params.get("unlock", True)):
        hda_node.allowEditingOfContents()

    target_node = hda_node.node(internal_node)
    if target_node is None:
        raise ValueError(f"Internal node not found: {hda_node_path}/{internal_node}")

    target_parm = target_node.parm(internal_parm)
    if target_parm is None:
        raise ValueError(f"Internal parameter not found: {target_node.path()}.{internal_parm}")

    if expression is not None:
        language = hou.exprLanguage.Python if language_raw == "python" else hou.exprLanguage.Hscript
        target_parm.setExpression(str(expression), language)
    else:
        target_parm.set(param_value)

    if bool(params.get("save_definition", True)):
        hda_node.type().definition().updateFromNode(hda_node)
    if bool(params.get("relock", True)):
        hda_node.matchCurrentDefinition()

    return {
        "hda_node_path": hda_node.path(),
        "target_parm_path": f"{target_node.path()}.{internal_parm}",
        "value": target_parm.evalAsString() if target_parm.parmTemplate().type() == hou.parmTemplateType.String else target_parm.eval(),
    }

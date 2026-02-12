from typing import Any, Optional
import json

TOOL_NAME = "set_hda_internal_binding"
IS_MUTATING = True

send_command = None

def set_hda_internal_binding(
    hda_node_path: str,
    internal_node: str,
    internal_parm: str,
    source_parm: Optional[str] = None,
    expression: Optional[str] = None,
    language: str = "hscript",
    unlock: bool = True,
    save_definition: bool = True,
    relock: bool = True,
) -> str:
    """Set an expression binding on an internal parameter of an HDA instance."""
    result = send_command({
        "type": "set_hda_internal_binding",
        "params": {
            "hda_node_path": hda_node_path,
            "internal_node": internal_node,
            "internal_parm": internal_parm,
            "source_parm": source_parm,
            "expression": expression,
            "language": language,
            "unlock": unlock,
            "save_definition": save_definition,
            "relock": relock,
        }
    })
    return (
        f"✅ Internal binding updated\n"
        f"HDA: {result.get('hda_node_path')}\n"
        f"Target: {result.get('target_parm_path')}\n"
        f"Expression: {result.get('expression')}\n"
        f"Language: {result.get('language')}"
    )


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(set_hda_internal_binding)


def execute_plugin(params, server, hou):
    """Set an expression binding on an internal parameter of an HDA instance."""
    hda_node_path = params.get("hda_node_path", "")
    internal_node = params.get("internal_node", "")
    internal_parm = params.get("internal_parm", "")
    source_parm = params.get("source_parm")
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

    if expression is None:
        if not source_parm:
            raise ValueError("Either source_parm or expression is required")
        expression = f'ch(\"../{source_parm}\")'

    language = hou.exprLanguage.Python if language_raw == "python" else hou.exprLanguage.Hscript
    target_parm.setExpression(str(expression), language)

    if bool(params.get("save_definition", True)):
        hda_node.type().definition().updateFromNode(hda_node)
    if bool(params.get("relock", True)):
        hda_node.matchCurrentDefinition()

    return {
        "hda_node_path": hda_node.path(),
        "target_parm_path": f"{target_node.path()}.{internal_parm}",
        "expression": str(expression),
        "language": "python" if language == hou.exprLanguage.Python else "hscript",
    }

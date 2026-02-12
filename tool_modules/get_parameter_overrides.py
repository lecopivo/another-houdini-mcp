TOOL_NAME = "get_parameter_overrides"
IS_MUTATING = False


def _safe_parm_value(parm):
    try:
        return parm.eval()
    except Exception:
        try:
            return parm.evalAsString()
        except Exception:
            return "N/A"


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def get_parameter_overrides(
        node_path: str,
        include_animated: bool = True,
        include_expressions: bool = True,
    ) -> str:
        """List non-default/animated parameters on a node."""
        result = send_command(
            {
                "type": TOOL_NAME,
                "params": {
                    "node_path": node_path,
                    "include_animated": include_animated,
                    "include_expressions": include_expressions,
                },
            }
        )

        output = (
            f"🎛️ Parameter overrides\n"
            f"Node: {result.get('node_path')}\n"
            f"Overrides: {result.get('num_overrides')}\n\n"
        )
        for item in result.get("overrides", []):
            tags = []
            if item.get("is_non_default"):
                tags.append("non-default")
            if item.get("has_keyframes"):
                tags.append("keyframed")
            if item.get("has_expression"):
                tags.append("expression")
            tag_text = ", ".join(tags) if tags else "override"
            output += f"- {item.get('name')}: {item.get('value')} ({tag_text})\n"
        return output.strip()


def execute_plugin(params, server, hou):
    node_path = params.get("node_path", "")
    include_animated = bool(params.get("include_animated", True))
    include_expressions = bool(params.get("include_expressions", True))

    node = hou.node(node_path)
    if node is None:
        raise ValueError(f"Node not found: {node_path}")

    overrides = []
    for parm in node.parms():
        try:
            is_non_default = not parm.isAtDefault()
        except Exception:
            is_non_default = False

        has_keyframes = False
        if include_animated:
            try:
                has_keyframes = len(parm.keyframes()) > 0
            except Exception:
                has_keyframes = False

        has_expression = False
        if include_expressions:
            try:
                has_expression = bool(parm.expression())
            except Exception:
                has_expression = False

        if not (is_non_default or has_keyframes or has_expression):
            continue

        overrides.append(
            {
                "name": parm.name(),
                "value": _safe_parm_value(parm),
                "is_non_default": is_non_default,
                "has_keyframes": has_keyframes,
                "has_expression": has_expression,
            }
        )

    overrides.sort(key=lambda item: item["name"])
    return {
        "node_path": node.path(),
        "num_overrides": len(overrides),
        "overrides": overrides,
    }

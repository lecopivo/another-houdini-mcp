TOOL_NAME = "get_node_presentation"
IS_MUTATING = False


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def get_node_presentation(node_path: str) -> str:
        """Get UI/presentation state for a node (flags and comment)."""
        result = send_command({"type": TOOL_NAME, "params": {"node_path": node_path}})
        output = f"🎛️ Node presentation: {result.get('path')}\n"
        output += f"Display: {result.get('display_flag')}\n"
        output += f"Render: {result.get('render_flag')}\n"
        output += f"Template: {result.get('template_flag')}\n"
        output += f"Bypass: {result.get('bypass_flag')}\n"
        comment = result.get("comment", "")
        output += f"Comment: {comment if comment else '(empty)'}"
        return output


def execute_plugin(params, server, hou):
    node_path = str(params.get("node_path", "")).strip()
    node = hou.node(node_path)
    if node is None:
        raise ValueError(f"Node not found: {node_path}")

    def _safe_call(method_name, fallback=False):
        fn = getattr(node, method_name, None)
        if callable(fn):
            try:
                return bool(fn())
            except Exception:
                return fallback
        return fallback

    template_flag = False
    template_fn = getattr(node, "isTemplateFlagSet", None)
    if callable(template_fn):
        try:
            template_flag = bool(template_fn())
        except Exception:
            template_flag = False
    else:
        generic_flag_fn = getattr(node, "isGenericFlagSet", None)
        if callable(generic_flag_fn):
            try:
                template_flag = bool(generic_flag_fn(hou.nodeFlag.Template))
            except Exception:
                template_flag = False

    return {
        "path": node.path(),
        "display_flag": _safe_call("isDisplayFlagSet", False),
        "render_flag": _safe_call("isRenderFlagSet", False),
        "template_flag": template_flag,
        "bypass_flag": _safe_call("isBypassed", False),
        "comment": node.comment() or "",
    }

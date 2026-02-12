TOOL_NAME = "get_node_info"
IS_MUTATING = False


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def get_node_info(node_path: str) -> str:
        """Get detailed information about a specific node."""
        result = send_command({
            "type": TOOL_NAME,
            "params": {"node_path": node_path}
        })

        output = f"📦 Node: {result['path']}\n"
        output += f"   Type: {result['type']} ({result['type_category']})\n"
        output += f"   Inputs: {result['num_inputs']}, Outputs: {result['num_outputs']}\n"
        output += f"   Position: {result['position']}\n"
        lock_value = result.get('is_locked')
        lock_label = str(lock_value) if lock_value is not None else "N/A (non-HDA)"
        output += f"   Locked: {lock_label}, Template: {result['is_template']}\n"
        if result.get('comment'):
            output += f"   Comment: {result['comment']}\n"
        return output


def execute_plugin(params, server, hou):
    node_path = params.get("node_path", "")
    node = hou.node(node_path)

    if not node:
        raise ValueError(f"Node not found: {node_path}")

    is_hda = node.type().definition() is not None
    is_locked = None
    if is_hda:
        lock_fn = getattr(node, "isLockedHDA", None)
        if callable(lock_fn):
            try:
                is_locked = bool(lock_fn())
            except Exception:
                is_locked = None

    return {
        "path": node.path(),
        "name": node.name(),
        "type": node.type().name(),
        "type_category": node.type().category().name(),
        "num_inputs": len(node.inputs()),
        "num_outputs": len(node.outputs()),
        "position": [node.position()[0], node.position()[1]],
        "is_hda": is_hda,
        "is_locked": is_locked,
        "is_template": node.isTemplateFlagSet(),
        "comment": node.comment(),
    }

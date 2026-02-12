TOOL_NAME = "delete_node"
IS_MUTATING = True


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def delete_node(node_path: str) -> str:
        """
        Delete a node from Houdini

        Args:
            node_path: Full path to the node (e.g., '/obj/geo1')

        Returns:
            Confirmation message
        """
        result = send_command({
            "type": TOOL_NAME,
            "params": {"node_path": node_path}
        })
        return result.get("message", "Node deleted")


def execute_plugin(params, server, hou):
    node_path = params.get("node_path", "")
    node = hou.node(node_path)

    if not node:
        raise ValueError(f"Node not found: {node_path}")

    node.destroy()
    print(f"✅ Deleted node: {node_path}")
    return {"message": f"Deleted: {node_path}"}

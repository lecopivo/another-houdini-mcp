"""create_node tool definition shared between bridge and plugin."""

TOOL_NAME = "create_node"
IS_MUTATING = True


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def create_node(node_type: str, node_name: str = "", parent: str = "/obj") -> str:
        """
        Create a new node in Houdini

        Args:
            node_type: Type of node (e.g., 'geo', 'null', 'light', 'camera')
            node_name: Optional name for the node
            parent: Parent path (default: /obj)

        Returns:
            Path to the created node
        """
        result = send_command(
            {
                "type": TOOL_NAME,
                "params": {
                    "node_type": node_type,
                    "node_name": node_name,
                    "parent": parent,
                },
            }
        )
        return f"✅ Created: {result['node_path']} (type: {result['node_type']})"


def execute_plugin(params, server, hou):
    node_type = params.get("node_type", "")
    node_name = params.get("node_name", "")
    parent_path = params.get("parent", "/obj")

    parent = hou.node(parent_path)
    if not parent:
        raise ValueError(f"Parent not found: {parent_path}")

    node = parent.createNode(node_type, node_name)
    print(f"✅ Created node: {node.path()}")

    return {
        "node_path": node.path(),
        "node_name": node.name(),
        "node_type": node.type().name(),
    }

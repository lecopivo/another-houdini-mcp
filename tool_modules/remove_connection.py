TOOL_NAME = "remove_connection"
IS_MUTATING = True


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def remove_connection(dest_path: str, dest_index: int = 0) -> str:
        """Remove a specific connection from a node's input."""
        result = send_command({
            "type": TOOL_NAME,
            "params": {
                "dest_path": dest_path,
                "dest_index": dest_index,
            }
        })
        return result.get("message", "Connection removed")


def execute_plugin(params, server, hou):
    dest_path = params.get("dest_path", "")
    dest_index = params.get("dest_index", 0)

    dest = hou.node(dest_path)
    if not dest:
        raise ValueError(f"Destination node not found: {dest_path}")

    current_input = dest.input(dest_index)
    if not current_input:
        raise ValueError(f"No connection at {dest_path} input {dest_index}")

    source_path = current_input.path()
    source_output_idx = 0
    for conn in current_input.outputConnections():
        if conn.inputNode() == dest and conn.inputIndex() == dest_index:
            source_output_idx = conn.outputIndex()
            break

    dest.setInput(dest_index, None)
    print(f"✅ Removed connection {source_path}[{source_output_idx}] -> {dest_path}[{dest_index}]")
    return {
        "message": f"Removed connection from {source_path}[output {source_output_idx}] to {dest_path}[input {dest_index}]",
        "source_path": source_path,
        "source_index": source_output_idx,
        "dest_path": dest_path,
        "dest_index": dest_index,
    }

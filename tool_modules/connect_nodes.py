TOOL_NAME = "connect_nodes"
IS_MUTATING = True


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def connect_nodes(source_path: str, dest_path: str, source_index: int = 0, dest_index: int = 0) -> str:
        """
        Connect one node's output to another node's input with specific indices
        """
        result = send_command({
            "type": TOOL_NAME,
            "params": {
                "source_path": source_path,
                "dest_path": dest_path,
                "source_index": source_index,
                "dest_index": dest_index,
            }
        })
        return result.get("message", "Nodes connected")


def execute_plugin(params, server, hou):
    source_path = params.get("source_path", "")
    dest_path = params.get("dest_path", "")
    source_index = params.get("source_index", 0)
    dest_index = params.get("dest_index", 0)

    source = hou.node(source_path)
    dest = hou.node(dest_path)

    if not source or not dest:
        raise ValueError("Source or destination not found")

    dest.setInput(dest_index, source, source_index)
    print(f"✅ Connected {source_path}[{source_index}] -> {dest_path}[{dest_index}]")
    return {"message": f"Connected {source_path}[output {source_index}] to {dest_path}[input {dest_index}]"}

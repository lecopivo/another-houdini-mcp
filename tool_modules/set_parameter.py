from typing import Any

TOOL_NAME = "set_parameter"
IS_MUTATING = True


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def set_parameter(node_path: str, param_name: str, param_value: Any) -> str:
        """Set a parameter on a node."""
        result = send_command({
            "type": TOOL_NAME,
            "params": {
                "node_path": node_path,
                "param_name": param_name,
                "param_value": param_value,
            }
        })
        return result.get("message", "Parameter set")


def execute_plugin(params, server, hou):
    node_path = params.get("node_path", "")
    param_name = params.get("param_name", "")
    param_value = params.get("param_value", "")

    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")

    parm = node.parm(param_name)
    if not parm:
        raise ValueError(f"Parameter not found: {param_name}")

    parm.set(param_value)
    print(f"✅ Set {node_path}.{param_name} = {param_value}")
    return {"message": f"Set {param_name} = {param_value}"}

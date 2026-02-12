"""Helpers for behavior-safe migration of legacy tools."""


def register_legacy_mcp_tool(tool_name, mcp, legacy_bridge_functions, tool_decorator=None):
    if legacy_bridge_functions is None:
        raise ValueError(f"Missing legacy_bridge_functions for tool: {tool_name}")
    legacy_fn = legacy_bridge_functions.get(tool_name)
    if legacy_fn is None:
        raise ValueError(f"Missing legacy bridge function for tool: {tool_name}")
    decorator = tool_decorator or mcp.tool
    decorator()(legacy_fn)


def execute_legacy_plugin_tool(server, method_name, params):
    method = getattr(server, method_name, None)
    if method is None:
        raise ValueError(f"Missing plugin handler method: {method_name}")
    return method(params)

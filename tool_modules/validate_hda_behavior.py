from .legacy_tool import execute_legacy_plugin_tool, register_legacy_mcp_tool

TOOL_NAME = "validate_hda_behavior"
IS_MUTATING = False


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    register_legacy_mcp_tool(TOOL_NAME, mcp, legacy_bridge_functions, tool_decorator)


def execute_plugin(params, server, hou):
    return execute_legacy_plugin_tool(server, "_validate_hda_behavior", params)

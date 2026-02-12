"""Registry for tools implemented as one file per tool."""

from . import create_node, get_folder_info

TOOL_MODULES = [
    create_node,
    get_folder_info,
]


def register_mcp_tools(mcp, send_command):
    """Register migrated per-tool MCP wrappers on the bridge side."""
    for module in TOOL_MODULES:
        module.register_mcp_tool(mcp, send_command)


def get_plugin_handlers(hou):
    """Return plugin handler mapping for migrated per-tool implementations."""
    handlers = {}
    for module in TOOL_MODULES:
        handlers[module.TOOL_NAME] = lambda params, fn=module.execute_plugin: fn(params, hou)
    return handlers


def get_mutating_commands():
    """Return migrated tool names that mutate scene state."""
    return {module.TOOL_NAME for module in TOOL_MODULES if getattr(module, "IS_MUTATING", False)}

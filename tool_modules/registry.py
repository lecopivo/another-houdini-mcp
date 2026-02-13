"""Registry for tools implemented as one file per tool."""

import importlib

from . import (
    bind_internal_parameters,
    connect_nodes,
    create_digital_asset,
    create_node,
    delete_node,
    edit_parameter_interface,
    execute_hscript,
    execute_python,
    get_folder_info,
    get_hda_definition_info,
    get_hda_parm_templates,
    get_node_connections,
    get_node_documentation,
    get_node_info,
    get_node_presentation,
    get_node_parameters,
    get_parameter_overrides,
    get_parameter_info,
    get_python_documentation,
    get_scene_info,
    get_sticky_notes,
    install_hda_file,
    instantiate_example_asset,
    instantiate_hda,
    list_example_nodes,
    list_node_categories,
    list_node_types,
    list_python_commands,
    load_example,
    probe_geometry,
    read_documentation_file,
    remove_connection,
    save_hda_definition,
    save_hda_from_instance,
    search_documentation_files,
    search_python_documentation,
    set_hda_internal_binding,
    set_hda_internal_parm,
    set_hda_lock_state,
    set_hda_parm_default,
    set_hda_parm_templates,
    set_output_node_index,
    set_parameter,
    set_parameter_conditionals,
    set_primitive_type_by_token,
    validate_hda,
    validate_hda_behavior,
)

TOOL_MODULES = [
    bind_internal_parameters,
    connect_nodes,
    create_digital_asset,
    create_node,
    delete_node,
    edit_parameter_interface,
    execute_hscript,
    execute_python,
    get_folder_info,
    get_hda_definition_info,
    get_hda_parm_templates,
    get_node_connections,
    get_node_documentation,
    get_node_info,
    get_node_presentation,
    get_node_parameters,
    get_parameter_overrides,
    get_parameter_info,
    get_python_documentation,
    get_scene_info,
    get_sticky_notes,
    install_hda_file,
    instantiate_example_asset,
    instantiate_hda,
    list_example_nodes,
    list_node_categories,
    list_node_types,
    list_python_commands,
    load_example,
    probe_geometry,
    read_documentation_file,
    remove_connection,
    save_hda_definition,
    save_hda_from_instance,
    search_documentation_files,
    search_python_documentation,
    set_hda_internal_binding,
    set_hda_internal_parm,
    set_hda_lock_state,
    set_hda_parm_default,
    set_hda_parm_templates,
    set_output_node_index,
    set_parameter,
    set_parameter_conditionals,
    set_primitive_type_by_token,
    validate_hda,
    validate_hda_behavior,
]

def _iter_tool_modules(reload_modules: bool = False):
    """Yield tool modules, optionally reloading each module first."""
    for module in TOOL_MODULES:
        if reload_modules:
            try:
                module = importlib.reload(module)
            except Exception:
                pass
        yield module


def register_mcp_tools(mcp, send_command, tool_decorator=None):
    """Register migrated per-tool MCP wrappers on the bridge side."""
    for module in _iter_tool_modules(reload_modules=False):
        module.register_mcp_tool(mcp, send_command, None, tool_decorator)


def get_plugin_handlers(server, hou):
    """Return plugin handler mapping for migrated per-tool implementations."""
    handlers = {}
    # Reload modules in-plugin so edits are picked up without restarting Houdini.
    for module in _iter_tool_modules(reload_modules=True):
        handlers[module.TOOL_NAME] = (
            lambda params, fn=module.execute_plugin: fn(params, server, hou)
        )
    return handlers


def get_mutating_commands():
    """Return migrated tool names that mutate scene state."""
    return {
        module.TOOL_NAME
        for module in _iter_tool_modules(reload_modules=True)
        if getattr(module, "IS_MUTATING", False)
    }

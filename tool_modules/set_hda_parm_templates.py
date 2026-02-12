from typing import Any, Optional
import json

TOOL_NAME = "set_hda_parm_templates"
IS_MUTATING = True

send_command = None

def set_hda_parm_templates(
    templates: Any,
    node_path: Optional[str] = None,
    type_name: Optional[str] = None,
    definition_name: Optional[str] = None,
    replace_all: bool = True,
    sync_instance: bool = True,
) -> str:
    """Set parameter templates on an HDA definition."""
    result = send_command({
        "type": "set_hda_parm_templates",
        "params": {
            "node_path": node_path,
            "type_name": type_name,
            "definition_name": definition_name,
            "templates": templates,
            "replace_all": replace_all,
            "sync_instance": sync_instance,
        }
    })
    return (
        f"✅ HDA templates updated\n"
        f"Definition: {result.get('definition_name')}\n"
        f"File: {result.get('library_file_path')}\n"
        f"Top-level templates: {result.get('num_top_level_templates')}\n"
        f"replace_all: {result.get('replace_all')}"
    )


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(set_hda_parm_templates)


def execute_plugin(params, server, hou):
    """Set parameter templates on an HDA definition."""
    node, definition = self._resolve_hda_definition(params)
    templates = params.get("templates", [])
    replace_all = bool(params.get("replace_all", True))

    if not isinstance(templates, list):
        raise ValueError("templates must be a list")

    if replace_all:
        ptg = hou.ParmTemplateGroup()
    else:
        ptg = definition.parmTemplateGroup()

    for spec in templates:
        ptg.append(self._create_parm_template_from_tree(spec))

    definition.setParmTemplateGroup(ptg)

    if node is not None and bool(params.get("sync_instance", True)):
        node.matchCurrentDefinition()

    return {
        "definition_name": definition.nodeTypeName(),
        "library_file_path": definition.libraryFilePath(),
        "num_top_level_templates": len(definition.parmTemplateGroup().entries()),
        "replace_all": replace_all,
    }

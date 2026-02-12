from typing import Any, Optional
import json

TOOL_NAME = "get_hda_parm_templates"
IS_MUTATING = False

send_command = None

def get_hda_parm_templates(
    node_path: Optional[str] = None,
    type_name: Optional[str] = None,
    definition_name: Optional[str] = None,
) -> str:
    """Get parameter templates from an HDA definition."""
    result = send_command({
        "type": "get_hda_parm_templates",
        "params": {
            "node_path": node_path,
            "type_name": type_name,
            "definition_name": definition_name,
        }
    })
    return json.dumps(result, indent=2, default=str)


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(get_hda_parm_templates)


def execute_plugin(params, server, hou):
    """Get parameter templates from an HDA definition."""
    _, definition = self._resolve_hda_definition(params)
    ptg = definition.parmTemplateGroup()
    templates = [self._parm_template_to_dict(entry) for entry in ptg.entries()]

    return {
        "definition_name": definition.nodeTypeName(),
        "library_file_path": definition.libraryFilePath(),
        "num_top_level_templates": len(templates),
        "templates": templates,
    }

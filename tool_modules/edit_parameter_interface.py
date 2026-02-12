from typing import Any, Optional
import json

TOOL_NAME = "edit_parameter_interface"
IS_MUTATING = True

send_command = None

def edit_parameter_interface(
    node_path: str,
    parameters: Any,
    folder_name: str = "custom_controls",
    folder_label: str = "Custom Controls",
    clear_folder: bool = True,
    append_at_end: bool = True,
) -> str:
    """Edit a node's parameter interface from a declarative schema."""
    result = send_command({
        "type": "edit_parameter_interface",
        "params": {
            "node_path": node_path,
            "folder_name": folder_name,
            "folder_label": folder_label,
            "clear_folder": clear_folder,
            "append_at_end": append_at_end,
            "parameters": parameters,
        }
    })
    return (
        f"✅ Parameter interface updated\n"
        f"Node: {result.get('node_path')}\n"
        f"Folder: {result.get('folder_name')} ({result.get('folder_label')})\n"
        f"Parameters added: {result.get('num_parameters_added')}"
    )


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(edit_parameter_interface)


def execute_plugin(params, server, hou):
    """Edit node parameter interface from a declarative schema."""
    node_path = params.get("node_path", "")
    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")

    folder_name = params.get("folder_name", "custom_controls")
    folder_label = params.get("folder_label", "Custom Controls")
    clear_folder = bool(params.get("clear_folder", True))
    append_at_end = bool(params.get("append_at_end", True))
    parameter_specs = params.get("parameters", [])

    if not isinstance(parameter_specs, list):
        raise ValueError("parameters must be a list")

    ptg = node.parmTemplateGroup()

    if clear_folder:
        try:
            ptg.remove(folder_name)
        except Exception:
            pass

    folder = hou.FolderParmTemplate(folder_name, folder_label)
    for spec in parameter_specs:
        parm_template = self._create_parm_template_from_spec(spec)
        folder.addParmTemplate(parm_template)

    if append_at_end:
        ptg.append(folder)
    else:
        ptg.insertBefore((0,), folder)

    node.setParmTemplateGroup(ptg)

    return {
        "node_path": node.path(),
        "folder_name": folder_name,
        "folder_label": folder_label,
        "num_parameters_added": len(parameter_specs),
    }

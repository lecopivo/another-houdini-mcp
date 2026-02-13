import os

from .hda_utils import find_node_type

TOOL_NAME = "instantiate_example_asset"
IS_MUTATING = True


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def instantiate_example_asset(
        example_otl_path: str,
        type_name: str = "",
        parent_path: str = "/obj",
        node_name: str = "",
        replace_if_exists: bool = False,
        set_display: bool = False,
    ) -> str:
        """Install an example OTL/HDA and instantiate one node from it."""
        result = send_command(
            {
                "type": TOOL_NAME,
                "params": {
                    "example_otl_path": example_otl_path,
                    "type_name": type_name,
                    "parent_path": parent_path,
                    "node_name": node_name,
                    "replace_if_exists": replace_if_exists,
                    "set_display": set_display,
                },
            }
        )

        output = "✅ Example asset loaded\n"
        output += f"Asset file: {result.get('example_otl_path')}\n"
        output += f"Type: {result.get('type_name')}\n"
        output += f"Created node: {result.get('node_path')}"
        return output


def execute_plugin(params, server, hou):
    example_otl_path = str(params.get("example_otl_path", "")).strip()
    parent_path = str(params.get("parent_path", "/obj")).strip() or "/obj"
    node_name = str(params.get("node_name", "")).strip()
    requested_type_name = str(params.get("type_name", "")).strip()
    replace_if_exists = bool(params.get("replace_if_exists", False))
    set_display = bool(params.get("set_display", False))

    if not example_otl_path:
        raise ValueError("example_otl_path is required")

    path = os.path.abspath(os.path.expanduser(example_otl_path))
    if not os.path.isfile(path):
        raise ValueError(f"Example asset not found: {path}")

    parent = hou.node(parent_path)
    if parent is None:
        raise ValueError(f"Parent not found: {parent_path}")

    hou.hda.installFile(path, change_oplibraries_file=False)

    type_name = requested_type_name
    definition_names = []
    if hasattr(hou.hda, "definitionsInFile"):
        defs = hou.hda.definitionsInFile(path)
        definition_names = [
            d.nodeTypeName() if hasattr(d, "nodeTypeName") else str(d)
            for d in defs
        ]
        if not type_name and defs:
            try:
                type_name = defs[0].nodeTypeName()
            except Exception:
                type_name = ""

    if not type_name:
        raise ValueError("Unable to resolve type_name from file; provide type_name explicitly")

    node_type = find_node_type(type_name, hou)
    if node_type is None:
        raise ValueError(f"Node type not found after install: {type_name}")

    if node_name:
        existing = parent.node(node_name)
        if existing is not None:
            if not replace_if_exists:
                raise ValueError(
                    f"Node already exists: {existing.path()}. Set replace_if_exists=True to replace."
                )
            existing.destroy()

    node = parent.createNode(node_type.name(), node_name) if node_name else parent.createNode(node_type.name())

    if set_display and hasattr(node, "setDisplayFlag"):
        try:
            node.setDisplayFlag(True)
            node.setRenderFlag(True)
        except Exception:
            pass

    return {
        "example_otl_path": path,
        "type_name": type_name,
        "definition_names": definition_names,
        "node_path": node.path(),
    }

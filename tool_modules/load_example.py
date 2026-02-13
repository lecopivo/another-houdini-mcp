import os

from .hda_utils import find_node_type

TOOL_NAME = "load_example"
IS_MUTATING = True


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def load_example(
        context: str,
        node: str,
        example_name: str,
        parent_path: str = "/obj",
        node_name: str = "",
        type_name: str = "",
        replace_if_exists: bool = False,
        set_display: bool = False,
    ) -> str:
        """Load an official example asset by context/node/example name and instantiate it."""
        result = send_command(
            {
                "type": TOOL_NAME,
                "params": {
                    "context": context,
                    "node": node,
                    "example_name": example_name,
                    "parent_path": parent_path,
                    "node_name": node_name,
                    "type_name": type_name,
                    "replace_if_exists": replace_if_exists,
                    "set_display": set_display,
                },
            }
        )

        lines = [
            "✅ Example loaded",
            f"Doc: {result.get('example_txt_path')}",
            f"Asset: {result.get('example_asset_path')}",
            f"Type: {result.get('type_name')}",
            f"Created node: {result.get('node_path')}",
        ]
        return "\n".join(lines)


def execute_plugin(params, server, hou):
    context = str(params.get("context", "")).strip().lower()
    node = str(params.get("node", "")).strip()
    example_name = str(params.get("example_name", "")).strip()
    parent_path = str(params.get("parent_path", "/obj")).strip() or "/obj"
    node_name = str(params.get("node_name", "")).strip()
    requested_type_name = str(params.get("type_name", "")).strip()
    replace_if_exists = bool(params.get("replace_if_exists", False))
    set_display = bool(params.get("set_display", False))

    if not context or not node or not example_name:
        raise ValueError("context, node, and example_name are required")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    example_dir = os.path.join(repo_dir, "help", "examples", "nodes", context, node)
    if not os.path.isdir(example_dir):
        raise ValueError(f"Example directory not found: {example_dir}")

    txt_path = os.path.join(example_dir, f"{example_name}.txt")
    if not os.path.isfile(txt_path):
        raise ValueError(f"Example text not found: {txt_path}")

    asset_path = None
    for ext in (".otl", ".hda"):
        candidate = os.path.join(example_dir, f"{example_name}{ext}")
        if os.path.isfile(candidate):
            asset_path = candidate
            break
    if asset_path is None:
        raise ValueError(
            f"No example asset found for {example_name}. Expected .otl or .hda in {example_dir}"
        )

    parent = hou.node(parent_path)
    if parent is None:
        raise ValueError(f"Parent not found: {parent_path}")

    hou.hda.installFile(asset_path, change_oplibraries_file=False)

    type_name = requested_type_name
    definition_names = []
    defs = hou.hda.definitionsInFile(asset_path) if hasattr(hou.hda, "definitionsInFile") else []
    if defs:
        definition_names = [
            d.nodeTypeName() if hasattr(d, "nodeTypeName") else str(d)
            for d in defs
        ]
        if not type_name:
            try:
                type_name = defs[0].nodeTypeName()
            except Exception:
                type_name = ""

    if not type_name:
        raise ValueError("Unable to resolve type_name from asset; provide type_name explicitly")

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

    created = parent.createNode(node_type.name(), node_name) if node_name else parent.createNode(node_type.name())

    if set_display and hasattr(created, "setDisplayFlag"):
        try:
            created.setDisplayFlag(True)
            created.setRenderFlag(True)
        except Exception:
            pass

    rel_txt = os.path.join("examples", "nodes", context, node, f"{example_name}.txt")
    rel_asset = os.path.join("examples", "nodes", context, node, os.path.basename(asset_path))

    return {
        "context": context,
        "node": node,
        "example_name": example_name,
        "example_txt_path": rel_txt,
        "example_asset_path": rel_asset,
        "type_name": type_name,
        "definition_names": definition_names,
        "node_path": created.path(),
    }

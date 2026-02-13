import os

TOOL_NAME = "install_hda_file"
IS_MUTATING = True


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def install_hda_file(
        hda_file_path: str,
        change_oplibraries_file: bool = False,
        force_reload: bool = False,
    ) -> str:
        """Install an HDA/OTL file into the current Houdini session."""
        result = send_command(
            {
                "type": TOOL_NAME,
                "params": {
                    "hda_file_path": hda_file_path,
                    "change_oplibraries_file": change_oplibraries_file,
                    "force_reload": force_reload,
                },
            }
        )

        lines = [
            "✅ HDA file installed",
            f"File: {result.get('hda_file_path')}",
            f"Definitions: {result.get('definition_count', 0)}",
        ]
        for name in result.get("definition_names", []):
            lines.append(f"- {name}")
        return "\n".join(lines)


def execute_plugin(params, server, hou):
    hda_file_path = str(params.get("hda_file_path", "")).strip()
    if not hda_file_path:
        raise ValueError("hda_file_path is required")

    path = os.path.abspath(os.path.expanduser(hda_file_path))
    if not os.path.isfile(path):
        raise ValueError(f"HDA file not found: {path}")

    change_oplibraries_file = bool(params.get("change_oplibraries_file", False))
    force_reload = bool(params.get("force_reload", False))

    if force_reload and hasattr(hou.hda, "reloadFile"):
        try:
            hou.hda.reloadFile(path)
        except Exception:
            pass

    hou.hda.installFile(path, change_oplibraries_file=change_oplibraries_file)

    definition_names = []
    if hasattr(hou.hda, "definitionsInFile"):
        try:
            defs = hou.hda.definitionsInFile(path)
            definition_names = [
                d.nodeTypeName() if hasattr(d, "nodeTypeName") else str(d)
                for d in defs
            ]
        except Exception:
            definition_names = []

    return {
        "hda_file_path": path,
        "definition_count": len(definition_names),
        "definition_names": definition_names,
    }

from typing import Any

TOOL_NAME = "get_sticky_notes"
IS_MUTATING = False


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def get_sticky_notes(
        folder_path: str = "/obj",
        recursive: bool = True,
        include_empty: bool = False,
    ) -> str:
        """Get sticky-note/post-it text from a network and optional sub-networks."""
        result = send_command(
            {
                "type": TOOL_NAME,
                "params": {
                    "folder_path": folder_path,
                    "recursive": recursive,
                    "include_empty": include_empty,
                },
            }
        )

        output = (
            f"🗒️ Sticky notes\n"
            f"Root: {result.get('folder_path')}\n"
            f"Recursive: {result.get('recursive')}\n"
            f"Notes: {result.get('num_notes')}\n\n"
        )
        for note in result.get("notes", []):
            output += f"- {note.get('sticky_path')} (network: {note.get('network_path')})\n"
            output += f"  {note.get('text')}\n"
        return output.strip()


def execute_plugin(params, server, hou):
    folder_path = params.get("folder_path", "/obj")
    recursive = bool(params.get("recursive", True))
    include_empty = bool(params.get("include_empty", False))

    root = hou.node(folder_path)
    if root is None:
        raise ValueError(f"Folder not found: {folder_path}")

    networks = [root]
    if recursive:
        for child in root.allSubChildren():
            try:
                if child.isNetwork():
                    networks.append(child)
            except Exception:
                pass

    seen = set()
    notes = []
    for net in networks:
        if net.path() in seen:
            continue
        seen.add(net.path())
        try:
            stickies = net.stickyNotes()
        except Exception:
            continue
        for sticky in stickies:
            text = (sticky.text() or "").strip()
            if not text and not include_empty:
                continue
            notes.append(
                {
                    "network_path": net.path(),
                    "sticky_path": sticky.path(),
                    "text": text,
                }
            )

    return {
        "folder_path": root.path(),
        "recursive": recursive,
        "num_notes": len(notes),
        "notes": notes,
    }

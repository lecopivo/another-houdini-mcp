TOOL_NAME = "read_documentation_file"
IS_MUTATING = False


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def read_documentation_file(path: str, max_chars: int = 20000) -> str:
        """Read a documentation file from the local project help directory."""
        result = send_command({
            "type": TOOL_NAME,
            "params": {
                "path": path,
                "max_chars": max_chars,
            }
        })

        if result.get("error"):
            return f"❌ {result['error']}"

        output = f"📄 Documentation file: {result['path']}\n"
        output += f"   Size: {result['size_bytes']} bytes\n"
        if result.get("truncated"):
            output += f"   Note: output truncated to {result['max_chars']} chars\n"
        output += "\n"
        output += result.get("content", "")
        return output


def execute_plugin(params, server, hou):
    import os

    rel_path = params.get("path", "").strip()
    max_chars = int(params.get("max_chars", 20000))
    max_chars = max(500, min(max_chars, 200000))

    if not rel_path:
        return {"error": "path is required"}

    script_dir = os.path.dirname(os.path.abspath(__file__))
    help_dir = os.path.join(os.path.dirname(script_dir), "help")
    normalized_rel = os.path.normpath(rel_path).lstrip("/")
    file_path = os.path.abspath(os.path.join(help_dir, normalized_rel))

    if not file_path.startswith(os.path.abspath(help_dir) + os.sep):
        return {"error": "path must stay within the help directory"}

    if not os.path.isfile(file_path):
        return {
            "error": f"Documentation file not found: {normalized_rel}",
            "help_dir": help_dir,
        }

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read(max_chars + 1)

    truncated = len(content) > max_chars
    if truncated:
        content = content[:max_chars]

    return {
        "path": normalized_rel,
        "file_path": file_path,
        "content": content,
        "truncated": truncated,
        "max_chars": max_chars,
        "size_bytes": os.path.getsize(file_path),
    }

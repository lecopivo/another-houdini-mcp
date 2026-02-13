import fnmatch
import os

TOOL_NAME = "list_example_nodes"
IS_MUTATING = False


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def list_example_nodes(
        context: str,
        node: str = "",
        file_pattern: str = "*.txt",
        include_missing_assets: bool = True,
    ) -> str:
        """List available example docs and assets under help/examples/nodes."""
        result = send_command(
            {
                "type": TOOL_NAME,
                "params": {
                    "context": context,
                    "node": node,
                    "file_pattern": file_pattern,
                    "include_missing_assets": include_missing_assets,
                },
            }
        )

        output = [
            f"📚 Example listing: context={result.get('context')}",
            f"Node filter: {result.get('node') or '(all)'}",
            f"Matches: {result.get('num_examples', 0)}",
            "",
        ]

        for entry in result.get("examples", []):
            line = f"- {entry.get('node')}/{entry.get('example_name')}: {entry.get('txt_path')}"
            asset = entry.get("asset_path")
            if asset:
                line += f" | asset: {asset}"
            output.append(line)

        if result.get("num_examples", 0) == 0:
            output.append("No matching examples found.")

        return "\n".join(output)


def execute_plugin(params, server, hou):
    context = str(params.get("context", "")).strip().lower()
    node_filter = str(params.get("node", "")).strip()
    file_pattern = str(params.get("file_pattern", "*.txt")).strip() or "*.txt"
    include_missing_assets = bool(params.get("include_missing_assets", True))

    if not context:
        raise ValueError("context is required")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    base_dir = os.path.join(repo_dir, "help", "examples", "nodes", context)

    if not os.path.isdir(base_dir):
        raise ValueError(f"Context examples directory not found: {base_dir}")

    node_dirs = [node_filter] if node_filter else sorted(os.listdir(base_dir))
    results = []

    for node_name in node_dirs:
        node_dir = os.path.join(base_dir, node_name)
        if not os.path.isdir(node_dir):
            continue

        for filename in sorted(os.listdir(node_dir)):
            if not fnmatch.fnmatch(filename, file_pattern):
                continue
            if not filename.lower().endswith(".txt"):
                continue

            example_name = os.path.splitext(filename)[0]
            txt_path = os.path.join("examples", "nodes", context, node_name, filename)

            asset_path = None
            for ext in (".otl", ".hda"):
                candidate = os.path.join(node_dir, example_name + ext)
                if os.path.isfile(candidate):
                    asset_path = os.path.join(
                        "examples", "nodes", context, node_name, example_name + ext
                    )
                    break

            if asset_path is None and not include_missing_assets:
                continue

            results.append(
                {
                    "context": context,
                    "node": node_name,
                    "example_name": example_name,
                    "txt_path": txt_path,
                    "asset_path": asset_path,
                }
            )

    results.sort(key=lambda x: (x["node"], x["example_name"]))

    return {
        "context": context,
        "node": node_filter,
        "file_pattern": file_pattern,
        "num_examples": len(results),
        "examples": results,
    }

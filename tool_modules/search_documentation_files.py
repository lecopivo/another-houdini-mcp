TOOL_NAME = "search_documentation_files"
IS_MUTATING = False


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def search_documentation_files(
        query: str,
        file_pattern: str = "*.txt",
        search_content: bool = True,
        search_mode: str = "any",
        max_results: int = 30,
        context_chars: int = 100,
    ) -> str:
        """
        Search local Houdini documentation files under the project help directory.

        This searches by file path and (optionally) file content. Use it to locate
        relevant docs before reading a specific file with read_documentation_file().
        """
        result = send_command({
            "type": TOOL_NAME,
            "params": {
                "query": query,
                "file_pattern": file_pattern,
                "search_content": search_content,
                "search_mode": search_mode,
                "max_results": max_results,
                "context_chars": context_chars,
            }
        })

        if result.get("error"):
            return f"❌ {result['error']}"

        output = f"🔎 Documentation search: '{query}'\n"
        output += f"   Terms: {', '.join(result.get('query_terms', []))}\n"
        output += f"   Pattern: {result.get('file_pattern', file_pattern)}\n"
        output += f"   Content search: {result.get('search_content', search_content)}\n"
        output += f"   Mode: {result.get('search_mode', search_mode)}\n"
        output += f"   Matches: {result.get('num_results', 0)}\n\n"

        matches = result.get("results", [])
        if not matches:
            output += "No matching documentation files found."
            return output

        for match in matches:
            output += (
                f"  • {match['rel_path']} "
                f"(score={match.get('score', 0)}, {match['matched_in']}, {match['size_bytes']} bytes)\n"
            )
            if match.get("matched_terms"):
                output += f"    terms: {', '.join(match['matched_terms'])}\n"
            if match.get("snippet"):
                output += f"    snippet: {match['snippet']}\n"

        output += "\nUse read_documentation_file(path) to read a specific file."
        return output


def execute_plugin(params, server, hou):
    import fnmatch
    import os
    import re

    query = params.get("query", "").strip().lower()
    file_pattern = params.get("file_pattern", "*.txt")
    search_content = bool(params.get("search_content", True))
    search_mode = str(params.get("search_mode", "any")).lower()
    max_results = int(params.get("max_results", 30))
    max_results = max(1, min(max_results, 200))
    context_chars = int(params.get("context_chars", 100))
    context_chars = max(20, min(context_chars, 400))

    if not query:
        return {"num_results": 0, "results": [], "error": "query is required"}

    if search_mode not in ("any", "all"):
        return {"num_results": 0, "results": [], "error": "search_mode must be 'any' or 'all'"}

    query_terms = [term for term in re.split(r"\s+", query) if term] or [query]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    help_dir = os.path.join(os.path.dirname(script_dir), "help")

    if not os.path.isdir(help_dir):
        return {
            "num_results": 0,
            "results": [],
            "error": f"Documentation directory not found: {help_dir}",
        }

    results = []
    for root, _, files in os.walk(help_dir):
        for filename in files:
            if not fnmatch.fnmatch(filename, file_pattern):
                continue

            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, help_dir)
            rel_path_lower = rel_path.lower()

            path_matches = [term for term in query_terms if term in rel_path_lower]
            content_matches = []
            snippet = ""
            content = ""
            content_lower = ""

            if search_content:
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read(120000)
                    content_lower = content.lower()
                    content_matches = [term for term in query_terms if term in content_lower]
                except Exception:
                    continue

            if search_mode == "all":
                matched_terms = set(path_matches) | set(content_matches)
                is_match = all(term in matched_terms for term in query_terms)
            else:
                is_match = bool(path_matches or content_matches)

            if is_match:
                matched_in = []
                score = 0
                if path_matches:
                    matched_in.append("path")
                    score += 100 + 10 * len(path_matches)
                if content_matches:
                    matched_in.append("content")
                    score += 20 + 3 * len(content_matches)

                snippet_term = next((term for term in query_terms if term in content_lower), None)
                if snippet_term:
                    idx = content_lower.find(snippet_term)
                    start = max(0, idx - context_chars)
                    end = min(len(content), idx + len(snippet_term) + context_chars)
                    snippet = content[start:end].replace("\n", " ").strip()

                results.append({
                    "rel_path": rel_path,
                    "file_path": file_path,
                    "matched_in": "+".join(matched_in),
                    "matched_terms": sorted(set(path_matches + content_matches)),
                    "score": score,
                    "snippet": snippet,
                    "size_bytes": os.path.getsize(file_path),
                })

            if len(results) >= max_results:
                break
        if len(results) >= max_results:
            break

    results.sort(key=lambda item: (-item.get("score", 0), item["rel_path"]))
    return {
        "query": query,
        "query_terms": query_terms,
        "file_pattern": file_pattern,
        "search_content": search_content,
        "search_mode": search_mode,
        "help_dir": help_dir,
        "num_results": len(results),
        "results": results,
    }

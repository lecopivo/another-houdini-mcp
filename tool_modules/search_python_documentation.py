from typing import Any, Optional
import json

TOOL_NAME = "search_python_documentation"
IS_MUTATING = False

send_command = None

def search_python_documentation(search_term: str, search_type: str = "all") -> str:
    """
    Search through HOM documentation for classes, functions, or keywords

    This tool searches the Houdini Object Model (HOM) documentation to help you
    find the right class or function when you don't know the exact name.

    Use this when you need to:
    - Find what classes/functions are available for a task
    - Discover HOM APIs by keyword (e.g., "geometry", "parameter", "render")
    - Look up related functionality

    Search types:
    - "all" - Search all documentation (default)
    - "class" - Search only class names
    - "function" - Search only function names
    - "content" - Search documentation content

    Examples:
    - search_term="geometry" - Find all geometry-related classes/functions
    - search_term="node", search_type="class" - Find node-related classes
    - search_term="parameter" - Find parameter manipulation APIs
    - search_term="vector" - Find vector/math classes

    Args:
        search_term: Keyword to search for
        search_type: Type of search ("all", "class", "function", "content")

    Returns:
        List of matching documentation entries with brief descriptions
    """
    result = send_command({
        "type": "search_python_documentation",
        "params": {
            "search_term": search_term,
            "search_type": search_type
        }
    })

    if result.get("error"):
        return f"❌ {result['error']}"

    output = f"🔍 Search results for '{search_term}' (type: {search_type})\n"
    output += f"Found {result['num_results']} matches\n\n"

    if result['num_results'] == 0:
        output += "No matches found. Try:\n"
        output += "- Using different keywords\n"
        output += "- Searching with search_type='all'\n"
        output += "- Using list_python_commands() to browse all available commands\n"
        return output

    for match in result['matches'][:30]:  # Limit to 30 results
        output += f"  • hou.{match['name']}"
        if match.get('type'):
            output += f" ({match['type']})"
        if match.get('description'):
            desc = match['description'][:80] + "..." if len(match['description']) > 80 else match['description']
            output += f"\n    {desc}"
        output += "\n\n"

    if result['num_results'] > 30:
        output += f"... and {result['num_results'] - 30} more matches\n"

    output += "\nUse get_python_documentation('name') to see full documentation\n"

    return output


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(search_python_documentation)


def execute_plugin(params, server, hou):
    """Search through HOM documentation"""
    search_term = params.get("search_term", "").lower()
    search_type = params.get("search_type", "all").lower()

    import os
    import re

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    hou_dir = os.path.join(script_dir, "help", "hom", "hou")

    if not os.path.exists(hou_dir):
        return {
            "num_results": 0,
            "matches": [],
            "error": f"Documentation directory not found: {hou_dir}"
        }

    matches = []

    try:
        for filename in os.listdir(hou_dir):
            if not filename.endswith(".txt"):
                continue

            command_name = filename[:-4]
            file_path = os.path.join(hou_dir, filename)

            # Read first 200 lines to get metadata and description
            with open(file_path, 'r', encoding='utf-8') as f:
                content = ""
                for i, line in enumerate(f):
                    if i >= 200:  # Limit reading for performance
                        break
                    content += line

            # Extract metadata
            doc_type = None
            description = None
            group = None

            # Parse type
            type_match = re.search(r'^#type:\s*(\w+)', content, re.MULTILINE)
            if type_match:
                doc_type = type_match.group(1)

            # Parse group
            group_match = re.search(r'^#group:\s*(.+)', content, re.MULTILINE)
            if group_match:
                group = group_match.group(1).strip()

            # Extract description (usually in triple quotes)
            desc_match = re.search(r'"""(.+?)"""', content, re.DOTALL)
            if desc_match:
                description = desc_match.group(1).strip()
                # Clean up description - take first line or first 150 chars
                description = description.split('\n')[0]
                if len(description) > 150:
                    description = description[:150] + "..."

            # Determine if this matches based on search_type
            is_match = False

            if search_type == "all":
                # Search in name, description, and group
                if search_term in command_name.lower():
                    is_match = True
                elif description and search_term in description.lower():
                    is_match = True
                elif group and search_term in group.lower():
                    is_match = True
            elif search_type == "class":
                # Only match classes
                if doc_type == "homclass" and search_term in command_name.lower():
                    is_match = True
            elif search_type == "function":
                # Only match functions
                if doc_type == "homfunction" and search_term in command_name.lower():
                    is_match = True
            elif search_type == "content":
                # Search in description only
                if description and search_term in description.lower():
                    is_match = True

            if is_match:
                matches.append({
                    "name": command_name,
                    "type": doc_type if doc_type else "unknown",
                    "description": description if description else "",
                    "group": group if group else ""
                })

        # Sort by relevance (exact matches first, then alphabetical)
        def sort_key(match):
            name = match['name'].lower()
            # Exact match
            if name == search_term:
                return (0, name)
            # Starts with search term
            elif name.startswith(search_term):
                return (1, name)
            # Contains search term
            elif search_term in name:
                return (2, name)
            # Only in description
            else:
                return (3, name)

        matches.sort(key=sort_key)

        return {
            "num_results": len(matches),
            "matches": matches,
            "search_term": search_term,
            "search_type": search_type
        }

    except Exception as e:
        return {
            "num_results": 0,
            "matches": [],
            "error": f"Search failed: {str(e)}"
        }

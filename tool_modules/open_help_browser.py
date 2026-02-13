from typing import Optional
import re
import os

TOOL_NAME = "open_help_browser"
IS_MUTATING = False

send_command = None

HELP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "help")

CONCEPT_PATHS = {
    "crowds": "/crowds/index",
    "crowd": "/crowds/index",
    "agents": "/crowds/agents",
    "flip": "/fluid/sopconfigflip",
    "flip fluid": "/fluid/sopconfigflip",
    "pyro": "/pyro/overview",
    "vellum": "/vellum/index",
    "ocean": "/ocean/overview",
    "destruction": "/destruction/overview",
    "rop": "/render/rop",
    "mantra": "/props/mantra",
    "kinefx": "/kinefx/index",
    "lops": "/solaris/overview",
    "solaris": "/solaris/overview",
    "top": "/tops/overview",
    "mpm": "/mpm/index",
    "usd": "/solaris/overview",
    "karma": "/solaris/karma",
}

VALID_EXTENSIONS = (".txt", ".md")


def _help_path_exists(help_path: str) -> bool:
    """Check if a help path exists in the local documentation."""
    if not HELP_DIR or not os.path.isdir(HELP_DIR):
        return True

    path_parts = help_path.strip("/").split("/")
    search_dir = HELP_DIR

    for part in path_parts:
        if not part:
            continue
        candidate = os.path.join(search_dir, part)
        if os.path.isdir(candidate):
            search_dir = candidate
        elif os.path.isfile(candidate + ".txt") or os.path.isfile(candidate + ".md"):
            return True
        elif os.path.isfile(candidate):
            return True
        else:
            return False

    return True


def _find_matching_docs(query: str) -> list:
    """Find documentation files matching the query."""
    matches = []
    if not HELP_DIR or not os.path.isdir(HELP_DIR):
        return matches

    query_lower = query.lower()
    for root, dirs, files in os.walk(HELP_DIR):
        for f in files:
            if f.endswith(VALID_EXTENSIONS):
                rel_path = os.path.relpath(os.path.join(root, f), HELP_DIR)
                if query_lower in rel_path.lower():
                    matches.append(rel_path)

    return matches[:5]

def open_help_browser(
    node_type: Optional[str] = None,
    help_path: Optional[str] = None,
    concept: Optional[str] = None,
    vex_function: Optional[str] = None,
    python_command: Optional[str] = None,
    command: Optional[str] = None,
) -> str:
    """
    Open the Houdini Help Browser with relevant documentation.

    This tool can open help for different types of content:
    - Node documentation: Use node_type (e.g., 'flipsolver', 'box', 'merge')
    - General concepts: Use help_path (e.g., '/crowds/basics', '/pyro/overview')
    - VEX functions: Use vex_function (e.g., 'clamp', 'noise')
    - Python/HOM commands: Use python_command (e.g., 'hou.node', 'hou.ui')
    - General commands: Use command (e.g., 'ch', 'opwf')

    Args:
        node_type: Node type to look up (e.g., 'flipsolver', 'box', 'merge')
        help_path: Direct help path (e.g., '/crowds/basics', '/nodes/sop/copy')
        concept: General concept topic (e.g., 'crowds', 'pyro', 'vellum')
        vex_function: VEX function name (e.g., 'clamp', 'noise')
        python_command: Python/HOM command (e.g., 'hou.node', 'pwd')
        command: HScript command (e.g., 'ch', 'opwf', 'ls')

    Returns:
        Confirmation message showing what help was opened
    """
    result = send_command({
        "type": "open_help_browser",
        "params": {
            "node_type": node_type,
            "help_path": help_path,
            "concept": concept,
            "vex_function": vex_function,
            "python_command": python_command,
            "command": command,
        }
    })

    if result.get("error"):
        return f"❌ {result['error']}"

    return f"✅ {result['message']}"


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(open_help_browser)


def execute_plugin(params, server, hou):
    """Open the Houdini Help Browser with the specified content."""
    node_type = params.get("node_type")
    help_path = params.get("help_path")
    concept = params.get("concept")
    vex_function = params.get("vex_function")
    python_command = params.get("python_command")
    command = params.get("command")

    try:
        desktop = hou.ui.curDesktop()
        
        # Try to find existing help browser
        help_browser = desktop.findPaneTab("Help")
        message = ""  # Initialize message
        
        if help_browser is None:
            # Create a new floating help browser pane
            help_browser = desktop.createFloatingPaneTab(hou.paneTabType.HelpBrowser)

        # Determine what to display based on parameters
        if node_type:
            # Display node help - can be category/node (e.g., "sop/box") or just node
            if "/" in node_type:
                help_browser.displayHelpNode(node_type)
                message = f"Opened help for node: {node_type}"
            else:
                # Try common categories
                categories = ["sop", "obj", "dop", "pop", "vop", "cop2", "rop", "chop", "shop"]
                found = False
                for cat in categories:
                    full_type = f"{cat}/{node_type}"
                    node_def = hou.nodeType(full_type)
                    if node_def:
                        help_browser.displayHelpNode(full_type)
                        message = f"Opened help for node: {full_type}"
                        found = True
                        break
                if not found:
                    # Try as generic node type name
                    help_browser.displayHelpNode(node_type)
                    message = f"Opened help for node: {node_type}"
                    
        elif help_path:
            # Direct help path
            help_browser.displayHelpPath(help_path)
            message = f"Opened help: {help_path}"
            
        elif concept:
            # General concept - try common paths
            concept_lower = concept.lower()
            
            # Check if concept is known
            if concept_lower in CONCEPT_PATHS:
                help_path = CONCEPT_PATHS[concept_lower]
                if help_path is None:
                    # Concept known but has no direct help page
                    matches = _find_matching_docs(concept_lower)
                    if matches:
                        best_match = matches[0].replace(".txt", "").replace(".md", "")
                        help_path = "/" + best_match
                    else:
                        return {
                            "error": f"Concept '{concept}' does not have a dedicated help page. Try using 'solaris' instead for USD workflows.",
                            "message": ""
                        }
            else:
                # Try to construct path and validate
                help_path = f"/{concept_lower}/index"
                if not _help_path_exists(help_path):
                    # Try alternate path
                    alt_path = f"/{concept_lower}/overview"
                    if not _help_path_exists(alt_path):
                        matches = _find_matching_docs(concept_lower)
                        if matches:
                            best_match = matches[0].replace(".txt", "").replace(".md", "")
                            help_path = "/" + best_match
                        else:
                            return {
                                "error": f"Documentation for '{concept}' not found. Try a different term or use 'solaris' for USD.",
                                "message": ""
                            }
                    else:
                        help_path = alt_path
            
            help_browser.displayHelpPath(help_path)
            message = f"Opened help for concept: {concept} ({help_path})"
            
        elif vex_function:
            # VEX function help
            help_path = f"/vex/functions/{vex_function}"
            help_browser.displayHelpPath(help_path)
            message = f"Opened VEX help for: {vex_function}"
            
        elif python_command:
            # Python/HOM command help
            # Try as specific command or look up in HOM docs
            if python_command.startswith("hou."):
                # Direct HOM reference
                help_path = f"/hom/{python_command[4:]}"
            else:
                help_path = f"/hom/{python_command}"
            help_browser.displayHelpPath(help_path)
            message = f"Opened Python/HOM help for: {python_command}"
            
        elif command:
            # General HScript command
            help_path = f"/commands/{command}"
            help_browser.displayHelpPath(help_path)
            message = f"Opened command help for: {command}"
            
        else:
            # Default to home page
            help_browser.homePage()
            message = "Opened Houdini Help Browser (home page)"

        return {
            "message": message,
            "success": True
        }

    except Exception as e:
        return {
            "error": f"Failed to open help browser: {str(e)}",
            "message": ""
        }

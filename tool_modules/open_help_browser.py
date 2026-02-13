from typing import Optional
import re

TOOL_NAME = "open_help_browser"
IS_MUTATING = False

send_command = None

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
            # Map common concept names to help paths
            concept_paths = {
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
            }
            
            if concept_lower in concept_paths:
                help_path = concept_paths[concept_lower]
            else:
                help_path = f"/{concept_lower}/index"
            
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

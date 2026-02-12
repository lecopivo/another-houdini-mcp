from typing import Any, Optional
import json

TOOL_NAME = "list_python_commands"
IS_MUTATING = False

send_command = None

def list_python_commands() -> str:
    """
    List all available Python HOM (Houdini Object Model) commands

    Returns a list of all hou module functions and classes available in the
    Python API documentation.

    Returns:
        List of all Python commands in the hou module
    """
    result = send_command({
        "type": "list_python_commands",
        "params": {}
    })

    output = f"🐍 Python HOM Commands: {result['num_commands']}\n\n"

    # Group commands by category if available
    if result.get('categories'):
        for category, commands in result['categories'].items():
            output += f"\n{category}:\n"
            for cmd in commands[:20]:  # Limit per category
                output += f"  • hou.{cmd}\n"
            if len(commands) > 20:
                output += f"  ... and {len(commands) - 20} more\n"
    else:
        # Fallback to flat list
        for cmd in result['commands'][:100]:
            output += f"  • hou.{cmd}\n"
        if result['num_commands'] > 100:
            output += f"\n... and {result['num_commands'] - 100} more commands\n"

    output += "\nTip: Use get_python_documentation('command_name') for detailed info\n"

    return output


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(list_python_commands)


def execute_plugin(params, server, hou):
    """List all available Python HOM commands from help/hom/hou directory"""
    import os

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the hou documentation directory
    hou_dir = os.path.join(script_dir, "help", "hom", "hou")

    if not os.path.exists(hou_dir):
        return {
            "num_commands": 0,
            "commands": [],
            "error": f"Documentation directory not found: {hou_dir}"
        }

    try:
        # List all .txt files in the hou directory
        commands = []
        for filename in os.listdir(hou_dir):
            if filename.endswith(".txt"):
                # Remove .txt extension
                command_name = filename[:-4]
                commands.append(command_name)

        # Sort alphabetically
        commands.sort()

        return {
            "num_commands": len(commands),
            "commands": commands
        }
    except Exception as e:
        return {
            "num_commands": 0,
            "commands": [],
            "error": f"Failed to list commands: {str(e)}"
        }

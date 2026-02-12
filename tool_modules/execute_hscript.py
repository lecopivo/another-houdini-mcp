TOOL_NAME = "execute_hscript"
IS_MUTATING = True


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def execute_hscript(code: str) -> str:
        """
        Execute HScript commands in Houdini

        IMPORTANT TOOL-USAGE RULE:
        For usual scene tasks (creating nodes, connecting nodes, setting parameters,
        and inspecting scene structure), use dedicated MCP tools first.
        Use execute_hscript only when no dedicated tool can do the task.
        If the command solves a reusable/general workflow, suggest adding a
        dedicated MCP tool for it instead of relying on custom HScript.

        WARNING: Use carefully - executes directly in Houdini

        Args:
            code: HScript code to execute

        Returns:
            Output from execution
        """
        result = send_command({
            "type": TOOL_NAME,
            "params": {"code": code}
        })

        output = result.get("output", "")
        error = result.get("error", "")

        if error:
            return f"Output:\n{output}\n\nErrors:\n{error}"
        return output


def execute_plugin(params, server, hou):
    code = params.get("code", "")
    try:
        result = hou.hscript(code)
        return {"output": result[0], "error": result[1]}
    except Exception as e:
        raise ValueError(f"HScript failed: {str(e)}")

TOOL_NAME = "execute_python"
IS_MUTATING = True


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def execute_python(code: str, allow_dangerous: bool = False) -> str:
        """
        Execute Python code in Houdini using the Houdini Object Model (HOM)

        IMPORTANT TOOL-USAGE RULE:
        For usual scene tasks (creating nodes, connecting nodes, setting parameters,
        and inspecting scene structure), use dedicated MCP tools first.

        Use execute_python only when no dedicated tool can do the task.
        If a custom snippet is reusable and generic, propose creating a new
        dedicated MCP tool instead of repeating ad-hoc code execution.

        WARNING: Use carefully - executes directly in Houdini.
        By default, dangerous patterns are blocked (subprocess, destructive os/shutil,
        hou.exit, etc.). Set allow_dangerous=True only when you explicitly need it.

        Args:
            code: Python code to execute (hou module is available)
            allow_dangerous: Allow potentially dangerous operations (default: False)

        Returns:
            Output from execution
        """
        result = send_command({
            "type": TOOL_NAME,
            "params": {"code": code, "allow_dangerous": allow_dangerous}
        })

        output = ""

        if result.get("return_value") is not None:
            output += f"Return value: {result['return_value']}\n\n"

        if result.get("output"):
            output += f"Output:\n{result['output']}\n"

        if result.get("error"):
            output += f"\n❌ Error:\n{result['error']}"

        if not output:
            output = "✅ Executed successfully (no output)"

        return output


def execute_plugin(params, server, hou):
    code = params.get("code", "")
    allow_dangerous = bool(params.get("allow_dangerous", False))

    import sys
    import textwrap
    from io import StringIO

    normalized_code = textwrap.dedent(code).strip()
    flattened_code = " ".join(
        line.strip() for line in normalized_code.splitlines() if line.strip()
    )

    dangerous_patterns = [
        "hou.exit",
        "os.remove",
        "os.unlink",
        "shutil.rmtree",
        "subprocess",
        "os.system",
        "os.popen",
        "__import__",
    ]

    if not allow_dangerous:
        lowered = normalized_code.lower()
        for pattern in dangerous_patterns:
            if pattern in lowered:
                raise ValueError(
                    "Dangerous pattern detected in execute_python: "
                    f"'{pattern}'. Set allow_dangerous=True to override."
                )

    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()

    result = {
        "return_value": None,
        "output": "",
        "error": ""
    }

    try:
        try:
            return_value = eval(normalized_code, {"hou": hou, "__builtins__": __builtins__})
            result["return_value"] = str(return_value) if return_value is not None else None
        except SyntaxError:
            try:
                exec(normalized_code, {"hou": hou, "__builtins__": __builtins__})
            except SyntaxError:
                exec(flattened_code, {"hou": hou, "__builtins__": __builtins__})

        result["output"] = captured_output.getvalue()

    except Exception:
        import traceback
        result["error"] = traceback.format_exc()

    finally:
        sys.stdout = old_stdout

    return result

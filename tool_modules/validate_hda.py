from typing import Any, Optional
import json

TOOL_NAME = "validate_hda"
IS_MUTATING = False

send_command = None

def validate_hda(node_path: str, rules: Any) -> str:
    """Validate HDA structure and expectations."""
    result = send_command({
        "type": "validate_hda",
        "params": {
            "node_path": node_path,
            "rules": rules,
        }
    })
    output = (
        f"🧪 validate_hda\n"
        f"Node: {result.get('node_path')}\n"
        f"Valid: {result.get('valid')}\n"
        f"Checks: {len(result.get('checks', []))}\n"
        f"Errors: {len(result.get('errors', []))}\n"
        f"Warnings: {len(result.get('warnings', []))}\n"
    )
    if result.get("errors"):
        output += "\nError details:\n"
        for err in result["errors"]:
            output += f"- {err}\n"
    if result.get("warnings"):
        output += "\nWarnings:\n"
        for warning in result["warnings"]:
            output += f"- {warning}\n"
    return output.strip()


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(validate_hda)


def execute_plugin(params, server, hou):
    """Validate common HDA expectations and return diagnostics."""
    node_path = params.get("node_path", "")
    rules = params.get("rules", {})

    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")

    errors = []
    warnings = []
    checks = []

    definition = node.type().definition()
    require_definition = bool(rules.get("require_definition", True))
    if require_definition and definition is None:
        errors.append("Node is not an HDA instance")
    checks.append({"check": "is_hda_instance", "ok": definition is not None})

    require_match = bool(rules.get("require_match_definition", False))
    matches_definition = node.matchesCurrentDefinition() if definition else False
    if require_match and not matches_definition:
        errors.append("Node does not match current definition")
    checks.append({"check": "matches_current_definition", "ok": matches_definition})

    required_parameters = rules.get("required_parameters", [])
    for parm_name in required_parameters:
        ok = node.parm(parm_name) is not None
        checks.append({"check": f"has_parameter:{parm_name}", "ok": ok})
        if not ok:
            errors.append(f"Missing parameter: {parm_name}")

    required_internal_nodes = rules.get("required_internal_nodes", [])
    for rel_path in required_internal_nodes:
        internal = node.node(rel_path)
        ok = internal is not None
        checks.append({"check": f"has_internal_node:{rel_path}", "ok": ok})
        if not ok:
            errors.append(f"Missing internal node: {rel_path}")

    expected_output_indices = rules.get("expected_output_indices", [])
    for entry in expected_output_indices:
        rel_node = entry.get("node", "")
        expected = int(entry.get("index", 0))
        internal = node.node(rel_node)
        ok = False
        if internal is not None and internal.parm("outputidx") is not None:
            ok = (internal.parm("outputidx").eval() == expected)
        checks.append({"check": f"output_index:{rel_node}", "ok": ok})
        if not ok:
            errors.append(f"Output index mismatch for {rel_node}, expected {expected}")

    primitive_type_expectations = rules.get("primitive_type_expectations", [])
    for entry in primitive_type_expectations:
        rel_node = entry.get("node", "")
        expected_token = str(entry.get("token", ""))
        internal = node.node(rel_node)
        ok = False
        if internal is not None and internal.parm("type") is not None:
            ok = (internal.parm("type").evalAsString() == expected_token)
        checks.append({"check": f"primitive_type:{rel_node}", "ok": ok})
        if not ok:
            errors.append(f"Primitive type mismatch for {rel_node}, expected {expected_token}")

    if definition and not definition.libraryFilePath():
        warnings.append("Definition has no library file path")

    return {
        "node_path": node.path(),
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
    }

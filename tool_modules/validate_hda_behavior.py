from typing import Any, Optional
import json

TOOL_NAME = "validate_hda_behavior"
IS_MUTATING = False

send_command = None

def validate_hda_behavior(
    node_path: str,
    cases: Any,
    comparisons: Optional[Any] = None,
    require_point_attributes: Optional[Any] = None,
) -> str:
    """Validate HDA behavior across parameterized geometry test cases."""
    result = send_command({
        "type": "validate_hda_behavior",
        "params": {
            "node_path": node_path,
            "cases": cases,
            "comparisons": comparisons or [],
            "require_point_attributes": require_point_attributes or [],
        }
    })
    output = (
        f"🧪 validate_hda_behavior\n"
        f"Node: {result.get('node_path')}\n"
        f"Valid: {result.get('valid')}\n"
        f"Cases: {len(result.get('case_results', {}))}\n"
        f"Checks: {len(result.get('checks', []))}\n"
        f"Errors: {len(result.get('errors', []))}\n"
    )
    if result.get("errors"):
        output += "\nError details:\n"
        for err in result["errors"]:
            output += f"- {err}\n"
    return output.strip()


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(validate_hda_behavior)


def execute_plugin(params, server, hou):
    """Validate HDA behavior by probing geometry across parameterized test cases."""
    node_path = params.get("node_path", "")
    cases = params.get("cases", [])
    comparisons = params.get("comparisons", [])
    require_point_attributes = params.get("require_point_attributes", [])

    node = hou.node(node_path)
    if not node:
        raise ValueError(f"Node not found: {node_path}")
    if not isinstance(cases, list) or len(cases) == 0:
        raise ValueError("cases must be a non-empty list")

    # Save initial parm values for all params touched by cases.
    tracked_parms = set()
    for case in cases:
        for parm_name in case.get("set_parameters", {}).keys():
            tracked_parms.add(parm_name)
    saved_values = {}
    for parm_name in tracked_parms:
        parm = node.parm(parm_name)
        if parm is not None:
            saved_values[parm_name] = parm.eval()

    case_results = {}
    errors = []
    checks = []

    try:
        for case in cases:
            name = case.get("name", "")
            if not name:
                raise ValueError("Each case requires a non-empty name")

            for parm_name, value in case.get("set_parameters", {}).items():
                parm = node.parm(parm_name)
                if parm is None:
                    raise ValueError(f"Parameter not found on node: {parm_name}")
                parm.set(value)

            stats = self._geometry_stats(node)
            case_results[name] = stats

            for attr_name in require_point_attributes:
                ok = attr_name in stats["point_attributes"]
                checks.append({"check": f"{name}:has_point_attr:{attr_name}", "ok": ok})
                if not ok:
                    errors.append(f"Case '{name}' missing point attribute '{attr_name}'")

        op_map = {
            "gt": lambda a, b: a > b,
            "ge": lambda a, b: a >= b,
            "lt": lambda a, b: a < b,
            "le": lambda a, b: a <= b,
            "eq": lambda a, b: a == b,
            "ne": lambda a, b: a != b,
        }

        for comparison in comparisons:
            case_a = comparison.get("a")
            case_b = comparison.get("b")
            metric = comparison.get("metric", "points")
            op = str(comparison.get("op", "gt")).lower()

            if case_a not in case_results or case_b not in case_results:
                raise ValueError(f"Invalid comparison cases: {case_a}, {case_b}")
            if metric not in ("points", "prims", "vertices"):
                raise ValueError(f"Unsupported metric for comparison: {metric}")
            if op not in op_map:
                raise ValueError(f"Unsupported comparison op: {op}")

            left = case_results[case_a][metric]
            right = case_results[case_b][metric]
            ok = op_map[op](left, right)
            checks.append({
                "check": f"{case_a}.{metric} {op} {case_b}.{metric}",
                "ok": ok,
                "left": left,
                "right": right,
            })
            if not ok:
                errors.append(
                    f"Behavior check failed: {case_a}.{metric} ({left}) "
                    f"{op} {case_b}.{metric} ({right})"
                )
    finally:
        for parm_name, value in saved_values.items():
            parm = node.parm(parm_name)
            if parm is not None:
                parm.set(value)

    return {
        "node_path": node.path(),
        "valid": len(errors) == 0,
        "errors": errors,
        "checks": checks,
        "case_results": case_results,
    }

from typing import Any, Optional
import json

from .hda_utils import resolve_hda_definition

TOOL_NAME = "set_hda_parm_default"
IS_MUTATING = True

send_command = None


def _coerce_default_value(value):
    if not isinstance(value, str):
        return value

    text = value.strip()
    if not text:
        return value

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        lower = text.lower()
        if lower in ("true", "false"):
            return lower == "true"
        try:
            if any(ch in text for ch in (".", "e", "E")):
                return float(text)
            return int(text)
        except ValueError:
            return value


def _coerce_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        lower = value.strip().lower()
        if lower in ("1", "true", "yes", "on"):
            return True
        if lower in ("0", "false", "no", "off", ""):
            return False
    raise ValueError(f"Cannot coerce value to bool: {value}")


def _normalize_default_value(value):
    if isinstance(value, tuple):
        if len(value) == 1:
            return value[0]
        return list(value)
    return value


def _defaults_equal(expected, actual):
    return _normalize_default_value(expected) == _normalize_default_value(actual)

def set_hda_parm_default(
    param_name: str,
    default_value: Any,
    node_path: Optional[str] = None,
    type_name: Optional[str] = None,
    definition_name: Optional[str] = None,
    sync_instance: bool = True,
) -> str:
    """Set a default value for an HDA parameter template."""
    result = send_command({
        "type": "set_hda_parm_default",
        "params": {
            "node_path": node_path,
            "type_name": type_name,
            "definition_name": definition_name,
            "param_name": param_name,
            "default_value": default_value,
            "sync_instance": sync_instance,
        }
    })
    return (
        f"✅ HDA default updated\n"
        f"Definition: {result.get('definition_name')}\n"
        f"Parameter: {result.get('param_name')}\n"
        f"Default: {result.get('default_value')}"
    )


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(set_hda_parm_default)


def execute_plugin(params, server, hou):
    """Set a single default value on an HDA definition parameter template."""
    node, definition = resolve_hda_definition(params, hou)
    param_name = params.get("param_name", "")
    default_value = _coerce_default_value(params.get("default_value"))

    if not param_name:
        raise ValueError("param_name is required")
    if default_value is None:
        raise ValueError("default_value is required")

    ptg = definition.parmTemplateGroup()
    template = ptg.find(param_name)
    if template is None:
        raise ValueError(f"Parameter template not found: {param_name}")

    parm_type = template.type()
    expected_default = None

    if parm_type == hou.parmTemplateType.Toggle:
        expected_default = _coerce_bool(default_value)
        template.setDefaultValue(expected_default)
    elif parm_type == hou.parmTemplateType.Menu:
        expected_default = int(default_value)
        template.setDefaultValue(expected_default)
    else:
        num_components = template.numComponents() if hasattr(template, "numComponents") else 1
        if isinstance(default_value, (list, tuple)):
            value_tuple = tuple(default_value)
        else:
            value_tuple = tuple(default_value for _ in range(num_components))
        if len(value_tuple) != num_components:
            raise ValueError(
                f"default_value length mismatch for {param_name}. "
                f"Expected {num_components}, got {len(value_tuple)}"
            )

        if parm_type == hou.parmTemplateType.Int:
            value_tuple = tuple(int(v) for v in value_tuple)
        elif parm_type == hou.parmTemplateType.String:
            value_tuple = tuple(str(v) for v in value_tuple)
        else:
            value_tuple = tuple(float(v) for v in value_tuple)

        expected_default = value_tuple if num_components != 1 else value_tuple[0]
        template.setDefaultValue(value_tuple)

    ptg.replace(param_name, template)
    definition.setParmTemplateGroup(ptg)

    updated = definition.parmTemplateGroup().find(param_name)
    if updated is None:
        raise ValueError(f"Parameter template not found after update: {param_name}")
    actual_default = updated.defaultValue()
    if not _defaults_equal(expected_default, actual_default):
        raise ValueError(
            f"Default value for '{param_name}' did not persist. "
            f"Expected {_normalize_default_value(expected_default)!r}, "
            f"got {_normalize_default_value(actual_default)!r}. "
            "This parameter may be a non-editable built-in default."
        )

    if node is not None and bool(params.get("sync_instance", True)):
        node.matchCurrentDefinition()

    return {
        "definition_name": definition.nodeTypeName(),
        "param_name": param_name,
        "default_value": default_value,
    }
